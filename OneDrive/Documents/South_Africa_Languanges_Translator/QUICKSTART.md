# Quick Start Guide

Get the SA Languages Translator running in 5 minutes!

## Prerequisites Check

Make sure you have:
- ✅ Python 3.11+ installed (`python --version`)
- ✅ Node.js 18+ installed (`node --version`)
- ✅ npm installed (`npm --version`)

## Step 1: Database Setup (2 minutes)

1. Go to your Supabase project: https://supabase.com/dashboard/project/dkjfrxtlwkjnxtkrpynp
2. Click "SQL Editor" in the left sidebar
3. Copy the contents of `supabase-schema.sql`
4. Paste and click "Run"
5. Verify the `translation_history` table appears in "Table Editor"

## Step 2: Start Backend (1 minute)

Open a terminal:

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

✅ Backend running at http://localhost:8000

## Step 3: Start Frontend (1 minute)

Open a NEW terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ Frontend running at http://localhost:3000

## Step 4: Test the App (1 minute)

1. Open http://localhost:3000 in your browser
2. Click "Sign Up"
3. Enter email and password (or use Google)
4. Enter English text: "Hello, how are you?"
5. Select language: "isiZulu"
6. Click "Translate & Speak"
7. See translation and click play button for audio!

## Troubleshooting

### Backend won't start

**Error: "No module named 'fastapi'"**
```bash
# Make sure venv is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall
pip install -r requirements.txt
```

**Error: "Port 8000 already in use"**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001

# Update frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "Environment variables not found"**
- Check `frontend/.env.local` exists
- Restart dev server after creating .env.local

### Translation fails

**"Invalid or expired token"**
- Log out and log back in
- Check Supabase project is active

**"Translation failed"**
- Verify Gemini API key in `backend/.env`
- Check API quota at https://makersuite.google.com

**"TTS generation failed"**
- Verify ElevenLabs API key in `backend/.env`
- Check free tier limits (10k chars/month)

## What's Next?

- ✅ App is running locally
- 📖 Read [SETUP.md](SETUP.md) for detailed setup
- 🏗️ Read [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) to understand the code
- 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) to deploy to Railway
- 🎨 Customize the UI in `frontend/src/components/`
- 🔧 Add features in `backend/app/routes/`

## Quick Commands Reference

### Backend
```bash
cd backend
venv\Scripts\activate          # Activate venv (Windows)
source venv/bin/activate       # Activate venv (Mac/Linux)
uvicorn app.main:app --reload  # Start server
deactivate                     # Deactivate venv
```

### Frontend
```bash
cd frontend
npm run dev    # Start dev server
npm run build  # Build for production
npm start      # Start production server
npm run lint   # Run linter
```

### Database
```bash
# View API docs
http://localhost:8000/docs

# Check health
http://localhost:8000/health
```

## Support

Having issues? Check:
1. Terminal error messages
2. Browser console (F12)
3. Backend logs in terminal
4. [SETUP.md](SETUP.md) for detailed troubleshooting

## Success Checklist

- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Can sign up/login
- ✅ Can translate text
- ✅ Can hear audio
- ✅ Can view history

Congratulations! Your SA Languages Translator is running! 🎉
