from django.shortcuts import render
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

def diagnose(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)
        if form.is_valid():
            diagnosis = form.save()
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
