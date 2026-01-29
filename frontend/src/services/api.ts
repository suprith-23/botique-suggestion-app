import axios, { AxiosInstance } from 'axios';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: '/api',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add token to requests
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth
  registerUser(email: string, username: string, password: string, fullName?: string) {
    return this.client.post('/auth/register/user', {
      email,
      username,
      password,
      full_name: fullName,
    });
  }

  registerAdmin(email: string, username: string, password: string, fullName?: string) {
    return this.client.post('/auth/register/admin', {
      email,
      username,
      password,
      full_name: fullName,
    });
  }

  login(email: string, password: string) {
    return this.client.post('/auth/login', null, {
      params: { email, password },
    });
  }

  getCurrentUser() {
    return this.client.get('/auth/me');
  }

  updateUser(fullName?: string, password?: string) {
    return this.client.put('/auth/me', {
      full_name: fullName,
      password,
    });
  }

  // Uploads
  uploadCloth(formData: FormData) {
    return this.client.post('/uploads', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }

  getMyUploads(skip: number = 0, limit: number = 10) {
    return this.client.get('/uploads/my-uploads', {
      params: { skip, limit },
    });
  }

  getUpload(uploadId: number) {
    return this.client.get(`/uploads/${uploadId}`);
  }

  // Design Suggestions
  getUploadSuggestions(uploadId: number) {
    return this.client.get(`/uploads/${uploadId}/suggestions`);
  }

  getSuggestion(suggestionId: number) {
    return this.client.get(`/design-suggestions/${suggestionId}`);
  }

  saveDesign(suggestionId: number) {
    return this.client.post(`/design-suggestions/${suggestionId}/save`);
  }

  getSavedDesigns() {
    return this.client.get('/design-suggestions/saved/list');
  }

  unsaveDesign(suggestionId: number) {
    return this.client.delete(`/design-suggestions/${suggestionId}/save`);
  }

  // Admin
  getDashboardStats() {
    return this.client.get('/admin/dashboard/stats');
  }

  getAllUploads(skip: number = 0, limit: number = 10) {
    return this.client.get('/admin/uploads', {
      params: { skip, limit },
    });
  }

  getUploadsByType(clothType: string) {
    return this.client.get(`/admin/uploads/by-type/${clothType}`);
  }

  getTrendingData() {
    return this.client.get('/admin/trending');
  }
}

export const api = new APIClient();
