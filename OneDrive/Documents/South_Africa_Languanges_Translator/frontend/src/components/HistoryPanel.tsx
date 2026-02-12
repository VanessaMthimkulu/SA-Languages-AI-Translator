"use client";

import { useState, useEffect } from "react";
import { getHistory, deleteHistory } from "@/lib/api";

/**
 * History panel displaying user's past translations with pagination
 */
interface HistoryPanelProps {
  session: any;
  refreshTrigger?: number;
}

interface HistoryItem {
  id: string;
  original_text: string;
  translated_text: string;
  target_language: string;
  created_at: string;
}

export default function HistoryPanel({ session, refreshTrigger }: HistoryPanelProps) {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const ITEMS_PER_PAGE = 10;

  // Fetch history from API
  const fetchHistory = async () => {
    setLoading(true);
    setError("");

    try {
      const token = session?.access_token;

      if (!token) {
        throw new Error("Not authenticated");
      }

      const result = await getHistory(token, ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);
      
      if (page === 0) {
        setHistory(result.history);
      } else {
        setHistory(prev => [...prev, ...result.history]);
      }

      setHasMore(result.history.length === ITEMS_PER_PAGE);
    } catch (err: any) {
      console.error("History fetch error:", err);
      setError(err.response?.data?.detail || err.message || "Failed to load history");
    } finally {
      setLoading(false);
    }
  };

  // Handle delete
  const handleDelete = async (id: string) => {
    if (!confirm("Delete this translation?")) return;

    try {
      const token = session?.access_token;

      if (!token) {
        throw new Error("Not authenticated");
      }

      await deleteHistory(id, token);
      setHistory(prev => prev.filter(item => item.id !== id));
    } catch (err: any) {
      console.error("Delete error:", err);
      alert("Failed to delete translation");
    }
  };

  // Load more items
  const loadMore = () => {
    setPage(prev => prev + 1);
  };

  // Fetch on mount and when page changes
  useEffect(() => {
    fetchHistory();
  }, [page]);

  // Refresh when trigger changes
  useEffect(() => {
    if (refreshTrigger && refreshTrigger > 0) {
      setPage(0);
      fetchHistory();
    }
  }, [refreshTrigger]);

  // Format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  if (loading && page === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-600">
        {error}
      </div>
    );
  }

  if (history.length === 0) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-12 text-center">
        <svg
          className="w-16 h-16 mx-auto mb-4 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
          />
        </svg>
        <h3 className="text-xl font-semibold text-gray-900 mb-2">
          No translations yet
        </h3>
        <p className="text-gray-600">
          Your translation history will appear here
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {history.map((item) => (
        <div
          key={item.id}
          className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition"
        >
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">
                  {item.target_language}
                </span>
                <span className="text-sm text-gray-500">
                  {formatDate(item.created_at)}
                </span>
              </div>
            </div>
            <button
              onClick={() => handleDelete(item.id)}
              className="text-gray-400 hover:text-red-600 transition"
              title="Delete"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                />
              </svg>
            </button>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">
                English
              </h4>
              <p className="text-gray-900">{item.original_text}</p>
            </div>
            <div>
              <h4 className="text-sm font-medium text-gray-500 mb-1">
                Translation
              </h4>
              <p className="text-gray-900">{item.translated_text}</p>
            </div>
          </div>
        </div>
      ))}

      {/* Load More Button */}
      {hasMore && (
        <div className="text-center pt-4">
          <button
            onClick={loadMore}
            disabled={loading}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? "Loading..." : "Load More"}
          </button>
        </div>
      )}
    </div>
  );
}
