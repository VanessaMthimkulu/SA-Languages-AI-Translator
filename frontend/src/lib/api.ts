/**
 * API client for backend communication
 */
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Translate text to a South African language
 */
export async function translateText(
  text: string,
  targetLanguage: string,
  token: string
) {
  const response = await apiClient.post(
    "/translate",
    {
      text,
      target_language: targetLanguage,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data;
}

/**
 * Generate text-to-speech audio
 */
export async function generateSpeech(
  text: string,
  language: string,
  token: string
) {
  const response = await apiClient.post(
    "/tts",
    {
      text,
      language,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data;
}

/**
 * Save translation to history
 */
export async function saveHistory(
  originalText: string,
  translatedText: string,
  targetLanguage: string,
  token: string,
  audioUrl?: string
) {
  const response = await apiClient.post(
    "/history/save",
    {
      original_text: originalText,
      translated_text: translatedText,
      target_language: targetLanguage,
      audio_url: audioUrl,
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  );
  return response.data;
}

/**
 * Get translation history with pagination
 */
export async function getHistory(
  token: string,
  limit: number = 20,
  offset: number = 0
) {
  const response = await apiClient.get("/history/get", {
    params: { limit, offset },
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}

/**
 * Delete a history item
 */
export async function deleteHistory(historyId: string, token: string) {
  const response = await apiClient.delete(`/history/delete/${historyId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
}
