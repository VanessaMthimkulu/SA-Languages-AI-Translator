"use client";

import { useState } from "react";
import { supabase } from "@/lib/supabase";
import TranslatorPanel from "./TranslatorPanel";
import HistoryPanel from "./HistoryPanel";

/**
 * Main translator page with tabs for translation and history
 */
interface TranslatorPageProps {
  session: any;
}

export default function TranslatorPage({ session }: TranslatorPageProps) {
  const [activeTab, setActiveTab] = useState<"translate" | "history">("translate");
  const [refreshHistory, setRefreshHistory] = useState(0);

  // Handle user logout
  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  // Trigger history refresh when new translation is saved
  const handleTranslationSaved = () => {
    setRefreshHistory(prev => prev + 1);
  };

  return (
    <div className="min-h-screen gradient-sa-blue">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-4 border-sa-yellow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">🇿🇦</span>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-sa-green via-sa-yellow to-sa-red bg-clip-text text-transparent">
                SA Translator
              </h1>
            </div>
            
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 font-medium">
                {session.user.email}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium text-white bg-sa-red rounded-lg hover:bg-sa-red/90 transition shadow-md"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="flex gap-2 border-b-2 border-sa-yellow/30">
          <button
            onClick={() => setActiveTab("translate")}
            className={`px-6 py-3 font-medium transition border-b-4 ${
              activeTab === "translate"
                ? "border-sa-yellow text-white bg-sa-green/20 rounded-t-lg"
                : "border-transparent text-white/70 hover:text-white hover:bg-white/10 rounded-t-lg"
            }`}
          >
            🌍 Translate
          </button>
          <button
            onClick={() => setActiveTab("history")}
            className={`px-6 py-3 font-medium transition border-b-4 ${
              activeTab === "history"
                ? "border-sa-yellow text-white bg-sa-green/20 rounded-t-lg"
                : "border-transparent text-white/70 hover:text-white hover:bg-white/10 rounded-t-lg"
            }`}
          >
            📚 History
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === "translate" ? (
          <TranslatorPanel 
            session={session} 
            onTranslationSaved={handleTranslationSaved}
          />
        ) : (
          <HistoryPanel 
            session={session} 
            refreshTrigger={refreshHistory}
          />
        )}
      </div>
    </div>
  );
}
