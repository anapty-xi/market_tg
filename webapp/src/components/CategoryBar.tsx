import type { Category } from '../types';

interface Props {
    categories: Category[];
    selectedId: number;
    onCategoryClick: (id: number) => void;
}

export const CategoryBar = ({ categories, selectedId, onCategoryClick }: Props) => {
    return (
        <div className="flex gap-2 overflow-x-auto pb-4 no-scrollbar">
            <button 
                onClick={() => onCategoryClick(0)}
                className={`px-4 py-1 rounded-full text-sm whitespace-nowrap ${selectedId === 0 ? 'bg-[#31b545] text-white' : 'bg-[#2c2c2e]'}`}
            >
                Все
            </button>
            {categories.map(cat => (
                <button 
                    key={cat.id}
                    onClick={() => onCategoryClick(cat.id)}
                    className={`px-4 py-1 rounded-full text-sm whitespace-nowrap ${selectedId === cat.id ? 'bg-[#31b545] text-white' : 'bg-[#2c2c2e]'}`}
                >
                    {cat.name}
                </button>
            ))}
        </div>
    );
};