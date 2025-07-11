from django.shortcuts import render
from .forms import DiagnosisForm
from .models import Diagnosis

import base64
import uuid  # 🔧 NEW: for generating unique image filenames
from django.core.files.base import ContentFile

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image as keras_image  # type: ignore
import os

# Load the model once globally
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'diagnosis', 'model', 'newresult.h5')
model = tf.keras.models.load_model(MODEL_PATH)

# Replace with your actual class names
DISEASE_CLASSES = [
    'Tomato_Tomato_YellowLeaf_Curl_Virus',
    'Tomato_Bacterial_spot',
    'Apple___Apple_scab',
    'Apple___healthy',
    'Apple___Black_rot',
    'Tomato_Late_blight',
    'Corn_(maize)_Northern_Leaf_Blight',
    'Corn_(maize)Common_rust',
    'Corn_(maize)_healthy',
    'Tomato_Septoria_leaf_spot',
    'Apple___Cedar_apple_rust',
    'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot',
    'Tomato_healthy',
    'Pepper_bell__healthy',
    'Tomato__Target_Spot',
    'Potato___Early_blight',
    'Potato___Late_blight',
    'Tomato_Early_blight',
    'Pepper_bell__Bacterial_spot',
    'Tomato_Leaf_Mold',
    'Tomato__Tomato_mosaic_virus',
    'Potato___healthy'
]

DISEASE_LABELS = {
    'Tomato_Tomato_YellowLeaf_Curl_Virus': 'Tomato Yellow Leaf Curl Virus',
    'Tomato_Bacterial_spot': 'Tomato Bacterial Spot',
    'Apple___Apple_scab': 'Apple Scab',
    'Apple___healthy': 'Apple (Healthy)',
    'Apple___Black_rot': 'Apple Black Rot',
    'Tomato_Late_blight': 'Tomato Late Blight',
    'Corn_(maize)_Northern_Leaf_Blight': 'Corn Northern Leaf Blight',
    'Corn_(maize)Common_rust': 'Corn Common Rust',
    'Corn_(maize)_healthy': 'Corn (Healthy)',
    'Tomato_Septoria_leaf_spot': 'Tomato Septoria Leaf Spot',
    'Apple___Cedar_apple_rust': 'Apple Cedar Apple Rust',
    'Tomato_Spider_mites_Two_spotted_spider_mite': 'Tomato Spider Mites (Two-Spotted)',
    'Corn_(maize)_Cercospora_leaf_spot Gray_leaf_spot': 'Corn Gray Leaf Spot',
    'Tomato_healthy': 'Tomato (Healthy)',
    'Pepper_bell__healthy': 'Pepper Bell (Healthy)',
    'Tomato__Target_Spot': 'Tomato Target Spot',
    'Potato___Early_blight': 'Potato Early Blight',
    'Potato___Late_blight': 'Potato Late Blight',
    'Tomato_Early_blight': 'Tomato Early Blight',
    'Pepper_bell__Bacterial_spot': 'Pepper Bell Bacterial Spot',
    'Tomato_Leaf_Mold': 'Tomato Leaf Mold',
    'Tomato__Tomato_mosaic_virus': 'Tomato Mosaic Virus',
    'Potato___healthy': 'Potato (Healthy)'
}


def diagnose(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST, request.FILES)

        # 🔧 NEW: handle base64 webcam image (if present)
        captured_image = request.POST.get('captured_image')
        if captured_image and not request.FILES.get('image'):
            format, imgstr = captured_image.split(';base64,')  # data:image/png;base64,...
            ext = format.split('/')[-1]  # Get extension
            image_data = ContentFile(base64.b64decode(imgstr), name=f"captured_{uuid.uuid4()}.{ext}")

            # Create a new Diagnosis object
            diagnosis = Diagnosis(image=image_data)
            diagnosis.save()
        elif form.is_valid():
            diagnosis = form.save()
        else:
            return render(request, 'upload.html', {'form': form})

        # 🔍 Common image processing and prediction
        image_path = diagnosis.image.path
        img = keras_image.load_img(image_path, target_size=(224, 224))
        img_array = keras_image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0]
        predicted_index = np.argmax(prediction)
        disease_name = DISEASE_CLASSES[predicted_index]
        confidence = float(np.max(prediction))

        diagnosis.disease_name = disease_name
        diagnosis.severity = "Unknown"
        diagnosis.affected_part = "Unknown"
        diagnosis.confidence = round(confidence * 100, 1)
        diagnosis.save()

        return render(request, 'results.html', {
        'diagnosis': diagnosis,
        'disease_label': DISEASE_LABELS.get(diagnosis.disease_name, diagnosis.disease_name)
     })
    else:
        form = DiagnosisForm()

    return render(request, 'upload.html', {'form': form})


def diagnosis_history(request):
    diagnoses = Diagnosis.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'diagnoses': diagnoses})
