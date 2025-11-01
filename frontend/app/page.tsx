'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Sparkles, Loader2, Calendar, TrendingUp, CheckCircle2, AlertCircle } from 'lucide-react';
import AnalyzeForm from '@/components/AnalyzeForm';
import IdeaList from '@/components/IdeaList';
import IdeaDetails from '@/components/IdeaDetails';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [ideas, setIdeas] = useState<any[]>([]);
  const [selectedIdea, setSelectedIdea] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    fetchIdeas();
  }, []);

  const fetchIdeas = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/api/ideas`);
      setIdeas(response.data);
    } catch (error) {
      console.error('Error fetching ideas:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async (url: string) => {
    try {
      setAnalyzing(true);
      const response = await axios.post(`${API_URL}/api/analyze`, { url });

      // Fetch updated ideas list
      await fetchIdeas();

      // Load the newly analyzed idea
      const ideaDetails = await axios.get(`${API_URL}/api/ideas/${response.data.idea_id}`);
      setSelectedIdea(ideaDetails.data);

    } catch (error: any) {
      console.error('Error analyzing URL:', error);
      alert(`Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSelectIdea = async (ideaId: number) => {
    try {
      const response = await axios.get(`${API_URL}/api/ideas/${ideaId}`);
      setSelectedIdea(response.data);
    } catch (error) {
      console.error('Error fetching idea details:', error);
    }
  };

  const handleDelete = async (ideaId: number) => {
    if (!confirm('Are you sure you want to delete this idea and all its posts?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/ideas/${ideaId}`);
      await fetchIdeas();
      if (selectedIdea?.idea?.id === ideaId) {
        setSelectedIdea(null);
      }
    } catch (error) {
      console.error('Error deleting idea:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-linkedin-500 p-2 rounded-lg">
                <Sparkles className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">LinkedIn Advertiser</h1>
                <p className="text-sm text-gray-500">AI-Powered Multi-Agent Post Generator</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm">
              <div className="flex items-center space-x-2 bg-green-50 px-3 py-1.5 rounded-full">
                <CheckCircle2 className="h-4 w-4 text-green-600" />
                <span className="text-green-700 font-medium">GPT-4 Active</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Analyze Form */}
        <div className="mb-8">
          <AnalyzeForm onAnalyze={handleAnalyze} analyzing={analyzing} />
        </div>

        {/* Analysis Status */}
        {analyzing && (
          <div className="mb-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
            <div className="flex items-start space-x-4">
              <Loader2 className="h-6 w-6 text-blue-600 animate-spin flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h3 className="font-semibold text-blue-900 mb-2">Multi-Agent Pipeline Running...</h3>
                <div className="space-y-2 text-sm text-blue-700">
                  <p>✓ Agent 1: Scraping web page...</p>
                  <p>✓ Agent 2: Analyzing product and market...</p>
                  <p>⏳ Agent 3: Critically evaluating (may loop)...</p>
                  <p>⏳ Agent 4: Generating LinkedIn posts...</p>
                </div>
                <p className="mt-3 text-xs text-blue-600">This may take 30-60 seconds...</p>
              </div>
            </div>
          </div>
        )}

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - Ideas List */}
          <div className="lg:col-span-1">
            <IdeaList
              ideas={ideas}
              selectedIdea={selectedIdea?.idea}
              onSelect={handleSelectIdea}
              onDelete={handleDelete}
              loading={loading}
            />
          </div>

          {/* Main Content - Idea Details */}
          <div className="lg:col-span-2">
            {selectedIdea ? (
              <IdeaDetails idea={selectedIdea} />
            ) : (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-12 text-center">
                <div className="max-w-md mx-auto">
                  <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
                    <TrendingUp className="h-8 w-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No Idea Selected
                  </h3>
                  <p className="text-gray-500 mb-6">
                    Analyze a product URL above or select an existing idea from the list to view generated LinkedIn posts
                  </p>
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-sm text-left">
                    <p className="font-medium text-blue-900 mb-2">How it works:</p>
                    <ol className="list-decimal list-inside space-y-1 text-blue-700">
                      <li>Enter your product URL</li>
                      <li>AI agents analyze your product</li>
                      <li>Get 7-10 optimized LinkedIn posts</li>
                      <li>Copy and schedule at suggested times</li>
                    </ol>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            Powered by GPT-4 • Multi-Agent Architecture • Based on 2025 LinkedIn Best Practices
          </p>
        </div>
      </footer>
    </div>
  );
}
