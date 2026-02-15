import apiClient from './client';
import { Drink } from '../types';

export const drinksApi = {
  getAll: async (): Promise<Drink[]> => {
    const response = await apiClient.get('/drinks');
    return response.data;
  },
};
