import apiClient from './client';
import { Mix } from '../types';

export const mixesApi = {
  // Получить все активные миксы
  getAll: async (): Promise<Mix[]> => {
    const response = await apiClient.get('/mixes');
    return response.data;
  },

  // Получить микс по ID
  getById: async (id: string): Promise<Mix> => {
    const response = await apiClient.get(`/mixes/${id}`);
    return response.data;
  },

  // Получить featured микс (Mix of the Week)
  getFeatured: async (): Promise<Mix | null> => {
    const response = await apiClient.get('/mixes/featured');
    return response.data;
  },
};
