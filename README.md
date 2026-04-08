# SA Languages AI Translator

A full-stack web application that translates English to 9 South African vernacular languages with text-to-speech capabilities.

## Features

- 🔐 User authentication (Email/Password + Google OAuth via Supabase)
- 🌍 Translation to 9 SA languages using Google Gemini API
- 🔊 Text-to-speech audio output via ElevenLabs
- 📝 Translation history storage per user
- 📱 Responsive TailwindCSS UI
- 🚀 Free-tier friendly deployment

## Supported Languages

- isiZulu
- isiXhosa
- Sesotho
- Setswana
- Sepedi
- siSwati
- Tshivenda
- Xitsonga
- Afrikaans

## Tech Stack

**Frontend:**
- Next.js 14 (React)
- TailwindCSS
- Supabase Auth Client

**Backend:**
- Python 3.11+
- FastAPI
- Google Gemini API
- ElevenLabs API
- Supabase (Auth + Database)

## Project Structure

```
sa-translator/
├── frontend/          # Next.js frontend
│   ├── src/
│   │   ├── app/      # App router pages
│   │   ├── components/
│   │   └── lib/      # Utilities
│   └── package.json
├── backend/          # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   └── services/
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Environment Variables

Create `.env` files in both frontend and backend directories:

**frontend/.env.local:**
```
NEXT_PUBLIC_SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**backend/.env:**
```
SUPABASE_URL=https://dkjfrxtlwkjnxtkrpynp.supabase.co
SUPABASE_ANON_KEY=sb_publishable_jU8S3UXYPIvXzS1fo6DslA_Uf1odGf5
GEMINI_API_KEY=AIzaSyAhGlyQuRebN3zOgJQIaE4Nz5WxGHqlxQo
ELEVENLABS_API_KEY=sk_dc81cf21bc407491202c704ae38552aa4eae4803970c890f
```

### 2. Database Setup

Run the SQL schema in your Supabase SQL editor (see `supabase-schema.sql`)

### 3. Local Development

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### 4. Railway Deployment

1. Create a new Railway project
2. Add two services: `backend` and `frontend`
3. Set root directory for backend: `/backend`
4. Set root directory for frontend: `/frontend`
5. Add environment variables to each service
6. Deploy!

**Backend Railway Settings:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Frontend Railway Settings:**
- Build Command: `npm install && npm run build`
- Start Command: `npm start`

## API Endpoints

- `POST /auth/verify` - Verify Supabase JWT token
- `POST /translate` - Translate text using Gemini
- `POST /tts` - Generate audio using ElevenLabs
- `POST /history/save` - Save translation to history
- `GET /history/get` - Retrieve user's translation history

## Usage

1. Sign up or log in with email/password or Google
2. Enter English text in the input box
3. Select target SA language from dropdown
4. Click "Translate & Speak"
5. View translated text and play audio
6. Access your translation history anytime

## Security Notes

- Never commit `.env` files
- API keys are server-side only
- All routes protected with Supabase auth
- CORS configured for production domains

## License

MIT
