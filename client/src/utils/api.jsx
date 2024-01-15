import axios from 'axios';

// Create an instance of axios
const api = axios.create({
    baseURL: 'https://smoke-detection-api.onrender.com/',
    headers: {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data'
    }
});

export default api;