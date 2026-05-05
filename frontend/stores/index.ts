import { create } from "zustand";
import { persist } from "zustand/middleware";
import api from "@/lib/api";
import { User, Cart } from "@/lib/types";

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (username: string, password: string) => {
        set({ isLoading: true });
        try {
          const formData = new URLSearchParams();
          formData.append("username", username);
          formData.append("password", password);

          const response = await api.post("/auth/login", formData.toString(), {
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
          });

          const { access_token, user } = response.data;
          localStorage.setItem("access_token", access_token);

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      register: async (data: RegisterData) => {
        set({ isLoading: true });
        try {
          const response = await api.post("/auth/register", data);
          const { access_token, user } = response.data;
          localStorage.setItem("access_token", access_token);

          set({
            user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },

      logout: () => {
        localStorage.removeItem("access_token");
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      fetchUser: async () => {
        const token = get().token;
        if (!token) return;

        try {
          const response = await api.get("/auth/me");
          set({ user: response.data, isAuthenticated: true });
        } catch {
          get().logout();
        }
      },
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

interface CartState {
  cart: Cart | null;
  isLoading: boolean;
  fetchCart: () => Promise<void>;
  addToCart: (productId: number, variantId?: number, quantity?: number) => Promise<void>;
  updateQuantity: (productId: number, variantId: number | null, quantity: number) => Promise<void>;
  removeFromCart: (productId: number, variantId: number | null) => Promise<void>;
  clearCart: () => Promise<void>;
}

export const useCartStore = create<CartState>((set, get) => ({
  cart: null,
  isLoading: false,

  fetchCart: async () => {
    set({ isLoading: true });
    try {
      const sessionId = localStorage.getItem("session_id");
      const response = await api.get("/cart/", {
        params: { session_id: sessionId },
      });
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
    }
  },

  addToCart: async (productId: number, variantId?: number, quantity: number = 1) => {
    set({ isLoading: true });
    try {
      const sessionId = localStorage.getItem("session_id");
      const response = await api.post("/cart/add", {
        product_id: productId,
        variant_id: variantId,
        quantity,
      }, {
        params: { session_id: sessionId },
      });
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  updateQuantity: async (productId: number, variantId: number | null, quantity: number) => {
    set({ isLoading: true });
    try {
      const sessionId = localStorage.getItem("session_id");
      const response = await api.put(
        `/cart/update/${productId}`,
        { quantity },
        { params: { variant_id: variantId, session_id: sessionId } }
      );
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  removeFromCart: async (productId: number, variantId: number | null) => {
    set({ isLoading: true });
    try {
      const sessionId = localStorage.getItem("session_id");
      const response = await api.delete(`/cart/remove/${productId}`, {
        params: { variant_id: variantId, session_id: sessionId },
      });
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },

  clearCart: async () => {
    set({ isLoading: true });
    try {
      const sessionId = localStorage.getItem("session_id");
      const response = await api.delete("/cart/clear", {
        params: { session_id: sessionId },
      });
      set({ cart: response.data, isLoading: false });
    } catch (error) {
      set({ isLoading: false });
      throw error;
    }
  },
}));
