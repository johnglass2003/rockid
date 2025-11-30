# Quick Start Guide - Train & Deploy Your Rock Classifier

## 📋 What You'll Need

1. **Your Kaggle Rock Dataset** - Downloaded and extracted
2. **Python 3.8+** installed
3. **A Railway or Render account** (free tier)

## 🚀 Step-by-Step Instructions

### Step 1: Set Up Python Environment (5 mins)

```bash
# Navigate to ml-training directory
cd ml-training

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Organize Your Dataset (5 mins)

Your Kaggle dataset should be structured like this:

```
dataset/
└── train/
    ├── granite/
    │   ├── image1.jpg
    │   ├── image2.jpg
    │   └── ...
    ├── basalt/
    │   ├── image1.jpg
    │   └── ...
    ├── limestone/
    └── ...
```

Each folder name = rock type name.

### Step 3: Train Your Model (30-60 mins)

```bash
python train_model.py --dataset ./dataset/train --epochs 20
```

**What happens:**
- Trains a MobileNetV2-based model (mobile-friendly)
- Uses data augmentation for better accuracy
- Saves best model automatically
- Creates `rock_classifier_model.h5` and `class_names.json`
- Generates training graphs

**Expected output:**
```
🪨 Starting Rock Classification Model Training...
✅ Found 10 rock classes:
   0: granite
   1: basalt
   ...
🏋️ Training model...
Epoch 1/20 ... val_accuracy: 0.85
...
✅ Model saved as 'rock_classifier_model.h5'
```

### Step 4: Test Locally (5 mins)

```bash
# Start the API server
python api.py

# In another terminal, test with a rock image
python test_api.py path/to/test_rock.jpg
```

**Expected output:**
```
✅ Rock Identified!
   Name: Granite
   Type: igneous
   Confidence: 94.5%
```

### Step 5: Deploy to Railway (10 mins)

#### Option A: GitHub Deploy (Easiest)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add rock classifier"
   git push
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo and `ml-training` folder
   - Railway auto-deploys! ✨

3. **Get your URL:**
   - Click "Settings" → "Domains" → "Generate Domain"
   - Copy: `https://your-app.railway.app`

#### Option B: Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy from ml-training directory
railway init
railway up
```

### Step 6: Connect to Your Expo App (2 mins)

1. **Create `.env` file** in `rock-id` directory:
   ```bash
   EXPO_PUBLIC_AI_PROVIDER=custom
   EXPO_PUBLIC_CUSTOM_MODEL_URL=https://your-app.railway.app
   ```

2. **Test it!**
   - Open your Expo app
   - Go to Scan tab
   - Take a rock picture
   - Watch it identify! 🎉

## 📊 Expected Accuracy

- **With good dataset:** 85-95% accuracy
- **Training time:** 30-60 minutes (depends on dataset size)
- **API response time:** 1-3 seconds per image

## 🎯 Tips for Better Results

1. **More training data = better accuracy**
   - Aim for 100+ images per rock type
   
2. **Diverse images**
   - Different lighting
   - Different angles
   - Various backgrounds

3. **Clean labels**
   - Make sure folders are named correctly
   - Remove misclassified images

4. **Monitor training**
   - Watch `training_history.png` for overfitting
   - If validation accuracy plateaus, stop early

## 🐛 Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Out of memory" during training:**
```bash
# Reduce batch size
python train_model.py --dataset ./dataset/train --batch-size 16
```

**Model too large for Railway:**
- Use Hugging Face Spaces instead (see deploy_huggingface.md)
- Or compress model with quantization

**API is slow:**
- Normal for first request (cold start)
- Consider Railway Pro ($5/month) for always-warm instances
- Or use Render/Hugging Face

## 🎓 Next Steps

Once working:
1. **Collect user feedback** - save misidentified rocks
2. **Retrain periodically** with new data
3. **Add more rock types** as needed
4. **Consider on-device model** for offline use (TensorFlow Lite)

## 💰 Cost Breakdown

- **Railway Free Tier:** $5 free credit/month, then $0.000463/GB-hour
- **Render Free Tier:** Free forever, but may sleep
- **Hugging Face Spaces:** Free forever with GPU!

**Recommendation:** Start with Railway, move to Hugging Face if you need more power.

---

**Need help?** Check the README files in each directory for more details!
