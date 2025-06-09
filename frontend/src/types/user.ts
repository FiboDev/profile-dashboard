export interface User {
  id: number;
  name: string;
  position: string;
  email: string;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: number;
  name: string;
  category: string;
  description?: string;
  level: number;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface UserProfile extends User {
  skills: Skill[];
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  message: string;
  user: User;
}
