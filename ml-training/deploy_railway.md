# Deploying to Railway (Free Tier)

Railway offers a free tier perfect for deploying your rock classification API.

## Prerequisites

- Trained model files: `rock_classifier_model.h5` and `class_names.json`
- Railway account (sign up at https://railway.app with GitHub)

## Step-by-Step Deployment

### 1. Create Required Files

Create `Procfile` in the `ml-training` directory:

```
web: gunicorn api:app
```

Create `.railwayignore`:

```
*.png
__pycache__/
*.pyc
dataset/
*.md
test_api.py
train_model.py
```

### 2. Initialize Git (if not already done)

```bash
cd ml-training
git init
git add .
git commit -m "Initial commit - rock classification API"
```

### 3. Deploy to Railway

#### Option A: Deploy from GitHub

1. Push your code to GitHub
2. Go to https://railway.app
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy

#### Option B: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### 4. Configure Environment

Railway will automatically:
- Detect `requirements.txt`
- Install dependencies
- Run the Procfile command

### 5. Get Your API URL

After deployment, Railway provides a URL like:
```
https://your-app-name.railway.app
```

### 6. Test Your Deployed API

```bash
curl https://your-app-name.railway.app/
```

### 7. Update Your Expo App

In `.env`:
```
EXPO_PUBLIC_AI_PROVIDER=custom
EXPO_PUBLIC_CUSTOM_MODEL_URL=https://your-app-name.railway.app
```

## Troubleshooting

### Build Fails - Model Too Large

If your model file is too large (>500MB), use Railway Volumes:

1. In Railway dashboard → Settings → Volumes
2. Mount volume at `/app/models`
3. Upload model separately using Railway CLI

### Cold Starts

Free tier may have cold starts (10-30 seconds). Consider:
- Upgrading to Railway Pro ($5/month)
- Or using Hugging Face Spaces (always warm)

## Alternative: Deploy to Render

Render also has a free tier:

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn api:app`

## Alternative: Deploy to Hugging Face Spaces

See `deploy_huggingface.md` for GPU-accelerated inference (free).
