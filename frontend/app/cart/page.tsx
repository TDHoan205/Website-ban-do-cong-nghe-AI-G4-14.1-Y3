"use client";

import { useEffect } from "react";
import { useCartStore, useAuthStore } from "@/stores";
import { formatPrice } from "@/lib/utils";
import Link from "next/link";
import { Trash2, Minus, Plus, ShoppingBag, ArrowRight } from "lucide-react";

export default function CartPage() {
  const { cart, fetchCart, updateQuantity, removeFromCart, isLoading } = useCartStore();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  if (isLoading && !cart) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8" />
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-32 bg-gray-200 rounded" />
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (!cart || cart.items.length === 0) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <ShoppingBag className="w-24 h-24 mx-auto text-gray-300 mb-4" />
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Giỏ hàng trống</h1>
        <p className="text-gray-500 mb-6">Hãy thêm sản phẩm vào giỏ hàng của bạn</p>
        <Link
          href="/products"
          className="inline-flex items-center bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700"
        >
          Tiếp tục mua sắm
          <ArrowRight className="ml-2 w-5 h-5" />
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-8">Giỏ hàng của bạn ({cart.item_count} sản phẩm)</h1>

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Cart Items */}
        <div className="lg:col-span-2 space-y-4">
          {cart.items.map((item) => (
            <div key={`${item.product_id}-${item.variant_id}`} className="bg-white rounded-lg shadow-sm p-4 flex gap-4">
              <div className="w-24 h-24 bg-gray-200 rounded-lg flex-shrink-0">
                {item.product_image && (
                  <img
                    src={item.product_image}
                    alt={item.product_name}
                    className="w-full h-full object-cover rounded-lg"
                  />
                )}
              </div>
              <div className="flex-1">
                <h3 className="font-medium">{item.product_name}</h3>
                {item.variant_name && (
                  <p className="text-sm text-gray-500">{item.variant_name}</p>
                )}
                <p className="text-lg font-bold text-blue-600 mt-1">
                  {formatPrice(item.unit_price || 0)}
                </p>
              </div>
              <div className="flex flex-col items-end justify-between">
                <button
                  onClick={() => removeFromCart(item.product_id, item.variant_id || null)}
                  className="text-gray-400 hover:text-red-500"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => updateQuantity(item.product_id, item.variant_id || null, item.quantity - 1)}
                    disabled={item.quantity <= 1}
                    className="p-1 border rounded hover:bg-gray-100 disabled:opacity-50"
                  >
                    <Minus className="w-4 h-4" />
                  </button>
                  <span className="w-8 text-center font-medium">{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.product_id, item.variant_id || null, item.quantity + 1)}
                    className="p-1 border rounded hover:bg-gray-100"
                  >
                    <Plus className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Order Summary */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-sm p-6 sticky top-24">
            <h2 className="text-lg font-bold mb-4">Tổng cộng</h2>
            <div className="space-y-3 pb-4 border-b">
              <div className="flex justify-between">
                <span className="text-gray-600">Tạm tính ({cart.item_count} sản phẩm)</span>
                <span className="font-medium">{formatPrice(cart.total_amount)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Giảm giá</span>
                <span className="font-medium text-green-600">-0đ</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Phí vận chuyển</span>
                <span className="font-medium">{cart.total_amount >= 500000 ? "Miễn phí" : "30,000đ"}</span>
              </div>
            </div>
            <div className="flex justify-between py-4">
              <span className="text-lg font-bold">Tổng cộng</span>
              <span className="text-lg font-bold text-blue-600">
                {formatPrice(
                  cart.total_amount + (cart.total_amount < 500000 ? 30000 : 0)
                )}
              </span>
            </div>
            {!isAuthenticated && (
              <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-lg mb-4">
                <p className="text-sm">
                  Bạn đang mua hàng với tư cách khách.{" "}
                  <Link href="/login" className="underline font-medium">
                    Đăng nhập
                  </Link>{" "}
                  để lưu thông tin đơn hàng.
                </p>
              </div>
            )}
            <Link
              href="/checkout"
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 flex items-center justify-center"
            >
              Tiến hành đặt hàng
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link
              href="/products"
              className="w-full border border-gray-300 py-3 rounded-lg font-semibold hover:bg-gray-50 flex items-center justify-center mt-3"
            >
              Tiếp tục mua sắm
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
