// API Configuration
const getApiUrl = () => {
  // Check for environment variable first
  const apiUrl = import.meta.env.VITE_API_URL;

  if (apiUrl) {
    return apiUrl;
  }

  // Fallback to Azure backend URL
  return "http://food-analyzer-backend-sea.southeastasia.azurecontainer.io:8000";
};

export const API_BASE_URL = getApiUrl();
export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/api/health`,
  analyze: `${API_BASE_URL}/api/analyze`,
};
