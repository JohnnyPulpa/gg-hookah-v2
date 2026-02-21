import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { Mix, Drink } from '../types';
import { getAvailability } from '../api/orders';

export interface CartItem {
  mix: Mix;
  quantity: number;
}

export interface DrinkSelection {
  drink: Drink;
  qty: number;
}

interface CartContextType {
  items: CartItem[];
  drinks: DrinkSelection[];
  addItem: (mix: Mix) => void;
  removeItem: (mixId: string) => void;
  clearCart: () => void;
  setDrinks: (drinks: DrinkSelection[]) => void;
  clearDrinks: () => void;
  totalHookahs: number;
  totalPrice: number;
  maxHookahs: number;
  availableHookahs: number;
  soldOut: boolean;
  isLoading: boolean;
  refreshAvailability: () => void;
}

const CartContext = createContext<CartContextType | null>(null);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [drinks, setDrinksState] = useState<DrinkSelection[]>([]);
  const [maxHookahs, setMaxHookahs] = useState(3);
  const [availableHookahs, setAvailableHookahs] = useState(5);
  const [isLoading, setIsLoading] = useState(true);

  const fetchAvailability = useCallback(() => {
    getAvailability()
      .then((data) => {
        setAvailableHookahs(data.available);
        setMaxHookahs(data.max_per_order);
      })
      .catch(() => {})
      .finally(() => setIsLoading(false));
  }, []);

  useEffect(() => {
    fetchAvailability();
  }, [fetchAvailability]);

  const totalHookahs = items.reduce((sum, i) => sum + i.quantity, 0);
  const totalPrice = items.reduce((sum, i) => sum + i.mix.price * i.quantity, 0);
  const soldOut = availableHookahs === 0;

  const addItem = (mix: Mix) => {
    const cap = Math.min(maxHookahs, availableHookahs);
    if (totalHookahs >= cap) return;

    setItems((prev) => {
      const existing = prev.find((i) => i.mix.id === mix.id);
      if (existing) {
        return prev.map((i) =>
          i.mix.id === mix.id ? { ...i, quantity: i.quantity + 1 } : i
        );
      }
      return [...prev, { mix, quantity: 1 }];
    });
  };

  const removeItem = (mixId: string) => {
    setItems((prev) => {
      const existing = prev.find((i) => i.mix.id === mixId);
      if (!existing) return prev;
      if (existing.quantity <= 1) {
        return prev.filter((i) => i.mix.id !== mixId);
      }
      return prev.map((i) =>
        i.mix.id === mixId ? { ...i, quantity: i.quantity - 1 } : i
      );
    });
  };

  const clearCart = () => {
    setItems([]);
    setDrinksState([]);
  };

  const setDrinks = (d: DrinkSelection[]) => setDrinksState(d);
  const clearDrinks = () => setDrinksState([]);

  return (
    <CartContext.Provider
      value={{
        items,
        drinks,
        addItem,
        removeItem,
        clearCart,
        setDrinks,
        clearDrinks,
        totalHookahs,
        totalPrice,
        maxHookahs,
        availableHookahs,
        soldOut,
        isLoading,
        refreshAvailability: fetchAvailability,
      }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart(): CartContextType {
  const ctx = useContext(CartContext);
  if (!ctx) {
    throw new Error('useCart must be used inside CartProvider');
  }
  return ctx;
}
