# Rock Classification Model Training

This directory contains the Python code to train your rock classification model on the Kaggle dataset.

## Prerequisites

```bash
pip install tensorflow pillow numpy flask
```

## Files Structure

```
ml-training/
├── requirements.txt          # Python dependencies
├── train_model.py           # Training script
├── api.py                   # Flask API server
├── test_api.py              # Test the API locally
└── deploy_railway.md        # Deployment guide
```

## Quick Start

### 1. Prepare Your Dataset

Download your Rock Classification Dataset from Kaggle and organize it:

```
dataset/
├── train/
│   ├── granite/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   ├── limestone/
│   │   ├── img1.jpg
│   │   └── img2.jpg
│   └── basalt/
│       ├── img1.jpg
│       └── img2.jpg
```

### 2. Train the Model

```bash
python train_model.py --dataset ./dataset/train --epochs 20
```

This will create:
- `rock_classifier_model.h5` - Your trained model
- `class_names.json` - Rock type labels
- `training_history.png` - Training graphs

### 3. Test Locally

```bash
# Start the API server
python api.py

# In another terminal, test it
python test_api.py
```

### 4. Deploy to Cloud

Follow `deploy_railway.md` for Railway (free tier)
Or see `deploy_huggingface.md` for Hugging Face Spaces

### 5. Update Your Expo App

In your `.env` file:
```
EXPO_PUBLIC_AI_PROVIDER=custom
EXPO_PUBLIC_CUSTOM_MODEL_URL=https://your-app.railway.app
```
