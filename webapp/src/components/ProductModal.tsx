import type { Product } from '../types';

const PHOTO_URL = "http://localhost:8001";

interface Props {
    product: Product;
    onClose: () => void;
    onAddToCart: (productId: number) => void;
}

export const ProductModal = ({ product, onClose, onAddToCart }: Props) => {
    return (
        // Контейнер теперь центрирует контент (items-center) и имеет более темный фон
        <div 
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
            onClick={onClose}
        >
            {/* Окно теперь с закруглением со всех сторон и анимацией появления из центра (zoom-in) */}
            <div 
                className="bg-[#1c1c1d] w-full max-w-sm rounded-[24px] p-6 shadow-2xl animate-in zoom-in duration-200"
                onClick={(e) => e.stopPropagation()} 
            >
                {/* Изображение товара */}
                <img 
                    src={`${PHOTO_URL}${product.images_links[0]}`} 
                    className="w-full h-56 object-contain rounded-xl mb-4" 
                    alt={product.name}
                />

                {/* Текстовый блок отцентрован для баланса в квадратном окне */}
                <h2 className="text-xl font-bold mb-2 text-center">{product.name}</h2>
                <p className="text-gray-400 text-sm mb-6 text-center leading-relaxed">
                    {product.description || "Описание товара скоро появится."}
                </p>

                {/* Блок цены и кнопки покупки */}
                <div className="flex flex-col gap-4">
                    <div className="text-2xl font-bold text-[#31b545] text-center">
                        {product.price} ₽
                    </div>
                    <button 
                        onClick={() => onAddToCart(product.id)}
                        className="w-full bg-[#31b545] text-white py-3 rounded-xl font-bold active:scale-95 transition-all shadow-lg shadow-[#31b545]/20"
                    >
                        В корзину
                    </button>
                </div>
            </div>
        </div>
    );
};