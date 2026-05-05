"use client";

import Link from "next/link";
import { useAuthStore, useCartStore } from "@/stores";
import { useEffect } from "react";
import { ShoppingCart, User, Menu, X, LogOut } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const { cart, fetchCart } = useCartStore();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-2xl font-bold text-blue-600">Tech</span>
            <span className="text-2xl font-bold text-gray-800">Store</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/products" className="text-gray-700 hover:text-blue-600">
              Sản phẩm
            </Link>
            <Link href="/products?filter=new" className="text-gray-700 hover:text-blue-600">
              Hàng mới
            </Link>
            <Link href="/products?filter=hot" className="text-gray-700 hover:text-blue-600">
              Hot deal
            </Link>
            <Link href="/products?filter=deal" className="text-gray-700 hover:text-blue-600">
              Giảm giá
            </Link>
          </div>

          {/* Right Side */}
          <div className="flex items-center space-x-4">
            {/* Cart */}
            <Link href="/cart" className="relative p-2 text-gray-700 hover:text-blue-600">
              <ShoppingCart className="w-6 h-6" />
              {cart && cart.item_count > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {cart.item_count}
                </span>
              )}
            </Link>

            {/* Auth */}
            {isAuthenticated ? (
              <div className="relative group">
                <button className="flex items-center space-x-2 p-2 text-gray-700 hover:text-blue-600">
                  <User className="w-6 h-6" />
                  <span className="hidden md:inline">{user?.full_name || user?.username}</span>
                </button>
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
                  <Link href="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    Tài khoản
                  </Link>
                  <Link href="/orders" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                    Đơn hàng
                  </Link>
                  {(user?.role_name === "Admin" || user?.role_name === "Staff") && (
                    <Link href="/admin" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      Quản trị
                    </Link>
                  )}
                  <button
                    onClick={logout}
                    className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 flex items-center"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    Đăng xuất
                  </button>
                </div>
              </div>
            ) : (
              <Link
                href="/login"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Đăng nhập
              </Link>
            )}

            {/* Mobile Menu Button */}
            <button
              className="md:hidden p-2 text-gray-700"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <Link href="/products" className="block py-2 text-gray-700">
              Sản phẩm
            </Link>
            <Link href="/products?filter=new" className="block py-2 text-gray-700">
              Hàng mới
            </Link>
            <Link href="/products?filter=hot" className="block py-2 text-gray-700">
              Hot deal
            </Link>
            <Link href="/products?filter=deal" className="block py-2 text-gray-700">
              Giảm giá
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}
