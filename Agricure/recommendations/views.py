from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
import json
import logging

from .Open_weather import WeatherClient
from .Soil import ISDAsoilClient
from .Gemini import GeminiContentGenerator
from .models import Recommendation, Feedback
from .forms import RecommendationRequestForm, RecommendationFeedbackForm
from diagnosis.models import Diagnosis

logger = logging.getLogger(__name__)

@login_required
def recommendation_dashboard(request):
    """
    Main dashboard showing user's recommendations
    """
    # Get user's recommendations through their diagnoses
    user_recommendations = Recommendation.objects.filter(
        diagnosis__user=request.user
    ).select_related('diagnosis')
    
    # Get recent recommendations
    recent_recommendations = user_recommendations[:5]
    
    # Get statistics
    total_recommendations = user_recommendations.count()
    healthy_count = user_recommendations.filter(diagnosis__disease_name__icontains='healthy').count()
    diseased_count = total_recommendations - healthy_count
    
    # Get recommendations needing feedback
    needs_feedback = user_recommendations.filter(
        feedback__isnull=True
    ).count()
    
    context = {
        'recent_recommendations': recent_recommendations,
        'total_recommendations': total_recommendations,
        'healthy_count': healthy_count,
        'diseased_count': diseased_count,
        'needs_feedback': needs_feedback,
    }
    
    return render(request, 'recommendations/dashboard.html', context)

@login_required
def recommendation_list(request):
    """
    List all recommendations for the user with filtering
    """
    recommendations = Recommendation.objects.filter(
        diagnosis__user=request.user
    ).select_related('diagnosis').order_by('-created_at')
    
    # Apply filters
    search_query = request.GET.get('search', '')
    disease_filter = request.GET.get('disease', '')
    city_filter = request.GET.get('city', '')
    
    if search_query:
        recommendations = recommendations.filter(
            Q(diagnosis__disease_name__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(treatment_summary__icontains=search_query)
        )
    
    if disease_filter:
        recommendations = recommendations.filter(
            diagnosis__disease_name__icontains=disease_filter
        )
    
    if city_filter:
        recommendations = recommendations.filter(city__icontains=city_filter)
    
    # Pagination
    paginator = Paginator(recommendations, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get unique values for filters
    all_diseases = Recommendation.objects.filter(
        diagnosis__user=request.user
    ).values_list('diagnosis__disease_name', flat=True).distinct()
    
    all_cities = Recommendation.objects.filter(
        diagnosis__user=request.user
    ).values_list('city', flat=True).distinct()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'disease_filter': disease_filter,
        'city_filter': city_filter,
        'all_diseases': all_diseases,
        'all_cities': all_cities,
    }
    
    return render(request, 'recommendations/list.html', context)

@login_required
def request_recommendation(request, diagnosis_id):
    """
    Request a recommendation for a specific diagnosis
    """
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id, user=request.user)
    
    # Check if recommendation already exists
    if hasattr(diagnosis, 'recommendation'):
        messages.info(request, 'A recommendation already exists for this diagnosis.')
        return redirect('recommendations:detail', pk=diagnosis.recommendation.pk)
    
    if request.method == 'POST':
        form = RecommendationRequestForm(request.POST)
        if form.is_valid():
            try:
                # Get form data
                city = form.cleaned_data['city']
                country_code = form.cleaned_data.get('country_code', 'UG')
                lat = form.cleaned_data.get('latitude')
                lon = form.cleaned_data.get('longitude')
                
                # Get coordinates if not provided
                if not lat or not lon:
                    weather_client = WeatherClient()
                    coords = weather_client.get_coordinates_by_city(city, country_code)
                    if coords:
                        lat, lon = coords['lat'], coords['lon']
                    else:
                        messages.error(request, 'Could not find coordinates for the specified city.')
                        return render(request, 'recommendations/request.html', {
                            'form': form, 
                            'diagnosis': diagnosis
                        })
                
                # Get weather and soil data
                weather_client = WeatherClient()
                weather_data = weather_client.get_weather_for_gemini(lat, lon)
                
                soil_client = ISDAsoilClient()
                soil_data = soil_client.get_soil_for_gemini(lat, lon)
                
                # Generate recommendation
                gemini_generator = GeminiContentGenerator()
                recommendation_json = gemini_generator.generate_recommendation(
                    diagnosis.disease_name, 
                    weather_data, 
                    soil_data
                )
                
                if not recommendation_json:
                    messages.error(request, 'Failed to generate recommendation. Please try again.')
                    return render(request, 'recommendations/request.html', {
                        'form': form, 
                        'diagnosis': diagnosis
                    })
                
                # Parse recommendation for summary fields
                try:
                    recommendation_data = json.loads(recommendation_json)
                    treatment_summary = '; '.join(recommendation_data.get('treatment', [])[:3])
                    prevention_summary = '; '.join(recommendation_data.get('prevention', [])[:3])
                except (json.JSONDecodeError, KeyError):
                    treatment_summary = "See full recommendation for details"
                    prevention_summary = "See full recommendation for details"
                
                # Create recommendation
                recommendation = Recommendation.objects.create(
                    diagnosis=diagnosis,
                    city=city,
                    latitude=lat,
                    longitude=lon,
                    # Store weather data
                    temperature=weather_data[0] if weather_data and len(weather_data) > 0 else None,
                    humidity=weather_data[1] if weather_data and len(weather_data) > 1 else None,
                    pressure=weather_data[2] if weather_data and len(weather_data) > 2 else None,
                    wind_speed=weather_data[3] if weather_data and len(weather_data) > 3 else None,
                    weather_description=weather_data[5] if weather_data and len(weather_data) > 5 else None,
                    # Store soil data
                    soil_ph=soil_data[0] if soil_data and len(soil_data) > 0 else None,
                    organic_carbon=soil_data[1] if soil_data and len(soil_data) > 1 else None,
                    soil_nitrogen=soil_data[2] if soil_data and len(soil_data) > 2 else None,
                    soil_phosphorus=soil_data[3] if soil_data and len(soil_data) > 3 else None,
                    soil_potassium=soil_data[4] if soil_data and len(soil_data) > 4 else None,
                    # Store recommendation
                    recommendation_json=recommendation_json,
                    treatment_summary=treatment_summary,
                    prevention_summary=prevention_summary,
                )
                
                messages.success(request, 'Recommendation generated successfully!')
                return redirect('recommendations:detail', pk=recommendation.pk)
                
            except Exception as e:
                logger.error(f"Error generating recommendation: {str(e)}")
                messages.error(request, f'Error generating recommendation: {str(e)}')
                return render(request, 'recommendations/request.html', {
                    'form': form, 
                    'diagnosis': diagnosis
                })
    else:
        form = RecommendationRequestForm()
    
    return render(request, 'recommendations/request.html', {
        'form': form, 
        'diagnosis': diagnosis
    })

@login_required
def recommendation_detail(request, pk):
    """
    View detailed recommendation
    """
    recommendation = get_object_or_404(
        Recommendation, 
        pk=pk, 
        diagnosis__user=request.user
    )
    
    # Parse JSON recommendation
    try:
        recommendation_data = json.loads(recommendation.recommendation_json)
    except json.JSONDecodeError:
        recommendation_data = {}
    
    # Get or create feedback form
    feedback = getattr(recommendation, 'feedback', None)
    feedback_form = None
    
    if request.method == 'POST' and 'feedback' in request.POST:
        if feedback:
            feedback_form = RecommendationFeedbackForm(request.POST, instance=feedback.first())
        else:
            feedback_form = RecommendationFeedbackForm(request.POST)
        
        if feedback_form.is_valid():
            feedback_obj = feedback_form.save(commit=False)
            feedback_obj.recommendation = recommendation
            feedback_obj.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('recommendations:detail', pk=pk)
    else:
        if feedback:
            feedback_form = RecommendationFeedbackForm(instance=feedback.first())
        else:
            feedback_form = RecommendationFeedbackForm()
    
    context = {
        'recommendation': recommendation,
        'recommendation_data': recommendation_data,
        'feedback_form': feedback_form,
        'has_feedback': feedback.exists() if feedback else False,
    }
    
    return render(request, 'recommendations/detail.html', context)

@login_required
@csrf_exempt
def get_agricultural_recommendation(request):
    """
    API endpoint for getting recommendations (for AJAX calls)
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Get coordinates
            lat = data.get('lat')
            lon = data.get('lon')
            city = data.get('city')
            disease = data.get('disease', 'healthy')
            
            if not lat or not lon:
                if city:
                    weather_client = WeatherClient()
                    coords = weather_client.get_coordinates_by_city(city)
                    if coords:
                        lat, lon = coords['lat'], coords['lon']
                    else:
                        return JsonResponse({'error': 'Location not found'}, status=404)
                else:
                    return JsonResponse({'error': 'Coordinates or city name required'}, status=400)
            
            # Get weather data
            weather_client = WeatherClient()
            weather_data = weather_client.get_weather_for_gemini(lat, lon)
            
            # Get soil data
            soil_client = ISDAsoilClient()
            soil_data = soil_client.get_soil_for_gemini(lat, lon)
            
            # Generate recommendation
            gemini_generator = GeminiContentGenerator()
            recommendation = gemini_generator.generate_recommendation(disease, weather_data, soil_data)
            
            response_data = {
                'recommendation': recommendation,
                'weather_data': weather_data,
                'soil_data': soil_data,
                'coordinates': {'lat': lat, 'lon': lon},
                'disease': disease
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

@login_required
def delete_recommendation(request, pk):
    """
    Delete a recommendation
    """
    recommendation = get_object_or_404(
        Recommendation, 
        pk=pk, 
        diagnosis__user=request.user
    )
    
    if request.method == 'POST':
        recommendation.delete()
        messages.success(request, 'Recommendation deleted successfully.')
        return redirect('recommendations:list')
    
    return render(request, 'recommendations/confirm_delete.html', {
        'recommendation': recommendation
    })

@login_required
def provide_feedback(request, pk):
    """Provide feedback for a recommendation"""
    recommendation = get_object_or_404(Recommendation, id=pk)
    
    if request.method == 'POST':
        # Create feedback instance
        feedback = Feedback.objects.create(
            recommendation=recommendation,
            user=request.user,
            rating=request.POST.get('rating'),
            usefulness=request.POST.get('usefulness'),
            treatment_effectiveness=request.POST.get('treatment_effectiveness'),
            comments=request.POST.get('comments', ''),
            improvements=request.POST.getlist('improvements')
        )
        
        messages.success(request, 'Thank you for your feedback! This helps us improve our AI recommendations.')
        return redirect('recommendations:detail', pk=recommendation.id)
    
    return render(request, 'recommendations/feedback.html', {
        'recommendation': recommendation
    })
