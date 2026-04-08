# Project Structure

Complete overview of the SA Languages Translator project architecture.

## Directory Tree

```
sa-translator/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py        # Package initializer
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── config.py          # Configuration and settings
│   │   ├── routes/            # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── translate.py  # Translation endpoints
│   │   │   ├── tts.py         # Text-to-speech endpoints
│   │   │   └── history.py     # History CRUD endpoints
│   │   └── services/          # Business logic services
│   │       ├── __init__.py
│   │       ├── supabase_client.py      # Supabase integration
│   │       ├── auth_middleware.py      # JWT verification
│   │       ├── gemini_service.py       # Google Gemini API
│   │       └── elevenlabs_service.py   # ElevenLabs TTS API
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   ├── .gitignore            # Git ignore rules
│   └── Procfile              # Railway deployment config
│
├── frontend/                  # Next.js React frontend
│   ├── src/
│   │   ├── app/              # Next.js 14 app router
│   │   │   ├── layout.tsx    # Root layout
│   │   │   ├── page.tsx      # Home page (router)
│   │   │   └── globals.css   # Global styles
│   │   ├── components/       # React components
│   │   │   ├── AuthPage.tsx          # Login/signup page
│   │   │   ├── TranslatorPage.tsx    # Main app layout
│   │   │   ├── TranslatorPanel.tsx   # Translation interface
│   │   │   └── HistoryPanel.tsx      # History display
│   │   └── lib/              # Utilities and clients
│   │       ├── supabase.ts   # Supabase client config
│   │       └── api.ts        # Backend API client
│   ├── package.json          # Node dependencies
│   ├── tsconfig.json         # TypeScript config
│   ├── tailwind.config.ts    # TailwindCSS config
│   ├── postcss.config.js     # PostCSS config
│   ├── next.config.js        # Next.js config
│   ├── .env.local.example    # Environment template
│   └── .gitignore            # Git ignore rules
│
├── supabase-schema.sql       # Database schema
├── README.md                 # Project overview
├── SETUP.md                  # Setup instructions
├── DEPLOYMENT.md             # Deployment guide
├── PROJECT_STRUCTURE.md      # This file
├── railway.json              # Railway config
└── .gitignore                # Root git ignore
```

## Backend Architecture

### Main Application (`app/main.py`)
- FastAPI application initialization
- CORS middleware configuration
- Route registration
- Health check endpoints

### Configuration (`app/config.py`)
- Environment variable loading
- Application settings
- Supported languages definition
- CORS origins configuration

### Routes (`app/routes/`)

**auth.py**
- `POST /auth/verify` - Verify JWT token
- Extracts and validates Supabase tokens
- Returns user information

**translate.py**
- `POST /translate` - Translate text
- Validates input and language
- Calls Gemini API
- Returns translated text

**tts.py**
- `POST /tts` - Generate speech
- Converts text to audio
- Calls ElevenLabs API
- Returns base64 encoded MP3

**history.py**
- `POST /history/save` - Save translation
- `GET /history/get` - Retrieve history (paginated)
- `DELETE /history/delete/{id}` - Delete item
- All protected by authentication

### Services (`app/services/`)

**supabase_client.py**
- Supabase client initialization
- JWT token verification
- User information retrieval

**auth_middleware.py**
- FastAPI dependency for auth
- Extracts Bearer token from headers
- Validates token with Supabase
- Returns user context

**gemini_service.py**
- Google Gemini API integration
- Translation prompt engineering
- Error handling and retries
- Context-aware translation

**elevenlabs_service.py**
- ElevenLabs API integration
- Voice selection by language
- Audio generation
- MP3 format output

## Frontend Architecture

### App Router (`src/app/`)

**page.tsx**
- Main entry point
- Session management
- Routes between auth and translator
- Loading states

**layout.tsx**
- Root layout wrapper
- Global styles import
- Metadata configuration

### Components (`src/components/`)

**AuthPage.tsx**
- Email/password authentication
- Google OAuth integration
- Login/signup toggle
- Error handling

**TranslatorPage.tsx**
- Main app layout
- Tab navigation (Translate/History)
- Header with user info
- Logout functionality

**TranslatorPanel.tsx**
- Text input area
- Language selection dropdown
- Translation trigger
- Output display with audio player
- Character counter

**HistoryPanel.tsx**
- Translation history list
- Pagination support
- Delete functionality
- Date formatting
- Empty state handling

### Libraries (`src/lib/`)

**supabase.ts**
- Supabase client configuration
- Authentication helpers
- Session management

**api.ts**
- Axios client setup
- API endpoint functions
- Token injection
- Error handling

## Data Flow

### Translation Flow

1. User enters text in `TranslatorPanel`
2. User selects target language
3. User clicks "Translate & Speak"
4. Frontend calls `translateText()` from `api.ts`
5. Backend `/translate` endpoint receives request
6. `auth_middleware` verifies JWT token
7. `gemini_service` translates text
8. Backend calls `/tts` endpoint
9. `elevenlabs_service` generates audio
10. Backend saves to history via Supabase
11. Frontend receives translation + audio
12. Audio plays in browser
13. History refreshes

### Authentication Flow

1. User enters credentials in `AuthPage`
2. Supabase handles authentication
3. JWT token stored in session
4. Token sent with all API requests
5. Backend verifies token on each request
6. User context available in all routes

### History Flow

1. User navigates to History tab
2. Frontend calls `getHistory()` from `api.ts`
3. Backend queries Supabase with RLS
4. Results filtered by user_id
5. Paginated results returned
6. Frontend displays in `HistoryPanel`
7. User can delete items
8. Changes reflected immediately

## Database Schema

### translation_history Table

```sql
id              UUID PRIMARY KEY
user_id         UUID REFERENCES auth.users
original_text   TEXT
translated_text TEXT
target_language VARCHAR(50)
audio_url       TEXT (optional)
created_at      TIMESTAMP
```

### Row Level Security (RLS)

- Users can only see their own translations
- Users can only insert their own translations
- Users can only delete their own translations

## API Endpoints

### Authentication
- `POST /auth/verify` - Verify token

### Translation
- `POST /translate` - Translate text
  - Body: `{text, target_language}`
  - Returns: `{original_text, translated_text, target_language}`

### Text-to-Speech
- `POST /tts` - Generate audio
  - Body: `{text, language}`
  - Returns: `{audio: base64, format: "mp3"}`

### History
- `POST /history/save` - Save translation
  - Body: `{original_text, translated_text, target_language, audio_url?}`
- `GET /history/get?limit=20&offset=0` - Get history
  - Returns: `{history: [], count, limit, offset}`
- `DELETE /history/delete/{id}` - Delete item

## Environment Variables

### Backend
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_ANON_KEY` - Supabase anonymous key
- `GEMINI_API_KEY` - Google Gemini API key
- `ELEVENLABS_API_KEY` - ElevenLabs API key

### Frontend
- `NEXT_PUBLIC_SUPABASE_URL` - Supabase project URL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` - Supabase anonymous key
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Supabase** - Auth and database
- **Google Gemini** - AI translation
- **ElevenLabs** - Text-to-speech
- **httpx** - Async HTTP client
- **python-dotenv** - Environment management

### Frontend
- **Next.js 14** - React framework
- **React 18** - UI library
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Supabase JS** - Auth client
- **Axios** - HTTP client

## Security Features

1. **JWT Authentication** - All routes protected
2. **Row Level Security** - Database-level access control
3. **CORS Configuration** - Restricted origins
4. **Environment Variables** - Secrets not in code
5. **Input Validation** - Pydantic models
6. **SQL Injection Protection** - Supabase ORM
7. **XSS Protection** - React escaping

## Performance Optimizations

1. **Async/Await** - Non-blocking I/O
2. **Connection Pooling** - Reused connections
3. **Pagination** - Limited result sets
4. **Base64 Audio** - No file storage needed
5. **Client-side Caching** - React state management
6. **Hot Reload** - Fast development

## Deployment

- **Railway** - Monorepo deployment
- **Separate Services** - Frontend and backend
- **Environment Variables** - Per-service config
- **Auto-scaling** - Based on traffic
- **Free Tier** - Cost-effective hosting

## Future Enhancements

1. Audio file storage in Supabase Storage
2. Batch translation support
3. Translation quality feedback
4. Custom voice selection
5. Offline mode with service workers
6. Mobile app (React Native)
7. Translation caching
8. Rate limiting
9. Analytics dashboard
10. Multi-language UI
