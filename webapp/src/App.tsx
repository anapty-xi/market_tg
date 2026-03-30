import { useState, useEffect } from 'react';
import axios from 'axios';
import type { Category, Product, CartItem } from './types'; 
import { CategoryBar } from './components/CategoryBar';
import { ProductCard } from './components/ProductCard';
import { ProductModal } from './components/ProductModal';
import { CartModal } from './components/CartModal'; 
import { OrderForm } from './components/OrderForm'; 

const BASE_URL = "http://localhost:8000"; 
import.meta.env.VITE_USER_ID

function App() {
    const [products, setProducts] = useState<Product[]>([]);
    const [categories, setCategories] = useState<Category[]>([]);
    const [selectedSubId, setSelectedSubId] = useState(0);
    const [loading, setLoading] = useState(true);
    const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
    
    // Состояния для корзины и заказа
    const [cartItems, setCartItems] = useState<CartItem[]>([]);
    const [isCartOpen, setIsCartOpen] = useState(false);
    const [isOrderFormOpen, setIsOrderFormOpen] = useState(false);

    useEffect(() => {
        const tg = window.Telegram?.WebApp;
        if (tg) {
            tg.ready();
            tg.setHeaderColor('secondary_bg_color');
            tg.setBackgroundColor('bg_color');
            tg.expand();
        }

        const loadData = async () => {
            try {
                const [catRes, prodRes] = await Promise.all([
                    axios.get(`${BASE_URL}/api/v1/sub_categories/0/`),
                    axios.get(`${BASE_URL}/api/v1/products/0/`)
                ]);
                setCategories(catRes.data);
                setProducts(prodRes.data);
                await fetchCart();
            } catch (err) { console.error(err); } 
            finally { setLoading(false); }
        };
        loadData();
    }, []);

    // --- ЛОГИКА КОРЗИНЫ ---

    const fetchCart = async () => {
        const tg = window.Telegram?.WebApp;
        const userId = tg?.initDataUnsafe?.user?.id || import.meta.env.VITE_USER_ID; 
        try {
            const res = await axios.get(`${BASE_URL}/api/v1/cart/${userId}/?_t=${Date.now()}`);
            setCartItems(res.data);
        } catch (err) {
            console.error("Ошибка загрузки корзины:", err);
        }
    };

    const handleUpdateQuantity = async (productId: number, increase: string) => {
        const userId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || import.meta.env.VITE_USER_ID;
        try {
            await axios.patch(`${BASE_URL}/api/v1/cart_item/${userId}/?prod_id=${productId}&increase=${increase}`);
            await fetchCart();
        } catch (err) {
            console.error("Ошибка PATCH:", err);
        }
    };

    const handleRemoveItem = async (productId: number) => {
        setCartItems(prev => prev.filter(item => item.product.id !== productId));
        const userId = window.Telegram?.WebApp?.initDataUnsafe?.user?.id || import.meta.env.VITE_USER_ID;
        try {
            await axios.delete(`${BASE_URL}/api/v1/cart_item/${userId}/?prod_id=${productId}`);
            await fetchCart();
        } catch (err) {
            console.error("Ошибка удаления:", err);
            await fetchCart();
        }
    };

    const addToCart = async (productId: number) => {
        const tg = window.Telegram?.WebApp;
        const userId = tg?.initDataUnsafe?.user?.id || import.meta.env.VITE_USER_ID; 
        try {
            await axios.post(`${BASE_URL}/api/v1/cart_item/${userId}/?prod_id=${productId}`);
            tg?.HapticFeedback.notificationOccurred('success');
            await fetchCart();
            alert("Товар добавлен в корзину!");
            setSelectedProduct(null);
        } catch (err) {
            console.error("Ошибка при добавлении в корзину:", err);
        }
    };

    // --- ЛОГИКА ЗАКАЗА ---

    const handleCreateOrder = async (fullName: string, address: string) => {
        const tg = window.Telegram?.WebApp;
        const userId = tg?.initDataUnsafe?.user?.id || import.meta.env.VITE_USER_ID;
        try {
                    await axios.post(`${BASE_URL}/api/v1/order/`, {
                        tg_id: userId,
                        address: address,
                        client_full_name: fullName
                    });

                    tg?.HapticFeedback.notificationOccurred('success');
                    alert("Заказ успешно создан!");
                    
                    // Сбрасываем состояния
                    setIsOrderFormOpen(false);
                    setIsCartOpen(false);
                    setCartItems([]); // Очищаем визуально
                    fetchCart(); // Синхронизируем с бэкендом (он должен вернуть пустой список)
                } catch (err) {
                    console.error("Ошибка при создании заказа:", err);
                    alert("Ошибка оформления заказа");
                }
            };

            // --- ЛОГИКА КАТЕГОРИЙ ---

            const handleCategoryClick = async (id: number) => {
                setLoading(true);
                setSelectedSubId(id);
                const res = await axios.get(`${BASE_URL}/api/v1/products/${id}/`);
                setProducts(res.data);
                setLoading(false);
            };

            return (
                <div className="p-4 bg-[#1c1c1d] min-h-screen text-white">
                    {/* Header */}
                    <div className="flex justify-between items-center mb-6">
                        <h1 className="text-xl font-bold uppercase italic text-[#31b545]">Market</h1>
                        <button 
                            onClick={() => setIsCartOpen(true)}
                            className="w-10 h-10 bg-[#2c2c2e] rounded-full flex items-center justify-center relative active:scale-90 transition-transform"
                        >
                            🛒
                            {cartItems.length > 0 && (
                                <span className="absolute -top-1 -right-1 bg-[#31b545] text-white text-[10px] w-5 h-5 rounded-full flex items-center justify-center border-2 border-[#1c1c1d] font-bold">
                                    {cartItems.length}
                                </span>
                            )}
                        </button>
                    </div>

                    <CategoryBar 
                        categories={categories} 
                        selectedId={selectedSubId} 
                        onCategoryClick={handleCategoryClick} 
                    />

                    <div className="grid grid-cols-2 gap-3 mt-4">
                        {loading ? (
                            <div className="col-span-2 text-center py-20 text-gray-500 italic">Загрузка...</div>
                        ) : (
                            products.map((product) => (
                                <div key={product.id} onClick={() => setSelectedProduct(product)} className="cursor-pointer">
                                    <ProductCard product={product} />
                                </div>
                            ))
                        )}
                    </div>

                    {selectedProduct && (
                        <ProductModal 
                            product={selectedProduct} 
                            onClose={() => setSelectedProduct(null)} 
                            onAddToCart={addToCart}
                        />
                    )}

                    {isCartOpen && (
                        <CartModal 
                            items={cartItems} 
                            onClose={() => setIsCartOpen(false)}
                            onUpdateQuantity={handleUpdateQuantity}
                            onRemove={handleRemoveItem}
                            // Важно: прокидываем функцию открытия формы
                            onCheckout={() => setIsOrderFormOpen(true)} 
                        />
                    )}

                    {/* Модалка оформления заказа */}
                    {isOrderFormOpen && (
                        <OrderForm 
                            onClose={() => setIsOrderFormOpen(false)}
                            onSubmit={handleCreateOrder}
                        />
                    )}
                </div>
            );
        }

        export default App;