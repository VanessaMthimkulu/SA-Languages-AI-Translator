-- Supabase Database Schema for SA Translator App
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Translation History Table
CREATE TABLE IF NOT EXISTS translation_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    target_language VARCHAR(50) NOT NULL,
    audio_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries by user_id
CREATE INDEX IF NOT EXISTS idx_translation_history_user_id 
ON translation_history(user_id);

-- Create index for sorting by created_at
CREATE INDEX IF NOT EXISTS idx_translation_history_created_at 
ON translation_history(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE translation_history ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read their own translation history
CREATE POLICY "Users can view own history" 
ON translation_history
FOR SELECT
USING (auth.uid() = user_id);

-- Policy: Users can only insert their own translations
CREATE POLICY "Users can insert own translations" 
ON translation_history
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Policy: Users can delete their own translations
CREATE POLICY "Users can delete own translations" 
ON translation_history
FOR DELETE
USING (auth.uid() = user_id);

-- Optional: Create a view for recent translations
CREATE OR REPLACE VIEW recent_translations AS
SELECT 
    id,
    user_id,
    original_text,
    translated_text,
    target_language,
    created_at
FROM translation_history
ORDER BY created_at DESC
LIMIT 100;

-- Grant access to authenticated users
GRANT SELECT ON recent_translations TO authenticated;
