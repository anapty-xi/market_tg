export interface Category {
    id: number;
    name: string;
}

export interface Product {
    id: number;
    name: string;
    description: string;
    price: string; 
    category: Category;
    images_links: string[];
}

export interface CartItem {
    id: number;
    product: Product;
    quantity: number;
    total_price: string; 
}