import type { CartItem } from '../types';

interface Props {
    items: CartItem[];
    onClose: () => void;
    // Используем string, так как твой бэкенд ждет "True"/"False" в URL
    onUpdateQuantity: (productId: number, increase: string) => void; 
    onRemove: (productId: number) => void;
    onCheckout: () => void; // Добавляем новый пропс для перехода к форме
}

export const CartModal = ({ items, onClose, onUpdateQuantity, onRemove, onCheckout }: Props) => {
    const totalCartSum = items.reduce((sum, item) => sum + parseFloat(item.total_price), 0);

    return (
        <div className="fixed inset-0 z-[60] bg-[#1c1c1d] flex flex-col animate-in slide-in-from-right duration-300">
            {/* Шапка корзины */}
            <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <button onClick={onClose} className="text-[#31b545] font-bold text-lg p-2">✕</button>
                <h2 className="text-lg font-bold">Корзина</h2>
                <div className="w-10"></div>
            </div>

            {/* Список товаров */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
                {items.length === 0 ? (
                    <div className="text-center py-20 text-gray-500 italic">Корзина пуста</div>
                ) : (
                    items.map((item) => (
                        <div key={item.id} className="bg-[#2c2c2e] p-4 rounded-2xl flex items-center gap-4">
                            <div className="flex-1">
                                <h3 className="font-bold text-sm leading-tight">{item.product.name}</h3>
                                <p className="text-[#31b545] font-bold mt-1">{item.product.price} ₽</p>
                            </div>

                            {/* Управление количеством */}
                            <div className="flex items-center bg-[#1c1c1d] rounded-xl p-1 gap-2">
                                <button 
                                    onClick={() => onUpdateQuantity(item.product.id, "False")}
                                    className="w-8 h-8 flex items-center justify-center bg-[#3a3a3c] rounded-lg active:scale-90 transition-transform"
                                >
                                    —
                                </button>
                                <span className="font-bold w-4 text-center text-sm">{item.quantity}</span>
                                <button 
                                    onClick={() => onUpdateQuantity(item.product.id, "True")}
                                    className="w-8 h-8 flex items-center justify-center bg-[#3a3a3c] rounded-lg active:scale-90 transition-transform"
                                >
                                    +
                                </button>
                            </div>

                            <button 
                                onClick={() => onRemove(item.product.id)}
                                className="p-2 text-gray-500 hover:text-red-500 transition-colors"
                            >
                                🗑
                            </button>
                        </div>
                    ))
                )}
            </div>

            {/* Футер с итогом */}
            {items.length > 0 && (
                <div className="p-6 bg-[#2c2c2e] rounded-t-[30px] shadow-2xl">
                    <div className="flex justify-between items-center mb-6">
                        <span className="text-gray-400">Итого:</span>
                        <span className="text-2xl font-bold text-[#31b545]">
                            {totalCartSum.toLocaleString()} ₽
                        </span>
                    </div>
                    <button 
                        className="w-full bg-[#31b545] text-white py-4 rounded-2xl font-bold text-lg active:scale-95 transition-all shadow-lg shadow-[#31b545]/20"
                        onClick={onCheckout} // ЗАМЕНИЛИ alert на вызов функции из App.tsx
                                            >
                                                Оформить заказ
                                            </button>
                                        </div>
                                    )}
                                </div>
                            );
                        };