import ApiService from './api';
import type { LoginCredentials, User } from '../types/user';

export interface AuthResponse {
  message: string;
  user: User;
  redirect_url?: string;
}

export class AuthService {
  /**
   * Login user with email and password
   */
  static async login(credentials: LoginCredentials): Promise<AuthResponse> {
    try {
      const response = await ApiService.post<AuthResponse>('/api/v1/users/login', credentials);
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Logout current user
   */
  static async logout(): Promise<{ message: string }> {
    try {
      const response = await ApiService.post<{ message: string }>('/api/v1/users/logout');
      return response;
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  /**
   * Get current authenticated user info
   */
  static async getCurrentUser(): Promise<User> {
    try {
      const response = await ApiService.get<User>('/api/v1/users/me');
      return response;
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  }

  /**
   * Check if user is authenticated by trying to get current user
   */
  static async isAuthenticated(): Promise<boolean> {
    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      return false;
    }
  }
}

export default AuthService;
