# Deployment Guide for Railway

This guide will help you deploy the SA Translator app to Railway.

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. GitHub repository with your code
3. Supabase project set up with the schema
4. API keys for Gemini and ElevenLabs

## Step-by-Step Deployment

### 1. Prepare Your Repository

Make sure all code is committed to your GitHub repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Create Railway Project

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Select your repository
4. Railway will detect your project

### 3. Configure Backend Service

1. In Railway dashboard, click "New Service"
2. Select your repository
3. Set the following:
   - **Name**: `sa-translator-backend`
   - **Root Directory**: `/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. Add environment variables:
   ```
   SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
   SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
   GEMINI_API_KEY=AIzaSyAhGlyQuRebN3zOgJQIaE4Nz5WxGHqlxQo
   ELEVENLABS_API_KEY=sk_dc81cf21bc407491202c704ae38552aa4eae4803970c890f
   ```

5. Deploy the service

### 4. Configure Frontend Service

1. Click "New Service" again
2. Select your repository
3. Set the following:
   - **Name**: `sa-translator-frontend`
   - **Root Directory**: `/frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`

4. Add environment variables:
   ```
   NEXT_PUBLIC_SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
   NEXT_PUBLIC_API_URL=<your-backend-railway-url>
   ```

   Note: Replace `<your-backend-railway-url>` with the URL from your backend service

5. Deploy the service

### 5. Update CORS Settings

After deployment, update the backend CORS settings:

1. Go to backend service settings
2. Add your frontend URL to `ALLOWED_ORIGINS` in `backend/app/config.py`
3. Redeploy backend service

### 6. Configure Supabase

1. Go to your Supabase project dashboard
2. Navigate to Authentication > URL Configuration
3. Add your Railway frontend URL to:
   - Site URL
   - Redirect URLs

### 7. Test Your Deployment

1. Visit your frontend Railway URL
2. Sign up with email or Google
3. Test translation functionality
4. Check history page

## Environment Variables Reference

### Backend Variables

| Variable | Description | Required |
|----------|-------------|----------|
| SUPABASE_URL | Your Supabase project URL | Yes |
| SUPABASE_ANON_KEY | Supabase anonymous key | Yes |
| GEMINI_API_KEY | Google Gemini API key | Yes |
| ELEVENLABS_API_KEY | ElevenLabs API key | Yes |
| PORT | Port number (auto-set by Railway) | No |

### Frontend Variables

| Variable | Description | Required |
|----------|-------------|----------|
| NEXT_PUBLIC_SUPABASE_URL | Your Supabase project URL | Yes |
| NEXT_PUBLIC_SUPABASE_ANON_KEY | Supabase anonymous key | Yes |
| NEXT_PUBLIC_API_URL | Backend API URL | Yes |

## Troubleshooting

### Backend won't start
- Check logs in Railway dashboard
- Verify all environment variables are set
- Ensure Python version is 3.11+

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running

### Authentication fails
- Verify Supabase URLs are correct
- Check redirect URLs in Supabase dashboard
- Ensure Google OAuth is configured in Supabase

### Translation fails
- Verify Gemini API key is valid
- Check API quota limits
- Review backend logs for errors

### TTS fails
- Verify ElevenLabs API key is valid
- Check API quota limits
- Ensure voice IDs are correct

## Monitoring

Railway provides built-in monitoring:
- View logs in real-time
- Monitor resource usage
- Set up alerts for errors

## Scaling

Railway automatically scales based on traffic. For high-traffic scenarios:
1. Upgrade to Railway Pro plan
2. Enable auto-scaling
3. Consider adding Redis for caching

## Cost Optimization

To stay on free tier:
- Monitor API usage (Gemini, ElevenLabs)
- Implement rate limiting
- Cache translations when possible
- Use Supabase free tier limits wisely

## Support

For issues:
- Check Railway documentation: https://docs.railway.app
- Review application logs
- Check Supabase status: https://status.supabase.com
- Verify API key validity
