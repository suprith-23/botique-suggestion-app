import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/services/api';
import { Upload as UploadType } from '@/types';

export const UserDashboard: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [uploads, setUploads] = useState<UploadType[]>([]);
  const [loading, setLoading] = useState(true);
  const [file, setFile] = useState<File | null>(null);
  const [clothType, setClothType] = useState('kurti');
  const [occasion, setOccasion] = useState('wedding');
  const [gender, setGender] = useState('female');
  const [ageGroup, setAgeGroup] = useState('adult');
  const [budgetRange, setBudgetRange] = useState('3000-8000');
  const [fabricDescription, setFabricDescription] = useState('');
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadUploads();
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

      // Navigate to suggestions page
      navigate(`/design-suggestions/${newUpload.id}`);

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
    navigate(`/design-suggestions/${upload.id}`);
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
                  className="w-full text-left p-3 rounded-lg transition bg-gray-50 border border-gray-200 hover:bg-gray-100"
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
    </div>
  );
};

export default UserDashboard;
