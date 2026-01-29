import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Eye, Download, Heart, Share2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/services/api';
import { Upload as UploadType, DesignSuggestion } from '@/types';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

export const UserDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [uploads, setUploads] = useState<UploadType[]>([]);
  const [suggestions, setSuggestions] = useState<DesignSuggestion[]>([]);
  const [selectedUpload, setSelectedUpload] = useState<UploadType | null>(null);
  const [selectedSuggestion, setSelectedSuggestion] = useState<DesignSuggestion | null>(null);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [clothType, setClothType] = useState('kurti');
  const [occasion, setOccasion] = useState('wedding');
  const [gender, setGender] = useState('female');
  const [ageGroup, setAgeGroup] = useState('adult');
  const [budgetRange, setBudgetRange] = useState('3000-8000');
  const [fabricDescription, setFabricDescription] = useState('');
  const [uploading, setUploading] = useState(false);
  const [savedDesigns, setSavedDesigns] = useState<Set<number>>(new Set());

  useEffect(() => {
    loadUploads();
    loadSavedDesigns();
  }, []);

  const loadUploads = async () => {
    try {
      const response = await api.getMyUploads();
      setUploads(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading uploads:', error);
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

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('cloth_type', clothType);
      formData.append('occasion', occasion);
      formData.append('gender', gender);
      formData.append('age_group', ageGroup);
      formData.append('budget_range', budgetRange);
      formData.append('fabric_description', fabricDescription);

      const response = await api.uploadCloth(formData);
      const newUpload = response.data;
      setUploads([newUpload, ...uploads]);

      // Load suggestions
      const suggestionsResponse = await api.getUploadSuggestions(newUpload.id);
      setSuggestions(suggestionsResponse.data);
      setSelectedUpload(newUpload);
      if (suggestionsResponse.data.length > 0) {
        setSelectedSuggestion(suggestionsResponse.data[0]);
      }

      setFile(null);
      (document.getElementById('fileInput') as HTMLInputElement).value = '';
    } catch (error) {
      console.error('Error uploading:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleViewSuggestions = async (upload: UploadType) => {
    setSelectedUpload(upload);
    try {
      const response = await api.getUploadSuggestions(upload.id);
      setSuggestions(response.data);
      if (response.data.length > 0) {
        setSelectedSuggestion(response.data[0]);
      }
    } catch (error) {
      console.error('Error loading suggestions:', error);
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
        <h1 className="text-3xl font-bold text-gray-800 mb-8">👩‍🎨 User Dashboard</h1>

        {/* Upload Section */}
        <div className="card p-8 mb-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">📸 Upload Your Cloth</h2>
          <form onSubmit={handleUpload} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cloth Type</label>
                <select
                  value={clothType}
                  onChange={(e) => setClothType(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                >
                  <option value="saree">Saree</option>
                  <option value="kurti">Kurti</option>
                  <option value="lehenga">Lehenga</option>
                  <option value="shirt">Shirt</option>
                  <option value="dress">Dress</option>
                  <option value="blouse">Blouse</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Occasion</label>
                <select
                  value={occasion}
                  onChange={(e) => setOccasion(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                >
                  <option value="wedding">Wedding</option>
                  <option value="casual">Casual</option>
                  <option value="festival">Festival</option>
                  <option value="party">Party</option>
                  <option value="office">Office</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="unisex">Unisex</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Age Group</label>
                <select
                  value={ageGroup}
                  onChange={(e) => setAgeGroup(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                >
                  <option value="child">Child</option>
                  <option value="adult">Adult</option>
                  <option value="senior">Senior</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Budget Range</label>
                <select
                  value={budgetRange}
                  onChange={(e) => setBudgetRange(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                >
                  <option value="1000-3000">₹1,000 - ₹3,000</option>
                  <option value="3000-8000">₹3,000 - ₹8,000</option>
                  <option value="10000+">₹10,000+</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Fabric Description (Optional)</label>
              <textarea
                value={fabricDescription}
                onChange={(e) => setFabricDescription(e.target.value)}
                placeholder="Describe the fabric (e.g., silk, cotton, linen)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none"
                rows={2}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Upload Image</label>
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-purple-500 transition cursor-pointer">
                <input
                  id="fileInput"
                  type="file"
                  accept="image/*"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="hidden"
                />
                <label htmlFor="fileInput" className="cursor-pointer flex flex-col items-center gap-2">
                  <Upload size={32} className="text-purple-600" />
                  <span className="text-gray-700">{file ? file.name : 'Click to upload or drag image'}</span>
                </label>
              </div>
            </div>

            <button
              type="submit"
              disabled={!file || uploading}
              className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {uploading ? 'Uploading...' : 'Upload & Get Suggestions'}
            </button>
          </form>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Uploads List */}
          <div className="lg:col-span-1">
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">📋 Your Uploads</h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {uploads.length === 0 ? (
                  <p className="text-gray-500 text-center py-4">No uploads yet</p>
                ) : (
                  uploads.map((upload) => (
                    <button
                      key={upload.id}
                      onClick={() => handleViewSuggestions(upload)}
                      className={`w-full text-left p-3 rounded-lg transition ${
                        selectedUpload?.id === upload.id
                          ? 'bg-purple-100 border-2 border-purple-600'
                          : 'bg-gray-50 border border-gray-200 hover:bg-gray-100'
                      }`}
                    >
                      <p className="font-medium text-gray-700">{upload.cloth_type}</p>
                      <p className="text-sm text-gray-500">{upload.occasion}</p>
                      <p className="text-xs text-gray-400">{new Date(upload.created_at).toLocaleDateString()}</p>
                    </button>
                  ))
                )}
              </div>
            </div>

            {/* Saved Designs */}
            <div className="card p-6 mt-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-4">❤️ Saved Designs</h3>
              <button
                onClick={() => navigate('/saved-designs')}
                className="w-full btn-secondary"
              >
                View All Saved
              </button>
            </div>
          </div>

          {/* Suggestions Detail */}
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
                      <Download size={20} />
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

                {suggestions.length > 1 && (
                  <div className="mt-6">
                    <h4 className="text-lg font-semibold text-gray-800 mb-3">Other Suggestions</h4>
                    <div className="space-y-2">
                      {suggestions.map((suggestion, idx) => (
                        <button
                          key={suggestion.id}
                          onClick={() => setSelectedSuggestion(suggestion)}
                          className={`w-full text-left p-3 rounded-lg border transition ${
                            selectedSuggestion.id === suggestion.id
                              ? 'bg-purple-100 border-purple-600'
                              : 'border-gray-200 hover:bg-gray-50'
                          }`}
                        >
                          <p className="font-medium text-gray-700">Suggestion {idx + 1}</p>
                          <p className="text-sm text-gray-600 truncate">{suggestion.description}</p>
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="card p-8 text-center">
                <Eye size={48} className="mx-auto text-gray-300 mb-4" />
                <p className="text-gray-500 text-lg">Select or upload an item to see suggestions</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
