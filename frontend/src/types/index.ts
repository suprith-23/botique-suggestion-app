export type UserRole = 'admin' | 'user';

export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user: User;
}

export type ClothType = 'saree' | 'kurti' | 'lehenga' | 'shirt' | 'dress' | 'blouse' | 'dupatta' | 'shawl';
export type Occasion = 'wedding' | 'casual' | 'festival' | 'party' | 'office';
export type Gender = 'male' | 'female' | 'unisex';
export type AgeGroup = 'child' | 'adult' | 'senior';
export type BudgetRange = '1000-3000' | '3000-8000' | '10000+';

export interface Upload {
  id: number;
  user_id: number;
  image_path: string;
  cloth_type: ClothType;
  occasion: Occasion;
  gender: Gender;
  age_group: AgeGroup;
  budget_range: BudgetRange;
  fabric_description?: string;
  created_at: string;
}

export interface DesignSuggestion {
  id: number;
  upload_id: number;
  user_id: number;
  neck_design: string;
  sleeve_style: string;
  embroidery_pattern: string;
  color_combination: string;
  border_style: string;
  description: string;
  confidence_score: string;
  created_at: string;
}

export interface SavedDesign {
  id: number;
  user_id: number;
  design_suggestion_id: number;
  saved_at: string;
}

export interface DashboardStats {
  total_uploads: number;
  cloth_types: Array<{ type: string; count: number }>;
  occasions: Array<{ occasion: string; count: number }>;
}

export interface TrendingData {
  trending_cloths: Array<{ cloth_type: string; count: number }>;
  trending_occasions: Array<{ occasion: string; count: number }>;
  trending_colors: string[];
  trending_patterns: string[];
}
