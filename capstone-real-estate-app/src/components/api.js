import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',  // backend URL
  withCredentials: true,
});

export const login = async (username, password) => {
  return api.post('/login/', { username, password });
};

export const signup = async (username, email, password) => {
  return api.post('/signup/', { username, email, password });
};
