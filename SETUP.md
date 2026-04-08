# Setup Guide - SA Languages Translator

Complete setup instructions for local development.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- Supabase account
- Google Gemini API key
- ElevenLabs API key

## 1. Clone Repository

```bash
git clone <your-repo-url>
cd sa-translator
```

## 2. Supabase Setup

### Create Supabase Project

1. Go to https://supabase.com
2. Create a new project
3. Wait for project to be ready

### Run Database Schema

1. Go to SQL Editor in Supabase dashboard
2. Copy contents of `supabase-schema.sql`
3. Run the SQL script
4. Verify `translation_history` table is created

### Configure Authentication

1. Go to Authentication > Providers
2. Enable Email provider
3. Enable Google provider:
   - Get OAuth credentials from Google Cloud Console
   - Add Client ID and Secret to Supabase
4. Go to Authentication > URL Configuration
5. Add `http://localhost:3000` to Site URL and Redirect URLs

### Get API Keys

1. Go to Settings > API
2. Copy:
   - Project URL (SUPABASE_URL)
   - anon/public key (SUPABASE_ANON_KEY)

## 3. Get External API Keys

### Google Gemini API

1. Go to https://makersuite.google.com/app/apikey
2. Create API key
3. Copy the key (GEMINI_API_KEY)

### ElevenLabs API

1. Go to https://elevenlabs.io
2. Sign up for free account
3. Go to Profile > API Keys
4. Create new API key
5. Copy the key (ELEVENLABS_API_KEY)

## 4. Backend Setup

### Install Dependencies

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Configure Environment

Create `backend/.env`:

```env
SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
GEMINI_API_KEY=AIzaSyAhGlyQuRebN3zOgJQIaE4Nz5WxGHqlxQo
ELEVENLABS_API_KEY=sk_dc81cf21bc407491202c704ae38552aa4eae4803970c890f
```

### Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

### Test Backend

Visit http://localhost:8000/docs for API documentation

## 5. Frontend Setup

### Install Dependencies

```bash
cd frontend
npm install
```

### Configure Environment

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Run Frontend

```bash
npm run dev
```

Frontend will run on http://localhost:3000

## 6. Test the Application

1. Open http://localhost:3000
2. Sign up with email or Google
3. Enter English text
4. Select target language
5. Click "Translate & Speak"
6. Verify translation and audio work
7. Check history page

## Common Issues

### Backend Issues

**Import errors**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

**Port already in use**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Supabase connection fails**
- Verify SUPABASE_URL and SUPABASE_ANON_KEY
- Check internet connection
- Verify Supabase project is active

### Frontend Issues

**Module not found**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Environment variables not loading**
- Ensure file is named `.env.local` (not `.env`)
- Restart dev server after changing env vars
- Variables must start with `NEXT_PUBLIC_`

**CORS errors**
- Verify backend is running
- Check `NEXT_PUBLIC_API_URL` is correct
- Ensure CORS is configured in backend

### API Issues

**Gemini API errors**
- Verify API key is valid
- Check quota limits
- Ensure API is enabled in Google Cloud Console

**ElevenLabs API errors**
- Verify API key is valid
- Check free tier limits (10,000 characters/month)
- Try different voice IDs

**Supabase auth errors**
- Verify redirect URLs are configured
- Check email confirmation for new signups
- Ensure Google OAuth is properly configured

## Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- Backend: Changes to Python files auto-reload
- Frontend: Changes to React files auto-reload

### Debugging

**Backend:**
```python
# Add print statements
print(f"Debug: {variable}")

# Use Python debugger
import pdb; pdb.set_trace()
```

**Frontend:**
```javascript
// Use console.log
console.log('Debug:', variable);

// Use React DevTools browser extension
```

### Testing API Endpoints

Use the interactive API docs at http://localhost:8000/docs

Or use curl:
```bash
# Test translation
curl -X POST http://localhost:8000/translate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text":"Hello","target_language":"isizulu"}'
```

## Next Steps

1. Review code structure
2. Customize UI styling
3. Add more features
4. Deploy to Railway (see DEPLOYMENT.md)
5. Set up monitoring and analytics

## Support

For issues:
- Check error messages in browser console
- Review backend logs in terminal
- Verify all environment variables
- Check API quotas and limits
