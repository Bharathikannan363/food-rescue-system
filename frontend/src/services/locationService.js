import api from './api';

export const locationService = {
  getVolunteersLocations: () => api.get('/location/volunteers')
};
