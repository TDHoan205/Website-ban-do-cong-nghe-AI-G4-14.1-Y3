/**
 * site.js – Base JavaScript for Webstore
 * Provides shared utilities, cart animations, and bootstrap enhancements
 */

(function () {
    'use strict';

    // ─── Bootstrap auto-init ────────────────────────────────
    document.addEventListener('DOMContentLoaded', function () {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.forEach(function (tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });

        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.forEach(function (popoverTriggerEl) {
            new bootstrap.Popover(popoverTriggerEl);
        });

        var alerts = document.querySelectorAll('.alert[data-auto-dismiss]');
        alerts.forEach(function (alert) {
            setTimeout(function () {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        });
    });

    // ─── Format currency helper ──────────────────────────────
    window.formatCurrency = function (amount) {
        return new Intl.NumberFormat('vi-VN').format(amount) + ' ₫';
    };

    // ─── Show toast notification ────────────────────────────
    window.showToast = function (type, message) {
        var icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        var existingToasts = document.querySelectorAll('.alert-toast');
        existingToasts.forEach(function (el) { el.remove(); });
        var toast = document.createElement('div');
        toast.className = 'alert-toast alert-toast-' + type;
        toast.innerHTML =
            '<i class="fas ' + (icons[type] || 'fa-info-circle') + '"></i>' +
            '<span style="flex:1">' + message + '</span>' +
            '<button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>';
        document.body.appendChild(toast);
        setTimeout(function () {
            if (toast.parentElement) {
                toast.style.animation = 'slideInRight 0.3s ease reverse';
                setTimeout(function () {
                    if (toast.parentElement) toast.remove();
                }, 300);
            }
        }, 3500);
    };

    // ─── Cart icon bounce animation ─────────────────────────
    window.animateCartIcon = function () {
        var badge = document.getElementById('cartCount');
        if (badge) {
            badge.style.transform = 'scale(1.8)';
            setTimeout(function () {
                badge.style.transform = 'scale(1)';
                badge.style.transition = 'transform 0.3s ease-out';
            }, 150);
        }
    };

    // ─── Add to Cart ──────────────────────────────────────
    window.addToCart = async function (productId, quantity, variantId) {
        quantity = quantity || 1;
        try {
            var body = 'productId=' + encodeURIComponent(productId) + '&quantity=' + encodeURIComponent(quantity);
            if (variantId) {
                body += '&variantId=' + encodeURIComponent(variantId);
            }

            var response = await fetch('/api/cart/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: body,
            });

            var data = await response.json();

            if (data.requiresLogin) {
                window.showToast('warning', data.message || 'Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng.');
                setTimeout(function () {
                    window.location.href = '/auth/login?return_url=' + encodeURIComponent(window.location.pathname);
                }, 1500);
                return;
            }

            if (data.success) {
                window.showToast('success', data.message || 'Đã thêm vào giỏ hàng!');
                window.updateCartCount();
                window.animateCartIcon();
            } else {
                window.showToast('error', data.message || 'Có lỗi xảy ra!');
            }
        } catch (error) {
            window.showToast('error', 'Có lỗi xảy ra!');
        }
    };

    // ─── Update Cart Count ─────────────────────────────────
    window.updateCartCount = async function () {
        try {
            var response = await fetch('/api/cart/count');
            var data = await response.json();
            var count = typeof data === 'number' ? data : (data.count || 0);
            var badge = document.getElementById('cartCount') || document.querySelector('.cart-badge');
            if (badge) {
                badge.textContent = count > 0 ? count : '';
                badge.style.display = count > 0 ? 'inline-flex' : 'none';
            }
        } catch (error) {
            // Ignore
        }
    };

    // ─── Update Cart Item ──────────────────────────────────
    window.updateCartItem = async function (productId, quantity, variantId) {
        try {
            var body = 'productId=' + encodeURIComponent(productId) + '&quantity=' + encodeURIComponent(quantity);
            if (variantId) {
                body += '&variantId=' + encodeURIComponent(variantId);
            }

            var response = await fetch('/api/cart/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: body,
            });

            var data = await response.json();
            if (data.success) {
                location.reload();
            } else {
                window.showToast('error', data.message || 'Có lỗi xảy ra!');
            }
        } catch (error) {
            window.showToast('error', 'Có lỗi xảy ra!');
        }
    };

    // ─── Remove Cart Item ───────────────────────────────────
    window.removeCartItem = async function (productId, variantId) {
        if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) return;
        try {
            var body = 'productId=' + encodeURIComponent(productId);
            if (variantId) {
                body += '&variantId=' + encodeURIComponent(variantId);
            }

            var response = await fetch('/api/cart/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: body,
            });

            var data = await response.json();
            if (data.success) {
                location.reload();
            } else {
                window.showToast('error', data.message || 'Có lỗi xảy ra!');
            }
        } catch (error) {
            window.showToast('error', 'Có lỗi xảy ra!');
        }
    };

    // ─── Clear Cart ────────────────────────────────────────
    window.clearCart = async function () {
        if (!confirm('Bạn có chắc muốn xóa toàn bộ giỏ hàng?')) return;
        try {
            var response = await fetch('/api/cart/clear', { method: 'POST' });
            var data = await response.json();
            if (data.success) {
                location.reload();
            } else {
                window.showToast('error', 'Có lỗi xảy ra!');
            }
        } catch (error) {
            window.showToast('error', 'Có lỗi xảy ra!');
        }
    };

    // ─── Fetch helper ─────────────────────────────────────
    window.apiFetch = function (url, options) {
        return fetch(url, options)
            .then(function (response) {
                if (!response.ok) {
                    throw new Error('Network error: ' + response.status);
                }
                return response.json();
            })
            .catch(function (error) {
                console.error('API Error:', error);
                window.showToast('error', 'Có lỗi xảy ra, vui lòng thử lại.');
                throw error;
            });
    };

    // ─── Debounce utility ─────────────────────────────────
    window.debounce = function (func, wait) {
        var timeout;
        return function () {
            var args = arguments;
            var context = this;
            clearTimeout(timeout);
            timeout = setTimeout(function () {
                func.apply(context, args);
            }, wait);
        };
    };

    // ─── Format price helper for JS ───────────────────────
    window.formatPrice = function (amount) {
        return new Intl.NumberFormat('vi-VN', {
            style: 'currency',
            currency: 'VND',
            minimumFractionDigits: 0
        }).format(amount).replace('₫', 'đ');
    };

})();
