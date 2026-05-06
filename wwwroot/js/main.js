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
            },
            body: `quantity=${quantity}`
        });

        if (response.redirected) {
            showNotification('Đã thêm vào giỏ hàng!', 'success');
            updateCartCount();
        }
    } catch (error) {
        showNotification('Có lỗi xảy ra!', 'danger');
    }
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

async function updateCartCount() {
    try {
        const response = await fetch('/Cart/Count');
        const data = await response.json();
        const badge = document.querySelector('.navbar .badge');
        if (badge) {
            badge.textContent = data.count || 0;
        }
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
