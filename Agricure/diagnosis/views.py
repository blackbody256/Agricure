from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DiagnosisForm
from .models import Diagnosis

import base64
import uuid
from django.core.files.base import ContentFile
 
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.efficientnet import preprocess_input  # 🔧 ADD: EfficientNet preprocessing
import os

import logging
import json

# 🔧 NEW: Add recommendation imports
from recommendations.models import Recommendation
from recommendations.Open_weather import WeatherClient
from recommendations.Gemini import GeminiContentGenerator

logger = logging.getLogger(__name__)

# Load the model once globally
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'diagnosis', 'model', 'newresult.h5')
model = tf.keras.models.load_model(MODEL_PATH)

DISEASE_CLASSES = [
    'Apple___Apple_scab',
    'Apple___Black_rot',
    'Apple___Cedar_apple_rust',
    'Apple___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
    'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight',
    'Corn_(maize)___healthy',
    'Pepper__bell___Bacterial_spot',
    'Pepper__bell___healthy',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Potato___healthy',
    'Tomato_Bacterial_spot',
    'Tomato_Early_blight',
    'Tomato_Late_blight',
    'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus',
    'Tomato__Tomato_mosaic_virus',
    'Tomato_healthy'
]


DISEASE_LABELS = {
    'Apple___Apple_scab': 'Apple Scab',
    'Apple___Black_rot': 'Apple Black Rot',
    'Apple___Cedar_apple_rust': 'Apple Cedar Apple Rust',
    'Apple___healthy': 'Apple (Healthy)',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Corn Gray Leaf Spot',
    'Corn_(maize)___Common_rust_': 'Corn Common Rust',
    'Corn_(maize)___Northern_Leaf_Blight': 'Corn Northern Leaf Blight',
    'Corn_(maize)___healthy': 'Corn (Healthy)',
    'Pepper__bell___Bacterial_spot': 'Pepper Bell Bacterial Spot',
    'Pepper__bell___healthy': 'Pepper Bell (Healthy)',
    'Potato___Early_blight': 'Potato Early Blight',
    'Potato___Late_blight': 'Potato Late Blight',
    'Potato___healthy': 'Potato (Healthy)',
    'Tomato_Bacterial_spot': 'Tomato Bacterial Spot',
    'Tomato_Early_blight': 'Tomato Early Blight',
    'Tomato_Late_blight': 'Tomato Late Blight',
    'Tomato_Leaf_Mold': 'Tomato Leaf Mold',
    'Tomato_Septoria_leaf_spot': 'Tomato Septoria Leaf Spot',
    'Tomato_Spider_mites_Two_spotted_spider_mite': 'Tomato Spider Mites (Two-Spotted)',
    'Tomato__Target_Spot': 'Tomato Target Spot',
    'Tomato__Tomato_YellowLeaf__Curl_Virus': 'Tomato Yellow Leaf Curl Virus',
    'Tomato__Tomato_mosaic_virus': 'Tomato Mosaic Virus',
    'Tomato_healthy': 'Tomato (Healthy)'
}


def get_model():
    """Return the loaded model"""
    return model

@login_required
def diagnose(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        
        # Handle webcam capture
        captured_image = request.POST.get('captured_image')
        
        # Check if neither file upload nor webcam capture was provided
        if not request.FILES.get('image') and not captured_image:
            messages.error(request, 'Please upload an image or capture one using the camera before diagnosing.')
            return render(request, 'upload.html', {'form': form})
        
        if captured_image and not request.FILES.get('image'):
            try:
                format, imgstr = captured_image.split(';base64,')
                ext = format.split('/')[-1]
                image_data = ContentFile(base64.b64decode(imgstr), name=f"captured_{uuid.uuid4()}.{ext}")
                
                diagnosis = Diagnosis(image=image_data, user=request.user)
                diagnosis.save()
            except Exception as e:
                logger.error(f"Error processing captured image: {str(e)}")
                messages.error(request, 'Error processing captured image. Please try again.')
                return render(request, 'upload.html', {'form': form})
                
        elif form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.user = request.user
            diagnosis.save()
        else: 
            return render(request, 'upload.html', {'form': form})   
            
        if diagnosis.image and diagnosis.image.name:
            image_path = diagnosis.image.path
            # Proceed with model prediction
        else:
            messages.error(request, "Please upload an image or capture one before diagnosing.")
            return redirect('diagnosis:diagnose')


        try:
            # Check if the image file exists
            if not hasattr(diagnosis.image, 'path') or not diagnosis.image.path:
                messages.error(request, 'Image file is invalid. Please try uploading again.')
                return render(request, 'upload.html', {'form': form})
                
            image_path = diagnosis.image.path
            
            # Verify the file actually exists
            if not os.path.exists(image_path):
                messages.error(request, 'Image file could not be found. Please try uploading again.')
                return render(request, 'upload.html', {'form': form})

            # Process the image
            img = keras_image.load_img(image_path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img)
            
            # Ensure proper data type
            img_array = img_array.astype('float32')
            
            # Use EfficientNet preprocessing
            img_array = preprocess_input(img_array)
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            # Debug logging
            logger.info(f"Image shape: {img_array.shape}, dtype: {img_array.dtype}")
            logger.info(f"Image min: {img_array.min():.3f}, max: {img_array.max():.3f}")

            model = get_model()
            
            # Get prediction
            prediction = model.predict(img_array)[0]

            # Get top 3 predictions
            top3_indices = np.argsort(prediction)[-3:][::-1]
            top3_predictions = [
                {
                    'label': DISEASE_CLASSES[idx],
                    'label_display': DISEASE_LABELS.get(DISEASE_CLASSES[idx], DISEASE_CLASSES[idx]),
                    'confidence': round(float(prediction[idx]) * 100, 2)
                }
                for idx in top3_indices
            ]

            # Primary prediction
            predicted_index = top3_indices[0]
            disease_name = DISEASE_CLASSES[predicted_index]
            confidence = top3_predictions[0]['confidence']  # use already computed

            diagnosis.disease_name = disease_name
            diagnosis.severity = "Unknown"
            diagnosis.affected_part = "Unknown"
            diagnosis.confidence = confidence
            diagnosis.save()

            
            # Generate AI recommendation
            try:
                create_ai_recommendation(diagnosis)
                messages.success(request, f'Diagnosis complete: {DISEASE_LABELS.get(disease_name, disease_name)}. AI recommendation generated!')
            except Exception as e:
                logger.error(f"Failed to generate AI recommendation: {str(e)}")
                messages.warning(request, f'Diagnosis complete: {DISEASE_LABELS.get(disease_name, disease_name)}. AI recommendation generation failed.')

            return render(request, 'results.html', {
                'diagnosis': diagnosis,
                'disease_label': DISEASE_LABELS.get(diagnosis.disease_name, diagnosis.disease_name),
                'top3': top3_predictions
            })

            
        except FileNotFoundError as e:
            logger.error(f"Model file not found: {str(e)}")
            messages.error(request, "The analysis model is currently unavailable. Please try again later.")
            return redirect('diagnosis:diagnose')
        except Exception as e:
            logger.error(f"Error during diagnosis: {str(e)}")
            messages.error(request, f'An unexpected error occurred during diagnosis. Please try again.')
            return redirect('diagnosis:diagnose')
    else:
        form = DiagnosisForm()
    
    return render(request, 'upload.html', {'form': form})



def create_ai_recommendation(diagnosis):
    """Create PURE AI-powered recommendation using APIs - NO HARDCODED CONTENT"""
    try:
        # 🌤️ Get live weather data optimized for AI
        weather_client = WeatherClient()
        city = diagnosis.location_context or "Kampala"
        
        logger.info(f"🌤️ Getting weather data for {city}")
        
        # 🔧 BETTER: Use the Gemini-optimized method
        weather_data = weather_client.get_weather_by_city_for_gemini(city, "UG")
        
        # Also get detailed weather for context
        coords = weather_client.get_coordinates_by_city(city, "UG")
        if coords:
            detailed_weather = weather_client.get_weather_by_coordinates(coords['lat'], coords['lon'])
        else:
            detailed_weather = None
        
        # 🤖 Generate AI recommendation using Gemini
        gemini_client = GeminiContentGenerator()
        
        # Prepare context for AI
        context = {
            'disease_name': diagnosis.disease_name,
            'disease_label': DISEASE_LABELS.get(diagnosis.disease_name, diagnosis.disease_name),
            'confidence': diagnosis.confidence,
            'weather': detailed_weather,
            'weather_for_ai': weather_data,  # [temp, humidity, pressure, wind_speed, visibility, description, cloudiness]
            'location': city,
            'crop_type': extract_crop_type(diagnosis.disease_name),
            'affected_part': diagnosis.affected_part,
            'severity': diagnosis.severity
        }
        
        logger.info(f"🤖 Generating AI recommendation for {context['disease_label']}")
        
        # Generate comprehensive AI recommendation
        ai_recommendation = gemini_client.generate_comprehensive_recommendation(context)
        
        # 💾 Save PURE AI recommendation to database
        recommendation = Recommendation.objects.create(
            diagnosis=diagnosis,
            city=city,
            latitude=coords['lat'] if coords else None,
            longitude=coords['lon'] if coords else None,
            
            # Live weather data
            temperature=detailed_weather['temperature'] if detailed_weather else None,
            humidity=detailed_weather['humidity'] if detailed_weather else None,
            pressure=detailed_weather['pressure'] if detailed_weather else None,
            wind_speed=detailed_weather['wind_speed'] if detailed_weather else None,
            weather_description=detailed_weather['description'] if detailed_weather else None,
            
            # Pure AI-generated content
            recommendation_json=json.dumps(ai_recommendation),
            treatment_summary=ai_recommendation.get('treatment_summary', ''),
            prevention_summary=ai_recommendation.get('prevention_summary', ''),
            
            is_active=True
        )
        
        logger.info(f"✅ Pure AI recommendation created for diagnosis {diagnosis.id}")
        return recommendation
    
    except Exception as e:
        logger.error(f"❌ Failed to create AI recommendation: {str(e)}")
        raise Exception(f"AI recommendation service unavailable: {str(e)}")

def extract_crop_type(disease_name):
    """Extract crop type from disease name"""
    if 'Tomato' in disease_name:
        return 'Tomato'
    elif 'Potato' in disease_name:
        return 'Potato'
    elif 'Apple' in disease_name:
        return 'Apple'
    elif 'Corn' in disease_name or 'maize' in disease_name:
        return 'Corn/Maize'
    elif 'Pepper' in disease_name:
        return 'Pepper'
    else:
        return 'General Crop'

@login_required
def diagnosis_history(request):
    diagnoses = Diagnosis.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'diagnoses': diagnoses})
