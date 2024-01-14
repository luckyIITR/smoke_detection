import axios from 'axios';

// Create an instance of axios
const api = axios.create({
    baseURL: 'http://10.14.0.57:10000/',
    headers: {
        'accept': 'application/json',
        'Content-Type': 'multipart/form-data'
    }
});

export default api;