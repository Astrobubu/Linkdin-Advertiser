'use client';

import { useState } from 'react';
import { Globe, Loader2 } from 'lucide-react';

interface AnalyzeFormProps {
  onAnalyze: (url: string) => Promise<void>;
  analyzing: boolean;
}

export default function AnalyzeForm({ onAnalyze, analyzing }: AnalyzeFormProps) {
  const [url, setUrl] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (url.trim() && !analyzing) {
      await onAnalyze(url.trim());
      setUrl('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="bg-linkedin-100 p-3 rounded-lg">
            <Globe className="h-6 w-6 text-linkedin-600" />
          </div>
        </div>
        <div className="flex-1">
          <label htmlFor="url" className="block text-sm font-medium text-gray-900 mb-2">
            Analyze Your Product
          </label>
          <div className="flex space-x-3">
            <input
              type="url"
              id="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://your-product-website.com"
              className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-linkedin-500 focus:border-transparent outline-none transition"
              required
              disabled={analyzing}
            />
            <button
              type="submit"
              disabled={analyzing || !url.trim()}
              className="px-6 py-2.5 bg-linkedin-500 text-white font-medium rounded-lg hover:bg-linkedin-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-linkedin-500 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center space-x-2"
            >
              {analyzing ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <span>Analyze & Generate Posts</span>
              )}
            </button>
          </div>
          <p className="mt-2 text-xs text-gray-500">
            Enter your product's website URL. Our AI agents will analyze it and generate optimized LinkedIn posts.
          </p>
        </div>
      </div>
    </form>
  );
}
