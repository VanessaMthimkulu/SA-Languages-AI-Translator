"use client";

import { useState } from "react";
import { translateText, generateSpeech, saveHistory } from "@/lib/api";

/**
 * Translation panel with input, language selection, and output
 */
interface TranslatorPanelProps {
  session: any;
  onTranslationSaved?: () => void;
}

// Supported South African languages
const LANGUAGES = [
  { code: "isizulu", name: "isiZulu" },
  { code: "isixhosa", name: "isiXhosa" },
  { code: "sesotho", name: "Sesotho" },
  { code: "setswana", name: "Setswana" },
  { code: "sepedi", name: "Sepedi" },
  { code: "siswati", name: "siSwati" },
  { code: "tshivenda", name: "Tshivenda" },
  { code: "xitsonga", name: "Xitsonga" },
  { code: "afrikaans", name: "Afrikaans" },
];

export default function TranslatorPanel({ session, onTranslationSaved }: TranslatorPanelProps) {
  const [inputText, setInputText] = useState("");
  const [selectedLanguage, setSelectedLanguage] = useState("isizulu");
  const [translatedText, setTranslatedText] = useState("");
  const [audioData, setAudioData] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [audioLoading, setAudioLoading] = useState(false);
  const [error, setError] = useState("");

  // Handle translation only
  const handleTranslate = async () => {
    if (!inputText.trim()) {
      setError("Please enter text to translate");
      return;
    }

    setLoading(true);
    setError("");
    setTranslatedText("");
    setAudioData(null);

    try {
      const token = session?.access_token;

      if (!token) {
        throw new Error("Not authenticated");
      }

      // Translate text
      const translationResult = await translateText(
        inputText,
        selectedLanguage,
        token
      );
      
      setTranslatedText(translationResult.translated_text);

      // Try to save to history (don't fail if it doesn't work)
      try {
        await saveHistory(
          inputText,
          translationResult.translated_text,
          translationResult.target_language,
          token
        );
        onTranslationSaved?.();
      } catch (historyErr) {
        console.warn("Could not save to history:", historyErr);
        // Don't show error to user, translation still worked
      }

    } catch (err: any) {
      console.error("Translation error:", err);
      setError(err.response?.data?.detail || err.message || "Translation failed");
    } finally {
      setLoading(false);
    }
  };

  // Handle audio generation separately
  const handleGenerateAudio = async () => {
    if (!translatedText) {
      setError("Please translate text first");
      return;
    }

    setAudioLoading(true);
    setError("");

    try {
      const token = session?.access_token;

      if (!token) {
        throw new Error("Not authenticated");
      }

      const ttsResult = await generateSpeech(
        translatedText,
        selectedLanguage,
        token
      );
      
      setAudioData(ttsResult.audio);

    } catch (err: any) {
      console.error("TTS error:", err);
      setError(err.response?.data?.detail || err.message || "Audio generation failed");
    } finally {
      setAudioLoading(false);
    }
  };

  // Play audio from base64 data
  const playAudio = () => {
    if (!audioData) return;

    try {
      const audio = new Audio(`data:audio/mpeg;base64,${audioData}`);
      audio.play();
    } catch (err) {
      console.error("Audio playback error:", err);
      setError("Failed to play audio");
    }
  };

  return (
    <div className="grid lg:grid-cols-2 gap-6">
      {/* Input Panel */}
      <div className="bg-white rounded-2xl shadow-xl p-6 border-t-4 border-sa-green">
        <h2 className="text-xl font-semibold text-sa-green mb-4 flex items-center gap-2">
          <span>🇬🇧</span> English Text
        </h2>
        
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Enter English text to translate..."
          className="w-full h-48 px-4 py-3 border-2 border-sa-green/30 rounded-lg focus:ring-2 focus:ring-sa-yellow focus:border-sa-green transition resize-none"
          maxLength={5000}
        />
        
        <div className="mt-4 flex items-center justify-between">
          <span className="text-sm text-gray-500">
            {inputText.length} / 5000 characters
          </span>
        </div>

        {/* Language Selection */}
        <div className="mt-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Target Language
          </label>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="w-full px-4 py-2 border-2 border-sa-green/30 rounded-lg focus:ring-2 focus:ring-sa-yellow focus:border-sa-green transition"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>
                {lang.name}
              </option>
            ))}
          </select>
        </div>

        {/* Translate Button */}
        <button
          onClick={handleTranslate}
          disabled={loading || !inputText.trim()}
          className="w-full mt-6 bg-sa-green text-white py-3 rounded-lg font-medium hover:bg-sa-green/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              Translating...
            </>
          ) : (
            <>
              <span>🌍</span>
              Translate
            </>
          )}
        </button>

        {/* Error Message */}
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Output Panel */}
      <div className="bg-white rounded-2xl shadow-xl p-6 border-t-4 border-sa-yellow">
        <h2 className="text-xl font-semibold text-sa-blue mb-4 flex items-center gap-2">
          <span>🇿🇦</span> Translation
        </h2>

        {translatedText ? (
          <div className="space-y-6">
            {/* Translated Text */}
            <div className="bg-gradient-to-br from-sa-green/10 to-sa-blue/10 border-2 border-sa-green/30 rounded-lg p-4 min-h-[12rem]">
              <p className="text-lg text-gray-900 leading-relaxed font-medium">
                {translatedText}
              </p>
            </div>

            {/* Audio Controls */}
            <div className="bg-gradient-to-r from-sa-yellow/20 to-sa-red/20 border-2 border-sa-yellow rounded-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="font-medium text-sa-blue mb-1 flex items-center gap-2">
                    <span>🔊</span> Text-to-Speech
                  </h3>
                  <p className="text-sm text-gray-600">
                    Generate and play audio
                  </p>
                </div>
              </div>

              <div className="flex gap-3">
                {/* Generate Audio Button */}
                <button
                  onClick={handleGenerateAudio}
                  disabled={audioLoading}
                  className="flex-1 bg-sa-red text-white py-3 rounded-lg font-medium hover:bg-sa-red/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-md"
                >
                  {audioLoading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <span>🎵</span>
                      Generate Audio
                    </>
                  )}
                </button>

                {/* Play Audio Button */}
                {audioData && (
                  <button
                    onClick={playAudio}
                    className="bg-white p-3 rounded-lg shadow-md hover:shadow-lg transition border-2 border-sa-yellow hover:bg-sa-yellow/10"
                  >
                    <svg
                      className="w-6 h-6 text-sa-green"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
                    </svg>
                  </button>
                )}
              </div>
            </div>

            {/* Language Info */}
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <span className="font-medium">Language:</span>
              <span className="px-3 py-1 bg-gradient-to-r from-sa-green to-sa-blue text-white rounded-full font-medium shadow-sm">
                {LANGUAGES.find(l => l.code === selectedLanguage)?.name}
              </span>
            </div>
          </div>
        ) : (
          <div className="flex items-center justify-center h-64 text-gray-400">
            <div className="text-center">
              <svg
                className="w-16 h-16 mx-auto mb-4 opacity-50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"
                />
              </svg>
              <p>Your translation will appear here</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
