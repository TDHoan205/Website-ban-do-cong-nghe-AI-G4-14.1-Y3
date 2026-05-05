import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";
import { Product, Category } from "@/lib/types";

export function useProducts(params?: {
  search?: string;
  category_id?: number;
  sort_by?: string;
  page?: number;
  page_size?: number;
  filter?: string;
}) {
  return useQuery({
    queryKey: ["products", params],
    queryFn: async () => {
      const response = await api.get("/products/", { params });
      return response.data;
    },
  });
}

export function useProduct(id: number) {
  return useQuery({
    queryKey: ["product", id],
    queryFn: async () => {
      const response = await api.get(`/products/${id}`);
      return response.data as Product;
    },
    enabled: !!id,
  });
}

export function useFeaturedProducts(type: string = "new", count: number = 10) {
  return useQuery({
    queryKey: ["featured-products", type, count],
    queryFn: async () => {
      const response = await api.get("/products/featured", {
        params: { type, count },
      });
      return response.data as Product[];
    },
  });
}

export function useSearchProducts(query: string, count: number = 10) {
  return useQuery({
    queryKey: ["search-products", query],
    queryFn: async () => {
      const response = await api.get("/products/search", {
        params: { q: query, count },
      });
      return response.data as Product[];
    },
    enabled: query.length >= 2,
  });
}

export function useCategories() {
  return useQuery({
    queryKey: ["categories"],
    queryFn: async () => {
      const response = await api.get("/categories/");
      return response.data as Category[];
    },
  });
}

export function useOrders(params?: { page?: number; page_size?: number; status?: string }) {
  return useQuery({
    queryKey: ["orders", params],
    queryFn: async () => {
      const response = await api.get("/orders/", { params });
      return response.data;
    },
  });
}

export function useOrder(id: number) {
  return useQuery({
    queryKey: ["order", id],
    queryFn: async () => {
      const response = await api.get(`/orders/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
}

export function useCreateOrder() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: {
      customer_name?: string;
      customer_phone?: string;
      customer_address?: string;
      notes?: string;
    }) => {
      const response = await api.post("/orders/", data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orders"] });
    },
  });
}
