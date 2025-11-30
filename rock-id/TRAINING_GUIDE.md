# Training Your Custom Rock Classification Model

## Quick Start (Using Kaggle Dataset)

### Step 1: Train the Model (Python)

```python
# train_rock_classifier.py
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load your Kaggle rock dataset
# Assuming structure: dataset/train/{rock_class_name}/image.jpg

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'dataset/train',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Build model (MobileNetV2 for mobile deployment)
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=20
)

# Save model
model.save('rock_classifier_model.h5')
# Save class names
import json
class_names = list(train_generator.class_indices.keys())
with open('class_names.json', 'w') as f:
    json.dump(class_names, f)
```

### Step 2: Deploy Options

#### Option A: Deploy to Hugging Face (FREE)

```python
# Convert to ONNX for web deployment
import tf2onnx
import onnx

spec = (tf.TensorSpec((None, 224, 224, 3), tf.float32, name="input"),)
output_path = "rock_classifier.onnx"

model_proto, _ = tf2onnx.convert.from_keras(model, input_signature=spec, opset=13, output_path=output_path)

# Upload to Hugging Face Spaces - create a simple API
```

#### Option B: Deploy to Flask API (Self-hosted)

```python
# api.py
from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from PIL import Image
import json

app = Flask(__name__)

model = tf.keras.models.load_model('rock_classifier_model.h5')
with open('class_names.json', 'r') as f:
    class_names = json.load(f)

@app.route('/identify', methods=['POST'])
def identify():
    file = request.files['image']
    img = Image.open(file).resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions = model.predict(img_array)
    class_idx = np.argmax(predictions[0])
    confidence = float(predictions[0][class_idx]) * 100
    
    return jsonify({
        'name': class_names[class_idx],
        'type': 'sedimentary',  # You can add logic to map classes to types
        'confidence': confidence,
        'description': f'Identified as {class_names[class_idx]}',
        'minerals': []
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Deploy to Railway, Render, or Google Cloud Run.

#### Option C: Convert to TensorFlow Lite (On-Device)

```python
# Convert to TFLite for mobile
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('rock_classifier.tflite', 'wb') as f:
    f.write(tflite_model)
```

Then use with `@tensorflow/tfjs-react-native` or `react-native-pytorch-core`.

### Step 3: Update Your App

Once deployed, update the `.env` file:

```env
EXPO_PUBLIC_AI_PROVIDER=custom
EXPO_PUBLIC_CUSTOM_MODEL_URL=https://your-api.com
```

## Recommended Approach

1. **Start with Gemini API** (free tier, no training needed)
2. **Train custom model** when you want specific rock types
3. **Deploy to cloud API** (Railway/Render/HuggingFace)
4. **Later: Convert to on-device** if you need offline support

## Get Free Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Create API key (free tier: 15 requests/minute)
3. Add to `.env`: `EXPO_PUBLIC_GEMINI_API_KEY=your_key_here`

This gives you immediate rock identification without training!
