"use client";

import { useState } from "react";
import { useProducts, useCategories } from "@/hooks/useApi";
import { formatPrice } from "@/lib/utils";
import { Star, Filter, Search, ChevronLeft, ChevronRight } from "lucide-react";
import Link from "next/link";

export default function ProductsPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [categoryId, setCategoryId] = useState<number | undefined>();
  const [sortBy, setSortBy] = useState("newest");
  const [filter, setFilter] = useState<string | undefined>();
  const [showFilters, setShowFilters] = useState(false);

  const { data, isLoading } = useProducts({
    search: search || undefined,
    category_id: categoryId,
    sort_by: sortBy,
    page,
    page_size: 12,
    filter,
  });

  const { data: categories } = useCategories();

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Sidebar */}
        <aside className={`w-full md:w-64 ${showFilters ? "block" : "hidden md:block"}`}>
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="font-semibold mb-4">Danh mục</h3>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => setCategoryId(undefined)}
                  className={`w-full text-left px-3 py-2 rounded ${
                    !categoryId ? "bg-blue-50 text-blue-600" : "hover:bg-gray-100"
                  }`}
                >
                  Tất cả sản phẩm
                </button>
              </li>
              {categories?.map((cat) => (
                <li key={cat.category_id}>
                  <button
                    onClick={() => setCategoryId(cat.category_id)}
                    className={`w-full text-left px-3 py-2 rounded ${
                      categoryId === cat.category_id
                        ? "bg-blue-50 text-blue-600"
                        : "hover:bg-gray-100"
                    }`}
                  >
                    {cat.name}
                  </button>
                </li>
              ))}
            </ul>

            <h3 className="font-semibold mt-6 mb-4">Bộ lọc</h3>
            <div className="space-y-2">
              {[
                { value: undefined, label: "Tất cả" },
                { value: "new", label: "Hàng mới" },
                { value: "hot", label: "Hot deal" },
                { value: "deal", label: "Giảm giá" },
              ].map((f) => (
                <button
                  key={f.value || "all"}
                  onClick={() => setFilter(f.value)}
                  className={`w-full text-left px-3 py-2 rounded ${
                    filter === f.value ? "bg-blue-50 text-blue-600" : "hover:bg-gray-100"
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <div className="flex-1">
          {/* Search & Sort */}
          <div className="bg-white rounded-lg shadow-sm p-4 mb-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Tìm kiếm sản phẩm..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="md:hidden p-2 border rounded-lg"
                >
                  <Filter className="w-5 h-5" />
                </button>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="newest">Mới nhất</option>
                  <option value="price">Giá: Thấp → Cao</option>
                  <option value="price_desc">Giá: Cao → Thấp</option>
                  <option value="name">Tên: A → Z</option>
                </select>
              </div>
            </div>
          </div>

          {/* Results */}
          {isLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {Array(8)
                .fill(0)
                .map((_, i) => (
                  <div key={i} className="bg-white rounded-lg overflow-hidden animate-pulse">
                    <div className="aspect-square bg-gray-200" />
                    <div className="p-4">
                      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                      <div className="h-6 bg-gray-200 rounded w-2/3" />
                    </div>
                  </div>
                ))}
            </div>
          ) : data?.items.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-gray-500 text-lg">Không tìm thấy sản phẩm nào</p>
            </div>
          ) : (
            <>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {data?.items.map((product: any) => (
                  <Link key={product.product_id} href={`/products/${product.product_id}`}>
                    <div className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-lg transition-shadow">
                      <div className="relative">
                        <div className="aspect-square bg-gray-200" />
                        {product.discount_percent > 0 && (
                          <span className="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded">
                            -{product.discount_percent}%
                          </span>
                        )}
                        {product.is_new && (
                          <span className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded">
                            Mới
                          </span>
                        )}
                      </div>
                      <div className="p-4">
                        <p className="text-xs text-gray-500 mb-1">{product.category_name}</p>
                        <h3 className="font-medium text-sm line-clamp-2 h-10 mb-2">
                          {product.name}
                        </h3>
                        <div className="flex items-center mb-2">
                          {Array(5)
                            .fill(0)
                            .map((_, i) => (
                              <Star
                                key={i}
                                className={`w-4 h-4 ${
                                  i < product.rating
                                    ? "text-yellow-400 fill-yellow-400"
                                    : "text-gray-300"
                                }`}
                              />
                            ))}
                        </div>
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="text-lg font-bold text-blue-600">
                              {formatPrice(product.price)}
                            </span>
                            {product.original_price && product.original_price > product.price && (
                              <span className="text-sm text-gray-400 line-through ml-1">
                                {formatPrice(product.original_price)}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                ))}
              </div>

              {/* Pagination */}
              {data && data.total_pages > 1 && (
                <div className="flex justify-center items-center space-x-2 mt-8">
                  <button
                    onClick={() => setPage(page - 1)}
                    disabled={page === 1}
                    className="p-2 border rounded-lg disabled:opacity-50 hover:bg-gray-100"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  <span className="px-4">
                    Trang {page} / {data.total_pages}
                  </span>
                  <button
                    onClick={() => setPage(page + 1)}
                    disabled={page === data.total_pages}
                    className="p-2 border rounded-lg disabled:opacity-50 hover:bg-gray-100"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
