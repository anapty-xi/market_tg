import axios from 'axios';

const API_BASE = "http://localhost:8001/api/v1"; 

export const fetchProducts = async (subCategoryId: number = 0) => {
    const response = await axios.get(`${API_BASE}/products/${subCategoryId}/`);
    return response.data;
};

export const fetchCategories = async () => {
    const response = await axios.get(`${API_BASE}/categories/`);
    return response.data;
};