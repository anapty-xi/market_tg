import type { Product } from '../types';


const PHOTO_URL = "http://localhost:8001";

interface Props {
    product: Product;
}

export const ProductCard = ({ product }: Props) => {
    return (
        <div 
            className="bg-[#2c2c2e] p-3 rounded-xl active:scale-95 transition-transform"

        >
            <img 
                src={`${PHOTO_URL}${product.images_links[0]}`} 
                className="w-full h-32 object-contain rounded-lg" 
                alt={product.name}
                onError={(e) => { (e.target as HTMLImageElement).src = 'https://via.placeholder.com/150' }}
            />
            <p className="text-sm mt-2 font-medium truncate">{product.name}</p>
            <p className="font-bold text-[#31b545]">{product.price} ₽</p>
        </div>
    );
};