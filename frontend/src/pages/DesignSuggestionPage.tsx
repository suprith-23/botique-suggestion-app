import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Download, Heart, Share2, FileText } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/services/api';
import { DesignSuggestion } from '@/types';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export const DesignSuggestionPage: React.FC = () => {
  const { uploadId } = useParams<{ uploadId: string }>();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [suggestions, setSuggestions] = useState<DesignSuggestion[]>([]);
  const [selectedSuggestion, setSelectedSuggestion] = useState<DesignSuggestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [savedDesigns, setSavedDesigns] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (uploadId) {
      loadSuggestions();
      loadSavedDesigns();
    }
  }, [uploadId]);

  const loadSuggestions = async () => {
    try {
      const response = await api.getUploadSuggestions(parseInt(uploadId!));
      setSuggestions(response.data);
      if (response.data.length > 0) {
        setSelectedSuggestion(response.data[0]);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error loading suggestions:', error);
      setLoading(false);
    }
  };

  const loadSavedDesigns = async () => {
    try {
      const response = await api.getSavedDesigns();
      const saved = new Set(response.data.map((d: DesignSuggestion) => d.id));
      setSavedDesigns(saved);
    } catch (error) {
      console.error('Error loading saved designs:', error);
    }
  };

  const handleSaveDesign = async (suggestion: DesignSuggestion) => {
    try {
      await api.saveDesign(suggestion.id);
      setSavedDesigns(new Set([...savedDesigns, suggestion.id]));
    } catch (error) {
      console.error('Error saving design:', error);
      alert('Design already saved or error occurred');
    }
  };

  const handleUnsaveDesign = async (suggestion: DesignSuggestion) => {
    try {
      await api.unsaveDesign(suggestion.id);
      setSavedDesigns(new Set([...savedDesigns].filter(id => id !== suggestion.id)));
    } catch (error) {
      console.error('Error unsaving design:', error);
    }
  };

  const downloadAsImage = async () => {
    if (!selectedSuggestion) return;

    const canvas = await html2canvas(document.getElementById('suggestion-card') || document.body);
    const link = document.createElement('a');
    link.href = canvas.toDataURL();
    link.download = `design-suggestion-${selectedSuggestion.id}.png`;
    link.click();
  };

  const downloadAsPDF = async () => {
    if (!selectedSuggestion) return;

    const pdf = new jsPDF();
    pdf.setFontSize(16);
    pdf.text('Design Suggestion', 20, 20);

    pdf.setFontSize(10);
    const details = [
      `Neck Design: ${selectedSuggestion.neck_design}`,
      `Sleeve Style: ${selectedSuggestion.sleeve_style}`,
      `Embroidery Pattern: ${selectedSuggestion.embroidery_pattern}`,
      `Color Combination: ${selectedSuggestion.color_combination}`,
      `Border Style: ${selectedSuggestion.border_style}`,
      ``,
      `Description:`,
      selectedSuggestion.description,
    ];

    pdf.text(details, 20, 40);
    pdf.save(`design-suggestion-${selectedSuggestion.id}.pdf`);
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">✨ Design Suggestions</h1>
          <button
            onClick={() => navigate('/user-dashboard')}
            className="btn-secondary"
          >
            Back to Dashboard
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Suggestions List */}
          <div className="lg:col-span-1">
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">📋 Suggestions</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {suggestions.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No suggestions available</p>
                ) : (
                  suggestions.map((suggestion, idx) => (
                    <button
                      key={suggestion.id}
                      onClick={() => setSelectedSuggestion(suggestion)}
                      className={`w-full text-left p-3 rounded-lg border transition ${
                        selectedSuggestion?.id === suggestion.id
                          ? 'bg-purple-100 border-purple-600'
                          : 'border-gray-200 hover:bg-gray-50'
                      }`}
                    >
                      <p className="font-medium text-gray-700">Suggestion {idx + 1}</p>
                      <p className="text-sm text-gray-600 truncate">{suggestion.description}</p>
                    </button>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Suggestion Detail */}
          <div className="lg:col-span-2">
            {selectedSuggestion ? (
              <div className="card p-8">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-2xl font-bold text-gray-800">✨ Design Suggestion</h3>
                  <div className="flex gap-2">
                    <button
                      onClick={downloadAsImage}
                      className="p-2 hover:bg-gray-100 rounded-lg transition"
                      title="Download as Image"
                    >
                      <Download size={20} />
                    </button>
                    <button
                      onClick={downloadAsPDF}
                      className="p-2 hover:bg-gray-100 rounded-lg transition"
                      title="Download as PDF"
                    >
                      <FileText size={20} />
                    </button>
                    <button
                      onClick={() =>
                        savedDesigns.has(selectedSuggestion.id)
                          ? handleUnsaveDesign(selectedSuggestion)
                          : handleSaveDesign(selectedSuggestion)
                      }
                      className={`p-2 rounded-lg transition ${
                        savedDesigns.has(selectedSuggestion.id)
                          ? 'bg-red-100 text-red-600'
                          : 'hover:bg-gray-100'
                      }`}
                      title="Save Design"
                    >
                      <Heart
                        size={20}
                        fill={savedDesigns.has(selectedSuggestion.id) ? 'currentColor' : 'none'}
                      />
                    </button>
                    <button
                      className="p-2 hover:bg-gray-100 rounded-lg transition"
                      title="Share Design"
                    >
                      <Share2 size={20} />
                    </button>
                  </div>
                </div>

                <div id="suggestion-card" className="space-y-6 bg-gray-50 p-6 rounded-lg">
                  <div>
                    <h4 className="text-lg font-semibold text-gray-800 mb-2">🎯 Design Details</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Neck Design</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.neck_design}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Sleeve Style</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.sleeve_style}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Embroidery Pattern</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.embroidery_pattern}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Color Combination</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.color_combination}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Border Style</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.border_style}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Confidence Score</p>
                        <p className="text-base font-medium text-gray-800">{selectedSuggestion.confidence_score}</p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-lg font-semibold text-gray-800 mb-2">📝 Description</h4>
                    <p className="text-gray-700 leading-relaxed">{selectedSuggestion.description}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="card p-8 text-center">
                <p className="text-gray-500 text-lg">Select a suggestion to view details</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DesignSuggestionPage;