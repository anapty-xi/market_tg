import { useState } from 'react';

interface Props {
    onClose: () => void;
    onSubmit: (fullName: string, address: string) => void;
}

export const OrderForm = ({ onClose, onSubmit }: Props) => {
    const [fullName, setFullName] = useState('');
    const [address, setAddress] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (fullName.trim() && address.trim()) {
            onSubmit(fullName, address);
        } else {
            alert('Пожалуйста, заполните все поля');
        }
    };

    return (
        <div className="fixed inset-0 z-[70] bg-[#1c1c1d] flex flex-col animate-in fade-in duration-200">
            <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <button onClick={onClose} className="text-[#31b545] font-bold">← Назад</button>
                <h2 className="text-lg font-bold">Оформление</h2>
                <div className="w-10"></div>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
                <div>
                    <label className="block text-gray-400 text-sm mb-2">ФИО получателя</label>
                    <input 
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="Иванов Иван Иванович"
                        className="w-full bg-[#2c2c2e] border border-gray-700 rounded-xl p-4 text-white focus:border-[#31b545] outline-none transition-all"
                    />
                </div>

                <div>
                    <label className="block text-gray-400 text-sm mb-2">Адрес доставки</label>
                    <textarea 
                        value={address}
                        onChange={(e) => setAddress(e.target.value)}
                        placeholder="Город, улица, дом, квартира"
                        className="w-full bg-[#2c2c2e] border border-gray-700 rounded-xl p-4 text-white focus:border-[#31b545] outline-none transition-all h-32 resize-none"
                    />
                </div>

                <button 
                    type="submit"
                    className="w-full bg-[#31b545] text-white py-4 rounded-2xl font-bold text-lg active:scale-95 transition-all shadow-lg shadow-[#31b545]/20"
                >
                    Подтвердить заказ
                </button>
            </form>
        </div>
    );
};