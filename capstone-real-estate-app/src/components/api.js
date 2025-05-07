import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // backend URL
  withCredentials: true,
});

export const login = async (email, password) => {
  //return api.post('/login/', { email, password });
  const response = await api.post('/login/', { email, password });
  return response.data;
};

export const signup = async ({ name, email, password }) => {
    return api.post('/signup/', { name, email, password });
  };
  
