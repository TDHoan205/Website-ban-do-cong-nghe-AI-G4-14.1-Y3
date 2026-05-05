import Link from "next/link";
import { useFeaturedProducts } from "@/hooks/useApi";
import { formatPrice } from "@/lib/utils";
import { Star, ShoppingCart, Zap, Flame, Gift } from "lucide-react";

export default function HomePage() {
  const { data: newProducts, isLoading: loadingNew } = useFeaturedProducts("new", 8);
  const { data: hotProducts, isLoading: loadingHot } = useFeaturedProducts("hot", 8);
  const { data: dealProducts, isLoading: loadingDeal } = useFeaturedProducts("deal", 8);

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white">
        <div className="max-w-7xl mx-auto px-4 py-20">
          <div className="grid md:grid-cols-2 gap-8 items-center">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                Cửa hàng công nghệ hàng đầu
              </h1>
              <p className="text-xl mb-6 text-blue-100">
                Khám phá các sản phẩm công nghệ mới nhất với AI hỗ trợ mua sắm thông minh
              </p>
              <div className="flex space-x-4">
                <Link
                  href="/products"
                  className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-blue-50"
                >
                  Mua sắm ngay
                </Link>
                <Link
                  href="/chat"
                  className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white/10"
                >
                  Chat với AI
                </Link>
              </div>
            </div>
            <div className="hidden md:block">
              <div className="bg-white/10 rounded-2xl p-8 backdrop-blur">
                <h3 className="text-2xl font-bold mb-4">Tại sao chọn TechStore?</h3>
                <ul className="space-y-3">
                  <li className="flex items-center">
                    <Zap className="w-5 h-5 mr-3 text-yellow-400" />
                    Sản phẩm chính hãng 100%
                  </li>
                  <li className="flex items-center">
                    <Gift className="w-5 h-5 mr-3 text-green-400" />
                    Giá cả cạnh tranh nhất
                  </li>
                  <li className="flex items-center">
                    <Flame className="w-5 h-5 mr-3 text-orange-400" />
                    Hỗ trợ AI 24/7
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: "🚚", title: "Miễn phí vận chuyển", desc: "Đơn hàng từ 500K" },
              { icon: "🔄", title: "Đổi trả dễ dàng", desc: "Trong 7 ngày" },
              { icon: "💳", title: "Thanh toán an toàn", desc: "Nhiều hình thức" },
              { icon: "🎧", title: "Hỗ trợ 24/7", desc: "Chat với AI" },
            ].map((item, i) => (
              <div key={i} className="text-center p-4">
                <div className="text-4xl mb-2">{item.icon}</div>
                <h3 className="font-semibold">{item.title}</h3>
                <p className="text-sm text-gray-500">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* New Products */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold">Sản phẩm mới</h2>
            <Link href="/products?filter=new" className="text-blue-600 hover:underline">
              Xem tất cả →
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {loadingNew
              ? Array(4)
                  .fill(0)
                  .map((_, i) => <ProductSkeleton key={i} />)
              : newProducts?.slice(0, 4).map((p) => <ProductCard key={p.product_id} product={p} />)}
          </div>
        </div>
      </section>

      {/* Hot Products */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center">
              <Flame className="w-6 h-6 text-red-500 mr-2" />
              <h2 className="text-2xl font-bold">Hot deals</h2>
            </div>
            <Link href="/products?filter=hot" className="text-blue-600 hover:underline">
              Xem tất cả →
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {loadingHot
              ? Array(4)
                  .fill(0)
                  .map((_, i) => <ProductSkeleton key={i} />)
              : hotProducts?.slice(0, 4).map((p) => <ProductCard key={p.product_id} product={p} />)}
          </div>
        </div>
      </section>

      {/* Deal Products */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center">
              <Gift className="w-6 h-6 text-green-500 mr-2" />
              <h2 className="text-2xl font-bold">Giảm giá</h2>
            </div>
            <Link href="/products?filter=deal" className="text-blue-600 hover:underline">
              Xem tất cả →
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {loadingDeal
              ? Array(4)
                  .fill(0)
                  .map((_, i) => <ProductSkeleton key={i} />)
              : dealProducts?.slice(0, 4).map((p) => <ProductCard key={p.product_id} product={p} />)}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-blue-600 text-white text-center">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold mb-4">Bạn cần tư vấn?</h2>
          <p className="text-xl mb-6 text-blue-100">
            Trò chuyện với AI assistant của chúng tôi để được hỗ trợ 24/7
          </p>
          <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50">
            Bắt đầu chat ngay
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">TechStore</h3>
              <p className="text-gray-400">
                Cửa hàng công nghệ hàng đầu Việt Nam với AI hỗ trợ mua sắm thông minh.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Liên kết</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/products">Sản phẩm</Link></li>
                <li><Link href="/about">Giới thiệu</Link></li>
                <li><Link href="/contact">Liên hệ</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Hỗ trợ</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/faq">FAQ</Link></li>
                <li><Link href="/shipping">Vận chuyển</Link></li>
                <li><Link href="/returns">Đổi trả</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Liên hệ</h4>
              <ul className="space-y-2 text-gray-400">
                <li>📞 1800-1234</li>
                <li>✉️ support@techstore.vn</li>
                <li>📍 123 Nguyễn Trãi, Q1, TP.HCM</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            © 2024 TechStore. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}

function ProductCard({ product }: { product: any }) {
  return (
    <Link href={`/products/${product.product_id}`}>
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
          <h3 className="font-medium text-sm line-clamp-2 h-10">{product.name}</h3>
          <div className="flex items-center mt-1">
            {Array(5)
              .fill(0)
              .map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < product.rating ? "text-yellow-400 fill-yellow-400" : "text-gray-300"
                  }`}
                />
              ))}
          </div>
          <div className="mt-2">
            <span className="text-lg font-bold text-blue-600">{formatPrice(product.price)}</span>
            {product.original_price && product.original_price > product.price && (
              <span className="text-sm text-gray-400 line-through ml-2">
                {formatPrice(product.original_price)}
              </span>
            )}
          </div>
        </div>
      </div>
    </Link>
  );
}

function ProductSkeleton() {
  return (
    <div className="bg-white rounded-lg overflow-hidden animate-pulse">
      <div className="aspect-square bg-gray-200" />
      <div className="p-4">
        <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
        <div className="h-4 bg-gray-200 rounded w-1/2" />
        <div className="h-6 bg-gray-200 rounded w-2/3 mt-2" />
      </div>
    </div>
  );
}
