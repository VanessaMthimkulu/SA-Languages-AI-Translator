"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, translate, tts, history

# Initialize FastAPI app
app = FastAPI(
    title="SA Languages Translator API",
    description="API for translating English to South African languages with TTS",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(translate.router, prefix="/translate", tags=["Translation"])
app.include_router(tts.router, prefix="/tts", tags=["Text-to-Speech"])
app.include_router(history.router, prefix="/history", tags=["History"])

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "SA Languages Translator API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
