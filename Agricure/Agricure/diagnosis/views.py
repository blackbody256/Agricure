from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DiagnosisForm
from .models import Diagnosis

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image # type: ignore
import os

# Load the model once globally
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'diagnosis', 'model', 'newresult.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Replace with your actual class names
DISEASE_CLASSES = [
    'Healthy', 'Late Blight', 'Rust', 'Bacterial Spot', 'Early Blight',
    'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites', 'Target Spot',
    'Mosaic Virus', 'Yellow Leaf Curl', 'Powdery Mildew', 'Wilt',
    'Anthracnose', 'Downy Mildew', 'Canker', 'Fusarium', 'Alternaria',
    'Black Rot', 'Scab', 'Smut', 'Mold', 'Other'
]

@login_required
def diagnose(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save(commit=False)
            diagnosis.user = request.user  # Add this line
            diagnosis.save()
            
            image_path = diagnosis.image.path

            # Load and preprocess image
            img = keras_image.load_img(image_path, target_size=(224, 224))
            img_array = keras_image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            prediction = model.predict(img_array)[0]
            predicted_index = np.argmax(prediction)
            disease_name = DISEASE_CLASSES[predicted_index]
            confidence = float(np.max(prediction))

            # Save prediction to DB
            diagnosis.disease_name = disease_name
            diagnosis.severity = "Unknown"        
            diagnosis.affected_part = "Unknown"    
            diagnosis.confidence = round(confidence * 100, 1)
   
            diagnosis.save()

            return render(request, 'results.html', {'diagnosis': diagnosis})
    else:
        form = DiagnosisForm()

    return render(request, 'upload.html', {'form': form})

@login_required
def diagnosis_history(request):
    diagnoses = Diagnosis.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'diagnoses': diagnoses})
