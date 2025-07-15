import { create } from "zustand";

/**
 * Global chat store to monitor authentication and cart management
 * Used across chat helpers
 */

export type ChatStore = {
  userId: string | null;
  username: string | null;
  cartId: string | null;
  setUserId: (userId: string) => void;
  setUsername: (username: string) => void;
  setCartId: (cartId: string) => void;
};

export const useChatStore = create<ChatStore>((set) => ({
  userId: null,
  username: null,
  cartId: null,
  setUserId: (userId: string) => set({ userId }),
  setUsername: (username: string) => set({ username }),
  setCartId: (cartId: string) => set({ cartId }),
}));
