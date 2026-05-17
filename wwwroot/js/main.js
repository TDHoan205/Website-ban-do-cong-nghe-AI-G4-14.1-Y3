/*
Tech Store - Main JavaScript
*/

// =====================================================
// Cart Functions
// =====================================================

async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch(`/Products/${productId}/add-to-cart`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new URLSearchParams({ quantity })
        });
        const data = await response.json();

        if (response.status === 401 && data.login_url) {
            window.location.href = data.login_url;
            return;
        }

        if (response.ok && data.success) {
            showNotification(data.message || 'Đã thêm vào giỏ hàng!', 'success');
            updateCartCount(data.cart_count);
            return;
        }

        showNotification(data.message || 'Có lỗi xảy ra!', 'danger');
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    }
}

async function submitAddToCartForm(form) {
    const button = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);

    if (button) {
        button.disabled = true;
        button.dataset.originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang thêm...';
    }

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: new URLSearchParams(formData)
        });
        const data = await response.json();

        if (response.status === 401 && data.login_url) {
            window.location.href = data.login_url;
            return;
        }

        if (response.ok && data.success) {
            showNotification(data.message || 'Đã thêm vào giỏ hàng!', 'success');
            updateCartCount(data.cart_count);
            return;
        }

        showNotification(data.message || 'Có lỗi xảy ra!', 'danger');
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    } finally {
        if (button) {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText;
        }
    }
}

function handleAddToCartSubmit(event, form) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    submitAddToCartForm(form);
    return false;
}

async function updateCartItem(itemId, quantity) {
    try {
        const response = await fetch(`/Cart/update/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `quantity=${quantity}`
        });

        if (response.redirected) {
            location.reload();
        }
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    }
}

async function removeCartItem(itemId) {
    if (!confirm('Bạn có chắc muốn xóa sản phẩm này?')) return;

    try {
        const response = await fetch(`/Cart/remove/${itemId}`, {
            method: 'POST'
        });

        if (response.redirected) {
            location.reload();
        }
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    }
}

async function clearCart() {
    if (!confirm('Bạn có chắc muốn xóa toàn bộ giỏ hàng?')) return;

    try {
        const response = await fetch('/Cart/clear', {
            method: 'POST'
        });

        if (response.redirected) {
            location.reload();
        }
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    }
}

// =====================================================
// Notification
// =====================================================

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} position-fixed animate__animated animate__fadeInRight`;
    notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 250px;';
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close float-end" onclick="this.parentElement.remove()"></button>
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.remove('animate__fadeInRight');
        notification.classList.add('animate__fadeOutRight');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

// =====================================================
// Cart Count
// =====================================================

async function updateCartCount(count = null) {
    try {
        if (count === null) {
            const response = await fetch('/Cart/Count', {
                headers: {
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });
            const data = await response.json();
            count = data.count || 0;
        }

        document
            .querySelectorAll('.header-action-badge, .navbar .badge, [data-cart-count]')
            .forEach((badge) => {
                badge.textContent = count || 0;
            });
    } catch (error) {
        // Ignore
    }
}

// =====================================================
// Search
// =====================================================

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = searchInput.closest('form');
                form.submit();
            }
        });
    }

    // Update cart count on page load
    updateCartCount();
});

document.addEventListener('submit', (event) => {
    const form = event.target.closest('form[action*="/add-to-cart"]');
    if (!form) return;

    handleAddToCartSubmit(event, form);
}, true);

// =====================================================
// Product Quick View
// =====================================================

function quickView(productId) {
    window.location.href = `/Products/${productId}`;
}

// =====================================================
// Format Currency
// =====================================================

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN').format(amount) + ' đ';
}
