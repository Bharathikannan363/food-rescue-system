import { useState, useEffect } from 'react';
import { volunteerService } from '../services/volunteerService';

export const useGeolocation = (isVolunteerActive = false) => {
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!navigator.geolocation) {
      setError('Geolocation API is not supported by your browser');
      return;
    }

    const handleSuccess = (position) => {
      const { latitude, longitude } = position.coords;
      setLocation({ latitude, longitude });

      // Automatically post to Flask backend if user is an active logged-in volunteer
      const token = localStorage.getItem('token');
      if (isVolunteerActive && token) {
        volunteerService.updateLocation(latitude, longitude).catch(err => {
          console.warn('[Geolocation API Sync Error]', err);
        });
      }
    };

    const handleError = (err) => {
      setError(err.message);
    };

    const watchId = navigator.geolocation.watchPosition(handleSuccess, handleError, {
      enableHighAccuracy: true,
      maximumAge: 10000,
      timeout: 15000
    });

    return () => navigator.geolocation.clearWatch(watchId);
  }, [isVolunteerActive]);

  return { location, error };
};
