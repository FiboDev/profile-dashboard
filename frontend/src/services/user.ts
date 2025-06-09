import ApiService from './api';
import type { User, Skill, UserProfile } from '../types/user';

export class UserService {
  /**
   * Get user by ID
   */
  static async getUserById(userId: number): Promise<User> {
    try {
      const response = await ApiService.get<User>(`/api/v1/users/${userId}`);
      return response;
    } catch (error) {
      console.error('Get user by ID error:', error);
      throw error;
    }
  }

  /**
   * Get user profile with skills (only for own profile)
   */
  static async getUserProfile(userId: number): Promise<UserProfile> {
    try {
      const response = await ApiService.get<UserProfile>(`/api/v1/users/${userId}/profile`);
      return response;
    } catch (error) {
      console.error('Get user profile error:', error);
      throw error;
    }
  }

  /**
   * Get all users (if needed for admin functionality)
   */
  static async getAllUsers(skip: number = 0, limit: number = 100): Promise<User[]> {
    try {
      const response = await ApiService.get<User[]>(`/api/v1/users/?skip=${skip}&limit=${limit}`);
      return response;
    } catch (error) {
      console.error('Get all users error:', error);
      throw error;
    }
  }
}

export class SkillService {
  /**
   * Get user's own skills
   */
  static async getMySkills(skip: number = 0, limit: number = 100, category?: string): Promise<Skill[]> {
    try {
      let endpoint = `/api/v1/skills/?skip=${skip}&limit=${limit}`;
      if (category) {
        endpoint += `&category=${encodeURIComponent(category)}`;
      }
      const response = await ApiService.get<Skill[]>(endpoint);
      return response;
    } catch (error) {
      console.error('Get my skills error:', error);
      throw error;
    }
  }

  /**
   * Get skills for a specific user (only own skills allowed)
   */
  static async getUserSkills(userId: number): Promise<Skill[]> {
    try {
      const response = await ApiService.get<Skill[]>(`/api/v1/skills/user/${userId}`);
      return response;
    } catch (error) {
      console.error('Get user skills error:', error);
      throw error;
    }
  }

  /**
   * Create a new skill
   */
  static async createSkill(skillData: Omit<Skill, 'id' | 'created_at' | 'updated_at'>): Promise<Skill> {
    try {
      const response = await ApiService.post<Skill>('/api/v1/skills/', skillData);
      return response;
    } catch (error) {
      console.error('Create skill error:', error);
      throw error;
    }
  }

  /**
   * Update a skill
   */
  static async updateSkill(skillId: number, skillData: Partial<Skill>): Promise<Skill> {
    try {
      const response = await ApiService.put<Skill>(`/api/v1/skills/${skillId}`, skillData);
      return response;
    } catch (error) {
      console.error('Update skill error:', error);
      throw error;
    }
  }

  /**
   * Delete a skill
   */
  static async deleteSkill(skillId: number): Promise<void> {
    try {
      await ApiService.delete(`/api/v1/skills/${skillId}`);
    } catch (error) {
      console.error('Delete skill error:', error);
      throw error;
    }
  }
}

export { UserService as default };
