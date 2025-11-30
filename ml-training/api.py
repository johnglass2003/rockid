"""
Flask API Server for Rock Classification
Serves the trained TensorFlow model
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import io
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React Native

# Load model and class names
MODEL_PATH = 'rock_classifier_model.h5'
CLASS_NAMES_PATH = 'class_names.json'

print("🚀 Loading rock classification model...")
model = tf.keras.models.load_model(MODEL_PATH)
print("✅ Model loaded successfully")

with open(CLASS_NAMES_PATH, 'r') as f:
    class_names_dict = json.load(f)
    # Convert string keys to int and sort
    class_names = [class_names_dict[str(i)] for i in range(len(class_names_dict))]

print(f"✅ Loaded {len(class_names)} rock classes: {', '.join(class_names)}")

# Rock type mapping (customize based on your dataset)
ROCK_TYPE_MAPPING = {
    'granite': 'igneous',
    'basalt': 'igneous',
    'obsidian': 'igneous',
    'pumice': 'igneous',
    'limestone': 'sedimentary',
    'sandstone': 'sedimentary',
    'shale': 'sedimentary',
    'conglomerate': 'sedimentary',
    'marble': 'metamorphic',
    'slate': 'metamorphic',
    'gneiss': 'metamorphic',
    'schist': 'metamorphic',
}

MINERAL_MAPPING = {
    'granite': ['quartz', 'feldspar', 'mica'],
    'basalt': ['pyroxene', 'plagioclase', 'olivine'],
    'limestone': ['calcite'],
    'marble': ['calcite', 'dolomite'],
    'sandstone': ['quartz'],
}

def preprocess_image(image_bytes, target_size=(224, 224)):
    """Preprocess image for model prediction"""
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize
    img = img.resize(target_size)
    
    # Convert to array and normalize
    img_array = np.array(img) / 255.0
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def get_rock_type(rock_name):
    """Get rock type from name"""
    rock_lower = rock_name.lower()
    for key, value in ROCK_TYPE_MAPPING.items():
        if key in rock_lower:
            return value
    return 'unknown'

def get_minerals(rock_name):
    """Get common minerals for rock type"""
    rock_lower = rock_name.lower()
    for key, value in MINERAL_MAPPING.items():
        if key in rock_lower:
            return value
    return []

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'model': 'rock_classifier',
        'classes': len(class_names),
        'version': '1.0.0'
    })

@app.route('/identify', methods=['POST'])
def identify():
    """Rock identification endpoint"""
    try:
        # Check if image is in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Read and preprocess image
        image_bytes = file.read()
        img_array = preprocess_image(image_bytes)
        
        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Get top prediction
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx]) * 100
        rock_name = class_names[class_idx]
        
        # Get top 3 predictions
        top_3_idx = np.argsort(predictions[0])[-3:][::-1]
        top_3 = [
            {
                'name': class_names[i],
                'confidence': float(predictions[0][i]) * 100
            }
            for i in top_3_idx
        ]
        
        # Build response
        response = {
            'name': rock_name.title(),
            'type': get_rock_type(rock_name),
            'confidence': round(confidence, 2),
            'description': f'This appears to be {rock_name}. Confidence: {confidence:.1f}%',
            'minerals': get_minerals(rock_name),
            'top_3_predictions': top_3
        }
        
        print(f"✅ Identified: {rock_name} ({confidence:.1f}%)")
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/classes', methods=['GET'])
def get_classes():
    """Get all available rock classes"""
    return jsonify({
        'classes': class_names,
        'count': len(class_names)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
