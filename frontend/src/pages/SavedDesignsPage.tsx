import React, { useState, useEffect } from 'react';
import { Heart, Download } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/services/api';
import { DesignSuggestion } from '@/types';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export const SavedDesignsPage: React.FC = () => {
  const { user } = useAuth();
  const [savedDesigns, setSavedDesigns] = useState<DesignSuggestion[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDesign, setSelectedDesign] = useState<DesignSuggestion | null>(null);

  useEffect(() => {
    loadSavedDesigns();
  }, []);

  const loadSavedDesigns = async () => {
    try {
      const response = await api.getSavedDesigns();
      setSavedDesigns(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading saved designs:', error);
      setLoading(false);
    }
  };

  const handleUnsave = async (designId: number) => {
    try {
      await api.unsaveDesign(designId);
      setSavedDesigns(savedDesigns.filter(d => d.id !== designId));
      if (selectedDesign?.id === designId) {
        setSelectedDesign(null);
      }
    } catch (error) {
      console.error('Error unsaving design:', error);
    }
  };

  const downloadAsImage = async (design: DesignSuggestion) => {
    const canvas = await html2canvas(document.getElementById(`design-${design.id}`) || document.body);
    const link = document.createElement('a');
    link.href = canvas.toDataURL();
    link.download = `design-${design.id}.png`;
    link.click();
  };

  const downloadAsPDF = async (design: DesignSuggestion) => {
    const pdf = new jsPDF();
    pdf.setFontSize(16);
    pdf.text('Saved Design Suggestion', 20, 20);
    
    pdf.setFontSize(10);
    const details = [
      `Neck Design: ${design.neck_design}`,
      `Sleeve Style: ${design.sleeve_style}`,
      `Embroidery Pattern: ${design.embroidery_pattern}`,
      `Color Combination: ${design.color_combination}`,
      `Border Style: ${design.border_style}`,
      ``,
      `Description:`,
      design.description,
    ];
    
    pdf.text(details, 20, 40);
    pdf.save(`design-${design.id}.pdf`);
  };

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">❤️ Saved Designs</h1>

        {savedDesigns.length === 0 ? (
          <div className="card p-12 text-center">
            <Heart size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-500 text-lg">No saved designs yet. Save some designs to see them here!</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Saved Designs List */}
            <div className="lg:col-span-1">
              <div className="card p-6 max-h-96 overflow-y-auto">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Your Saved Designs</h3>
                <div className="space-y-2">
                  {savedDesigns.map((design) => (
                    <button
                      key={design.id}
                      onClick={() => setSelectedDesign(design)}
                      className={`w-full text-left p-3 rounded-lg border transition ${
                        selectedDesign?.id === design.id
                          ? 'bg-red-100 border-red-600'
                          : 'border-gray-200 hover:bg-gray-50'
                      }`}
                    >
                      <p className="font-medium text-gray-700">Design #{design.id}</p>
                      <p className="text-xs text-gray-400 truncate">{design.description}</p>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Design Details */}
            {selectedDesign && (
              <div className="lg:col-span-2">
                <div className="card p-8">
                  <div className="flex justify-between items-center mb-6">
                    <h3 className="text-2xl font-bold text-gray-800">✨ Design Details</h3>
                    <div className="flex gap-2">
                      <button
                        onClick={() => downloadAsImage(selectedDesign)}
                        className="p-2 hover:bg-gray-100 rounded-lg transition"
                        title="Download as Image"
                      >
                        <Download size={20} />
                      </button>
                      <button
                        onClick={() => downloadAsPDF(selectedDesign)}
                        className="p-2 hover:bg-gray-100 rounded-lg transition"
                        title="Download as PDF"
                      >
                        <Download size={20} />
                      </button>
                      <button
                        onClick={() => handleUnsave(selectedDesign.id)}
                        className="p-2 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition"
                        title="Remove from Saved"
                      >
                        <Heart size={20} fill="currentColor" />
                      </button>
                    </div>
                  </div>

                  <div id={`design-${selectedDesign.id}`} className="space-y-6 bg-gray-50 p-6 rounded-lg">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-600">Neck Design</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.neck_design}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Sleeve Style</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.sleeve_style}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Embroidery Pattern</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.embroidery_pattern}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Color Combination</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.color_combination}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Border Style</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.border_style}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Confidence</p>
                        <p className="text-base font-medium text-gray-800">{selectedDesign.confidence_score}</p>
                      </div>
                    </div>

                    <div>
                      <p className="text-sm text-gray-600 mb-2">Description</p>
                      <p className="text-gray-700 leading-relaxed">{selectedDesign.description}</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default SavedDesignsPage;
