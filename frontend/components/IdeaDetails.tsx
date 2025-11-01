'use client';

import { useState } from 'react';
import { Copy, Check, Calendar, TrendingUp, Target, Award, FileText, Image } from 'lucide-react';

interface IdeaDetailsProps {
  idea: any;
}

export default function IdeaDetails({ idea }: IdeaDetailsProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const handleCopy = (content: string, index: number) => {
    navigator.clipboard.writeText(content);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'carousel':
        return <Image className="h-4 w-4" />;
      case 'video_script':
        return <FileText className="h-4 w-4" />;
      default:
        return <FileText className="h-4 w-4" />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'carousel':
        return 'bg-purple-100 text-purple-800';
      case 'video_script':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-blue-100 text-blue-800';
    }
  };

  return (
    <div className="space-y-6">
      {/* Product Overview */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{idea.idea.title}</h2>
            <p className="text-gray-600 mb-4">{idea.idea.description}</p>
            <a
              href={idea.idea.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-linkedin-600 hover:text-linkedin-700 hover:underline"
            >
              {idea.idea.url} ↗
            </a>
          </div>
        </div>

        {/* Scores */}
        {idea.analysis && (
          <div className="mt-6 grid grid-cols-2 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <TrendingUp className="h-5 w-5 text-blue-600" />
                <span className="text-sm font-medium text-blue-900">Market Score</span>
              </div>
              <div className="text-3xl font-bold text-blue-700">
                {idea.analysis.market_analysis?.market_score || 'N/A'}/10
              </div>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
              <div className="flex items-center space-x-2 mb-2">
                <Award className="h-5 w-5 text-purple-600" />
                <span className="text-sm font-medium text-purple-900">Uniqueness Score</span>
              </div>
              <div className="text-3xl font-bold text-purple-700">
                {idea.analysis.uniqueness?.uniqueness_score || 'N/A'}/10
              </div>
            </div>
          </div>
        )}

        {/* Target Audience */}
        {idea.analysis?.target_persona && (
          <div className="mt-4 bg-gray-50 rounded-lg p-4">
            <div className="flex items-center space-x-2 mb-2">
              <Target className="h-4 w-4 text-gray-600" />
              <span className="text-sm font-semibold text-gray-900">Target Audience</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {idea.analysis.target_persona.titles?.map((title: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-white rounded-full text-xs text-gray-700 border border-gray-200">
                  {title}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Iterations Badge */}
        <div className="mt-4 inline-flex items-center space-x-2 bg-green-50 px-3 py-1.5 rounded-full">
          <Check className="h-4 w-4 text-green-600" />
          <span className="text-sm text-green-700">
            Refined through {idea.iterations} iteration{idea.iterations > 1 ? 's' : ''}
          </span>
        </div>
      </div>

      {/* Generated Posts */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">Generated LinkedIn Posts</h3>
          <p className="text-sm text-gray-500 mt-1">
            {idea.posts.length} posts optimized for maximum engagement
          </p>
        </div>

        <div className="divide-y divide-gray-200">
          {idea.posts.map((post: any, index: number) => (
            <div key={post.id} className="p-6 hover:bg-gray-50 transition">
              {/* Post Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-3">
                  <div className="bg-linkedin-100 px-3 py-1 rounded-full">
                    <span className="text-sm font-semibold text-linkedin-700">Post #{index + 1}</span>
                  </div>
                  <span className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${getTypeColor(post.type)}`}>
                    {getTypeIcon(post.type)}
                    <span>{post.type.replace('_', ' ')}</span>
                  </span>
                  {post.engagement_prediction && (
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                      post.engagement_prediction === 'high'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {post.engagement_prediction} engagement
                    </span>
                  )}
                </div>
                <button
                  onClick={() => handleCopy(post.content, index)}
                  className="flex items-center space-x-2 px-4 py-2 bg-linkedin-500 text-white rounded-lg hover:bg-linkedin-600 transition text-sm font-medium"
                >
                  {copiedIndex === index ? (
                    <>
                      <Check className="h-4 w-4" />
                      <span>Copied!</span>
                    </>
                  ) : (
                    <>
                      <Copy className="h-4 w-4" />
                      <span>Copy Post</span>
                    </>
                  )}
                </button>
              </div>

              {/* Scheduling Info */}
              {post.scheduled_date && post.scheduled_time && (
                <div className="mb-4 flex items-center space-x-2 text-sm">
                  <Calendar className="h-4 w-4 text-gray-400" />
                  <span className="text-gray-600">
                    Post on <span className="font-medium text-gray-900">{post.scheduled_date}</span> at{' '}
                    <span className="font-medium text-gray-900">{post.scheduled_time}</span>
                  </span>
                </div>
              )}

              {/* Post Content */}
              <div className="bg-gray-50 rounded-lg p-4 mb-4">
                <div className="whitespace-pre-wrap text-sm text-gray-900 leading-relaxed">
                  {post.content}
                </div>
              </div>

              {/* Carousel Slides */}
              {post.carousel_slides && post.carousel_slides.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-3">Carousel Slides:</p>
                  <div className="grid grid-cols-2 gap-3">
                    {post.carousel_slides.map((slide: any, i: number) => (
                      <div key={i} className="bg-white border border-gray-200 rounded-lg p-3">
                        <div className="text-xs font-semibold text-gray-500 mb-1">Slide {slide.slide_number}</div>
                        <div className="text-sm font-medium text-gray-900 mb-1">{slide.headline}</div>
                        <div className="text-xs text-gray-600">{slide.content}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Hashtags */}
              {post.hashtags && post.hashtags.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {post.hashtags.map((tag: string, i: number) => (
                    <span key={i} className="text-xs text-linkedin-600 bg-linkedin-50 px-2 py-1 rounded">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
