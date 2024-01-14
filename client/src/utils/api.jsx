import axios from 'axios';

// Create an instance of axios
const api = axios.create({
    baseURL: 'http://localhost:8000/',
    headers: {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data'
    }
});

export default api;