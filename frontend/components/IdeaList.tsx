'use client';

import { Loader2, Trash2, ExternalLink } from 'lucide-react';

interface Idea {
  id: number;
  url: string;
  title: string;
  description: string;
  status: string;
  created_at: string;
}

interface IdeaListProps {
  ideas: Idea[];
  selectedIdea: any;
  onSelect: (id: number) => void;
  onDelete: (id: number) => void;
  loading: boolean;
}

export default function IdeaList({ ideas, selectedIdea, onSelect, onDelete, loading }: IdeaListProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-center space-x-2 text-gray-500">
          <Loader2 className="h-5 w-5 animate-spin" />
          <span>Loading ideas...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      <div className="p-4 border-b border-gray-200">
        <h2 className="font-semibold text-gray-900">Your Products</h2>
        <p className="text-xs text-gray-500 mt-1">
          {ideas.length} {ideas.length === 1 ? 'product' : 'products'} analyzed
        </p>
      </div>

      <div className="divide-y divide-gray-200 max-h-[600px] overflow-y-auto">
        {ideas.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <p className="text-sm">No products yet</p>
            <p className="text-xs mt-1">Analyze a URL to get started</p>
          </div>
        ) : (
          ideas.map((idea) => (
            <div
              key={idea.id}
              className={`p-4 cursor-pointer transition hover:bg-gray-50 ${
                selectedIdea?.id === idea.id ? 'bg-blue-50 border-l-4 border-linkedin-500' : ''
              }`}
              onClick={() => onSelect(idea.id)}
            >
              <div className="flex items-start justify-between space-x-2">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-gray-900 truncate text-sm">
                    {idea.title || 'Untitled'}
                  </h3>
                  <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                    {idea.description || 'No description'}
                  </p>
                  <div className="flex items-center space-x-2 mt-2">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      idea.status === 'posts_generated'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {idea.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(idea.id);
                  }}
                  className="flex-shrink-0 p-1.5 text-gray-400 hover:text-red-600 transition rounded"
                  title="Delete"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
