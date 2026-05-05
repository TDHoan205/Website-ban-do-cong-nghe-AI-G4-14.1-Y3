export interface User {
  user_id: number;
  username: string;
  email?: string;
  full_name?: string;
  phone?: string;
  address?: string;
  is_active: boolean;
  role_id: number;
  role_name?: string;
}

export interface Product {
  product_id: number;
  name: string;
  description?: string;
  image_url?: string;
  price: number;
  original_price?: number;
  stock_quantity: number;
  is_available: boolean;
  rating: number;
  is_new: boolean;
  is_hot: boolean;
  discount_percent: number;
  specifications?: string;
  category_id?: number;
  supplier_id?: number;
  category_name?: string;
  supplier_name?: string;
  variants: ProductVariant[];
  images: ProductImage[];
  created_at?: string;
}

export interface ProductVariant {
  variant_id: number;
  product_id: number;
  color?: string;
  storage?: string;
  ram?: string;
  variant_name?: string;
  sku?: string;
  price?: number;
  original_price?: number;
  stock_quantity: number;
}

export interface ProductImage {
  image_id: number;
  product_id: number;
  image_url: string;
  display_order: number;
  is_primary: boolean;
}

export interface Category {
  category_id: number;
  name: string;
  description?: string;
  created_at?: string;
}

export interface CartItem {
  cart_item_id: number;
  cart_id: number;
  product_id: number;
  variant_id?: number;
  quantity: number;
  added_date?: string;
  product_name?: string;
  product_image?: string;
  variant_name?: string;
  unit_price?: number;
}

export interface Cart {
  cart_id: number;
  user_id?: number;
  session_id?: string;
  items: CartItem[];
  total_amount: number;
  item_count: number;
  created_at?: string;
}

export interface Order {
  order_id: number;
  user_id?: number;
  order_date?: string;
  total_amount: number;
  status: string;
  customer_name?: string;
  customer_phone?: string;
  customer_address?: string;
  notes?: string;
  items: OrderItem[];
  created_at?: string;
}

export interface OrderItem {
  order_item_id: number;
  order_id: number;
  product_id: number;
  variant_id?: number;
  quantity: number;
  unit_price: number;
  product_name?: string;
  product_image?: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
  suggested_products?: Product[];
}

export interface ChatResponse {
  response: string;
  session_id: string;
  intent?: string;
  action?: Record<string, unknown>;
  suggested_products?: Product[];
  timestamp: string;
}
