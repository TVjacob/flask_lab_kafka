// src/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5080', // Flask app port
});

export default api;
