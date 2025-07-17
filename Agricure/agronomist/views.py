import json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from users.models import User  
from administrator.models import DatasetUpload
from diagnosis.models import Diagnosis
from django.db.models import Count, Avg
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages 
from recommendations.models import Recommendation


@login_required
def dashboard(request):
    if request.user.role != 'AGRONOMIST':
        return render(request, '403.html')  # or redirect with error

    return render(request, 'agronomist/dashboard.html')


@login_required
def dataset_list(request):
    if request.user.role.lower() != 'agronomist':
        return render(request, '403.html')  # Optional error page

    datasets = DatasetUpload.objects.all().order_by('-uploaded_at')
    return render(request, 'agronomist/dataset_list.html', {'datasets': datasets})

@login_required
def agronomist_report(request):
    if request.user.role not in ['AGRONOMIST', 'FARMER']:
        messages.error(request, "Access denied.")
        return redirect('agronomist:dashboard')

    # For AGRONOMIST, use assigned_agronomist; for FARMER, use user
    if request.user.role == 'AGRONOMIST':
        diagnoses = Diagnosis.objects.filter(user=request.user)

    else:
        diagnoses = Diagnosis.objects.filter(user=request.user)

    diagnoses = diagnoses.order_by('-timestamp')

    disease_summary = diagnoses.values('disease_name') \
        .annotate(total=Count('disease_name')) \
        .order_by('-total')

    avg_confidence = diagnoses.aggregate(avg=Avg('confidence'))

    # Fetch recommendations
    recommendations = Recommendation.objects.filter(diagnosis__in=diagnoses)

    treatment_keywords = []
    prevention_keywords = []

    for rec in recommendations:
        try:
            rec_data = json.loads(rec.recommendation_json)
            treatment_keywords += rec_data.get('treatment', [])
            prevention_keywords += rec_data.get('prevention', [])
        except Exception as e:
            print(f"Recommendation parsing failed: {e}")
            continue

    from collections import Counter
    top_treatments = Counter(treatment_keywords).most_common(5)
    top_preventions = Counter(prevention_keywords).most_common(5)

    # Handle email form submission
    if request.method == 'POST':
        recipient_email = request.POST.get('recipient_email')
        context = {
            'diagnoses': diagnoses,
            'disease_summary': disease_summary,
            'avg_confidence': round(avg_confidence['avg'] or 0, 1),
            'top_treatments': top_treatments,
            'top_preventions': top_preventions,
            'recommendations': recommendations,
            'agronomist': request.user
        }
        email_html = render_to_string('agronomist/email_report.html', context)
        email = EmailMessage(
            subject='Agronomist Report Summary',
            body=email_html,
            from_email='ayanhilwa@gmail.com',
            to=[recipient_email]
        )
        email.content_subtype = 'html'
        email.send()
        messages.success(request, f'Report successfully sent to {recipient_email}')
        return redirect('agronomist:report')

    context = {
        'diagnoses': diagnoses,
        'disease_summary': disease_summary,
        'avg_confidence': round(avg_confidence['avg'] or 0, 1),
        'top_treatments': top_treatments,
        'top_preventions': top_preventions,
        'recommendations': recommendations, 
    }
    return render(request, 'agronomist/report.html', context)


@login_required
def report_view(request):
    user = request.user
    diagnoses = Diagnosis.objects.filter(user=user)


    # Existing stats
    total_diagnoses = diagnoses.count()
    avg_confidence = round(diagnoses.aggregate(Avg('confidence'))['confidence__avg'] or 0, 1)

    # Disease summary
    disease_summary = diagnoses.values('disease_name').annotate(total=Count('id')).order_by('-total')

    # NEW: Recommendations based on those diagnoses
    recommendations = Recommendation.objects.filter(diagnosis__in=diagnoses)

    treatment_keywords = []
    prevention_keywords = []

    for rec in recommendations:
        try:
            rec_data = json.loads(rec.recommendation_json)
            treatment_keywords += rec_data.get('treatment', [])
            prevention_keywords += rec_data.get('prevention', [])
        except Exception:
            continue

    from collections import Counter
    top_treatments = Counter(treatment_keywords).most_common(5)
    top_preventions = Counter(prevention_keywords).most_common(5)

    context = {
        'diagnoses': diagnoses,
        'avg_confidence': avg_confidence,
        'disease_summary': disease_summary,
        'recommendations': recommendations,
        'top_treatments': top_treatments,
        'top_preventions': top_preventions,
        'recommendations': recommendations,
        'agronomist': request.user
    }

    return render(request, 'agronomist/report.html', context)
