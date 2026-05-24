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

        const contentType = response.headers.get('Content-Type') || '';
        if (!contentType.includes('application/json')) {
            console.debug('[Cart] Non-JSON response from addToCart. Status:', response.status);
            if (response.redirected) {
                window.location.href = response.url;
            }
            return;
        }

        const data = await response.json();
        console.debug('[Cart] addToCart response:', data);

        if (response.status === 401 && data.login_url) {
            window.location.href = data.login_url;
            return;
        }

        if (response.ok && data.success) {
            const msg = (data.message !== undefined && data.message !== null && data.message !== '')
                ? data.message
                : 'Đã thêm sản phẩm vào giỏ hàng!';
            showNotification(msg, 'success');
            updateCartCount(data.cart_count);
            return;
        }

        const errMsg = (data.message !== undefined && data.message !== null && data.message !== '')
            ? data.message
            : 'Có lỗi xảy ra!';
        showNotification(errMsg, 'danger');
    } catch (error) {
        console.error('[Cart] addToCart error:', error);
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

        // ─── Validate JSON response ───
        const contentType = response.headers.get('Content-Type') || '';
        if (!contentType.includes('application/json')) {
            // Server returned HTML/redirect — treat as success (redirect happened)
            console.debug('[Cart] Non-JSON response, page probably redirected. Status:', response.status);
            if (response.redirected || response.status === 303) {
                window.location.href = response.url || form.action;
            }
            return;
        }

        const data = await response.json();
        console.debug('[Cart] Response:', data);
        // TEMPORARY DEBUG: show raw server response in an alert
        window.__lastCartResponse = data;

        if (response.status === 401 && data.login_url) {
            window.location.href = data.login_url;
            return;
        }

        if (response.ok && data.success) {
            const msg = (data.message !== undefined && data.message !== null && data.message !== '')
                ? data.message
                : 'Đã thêm sản phẩm vào giỏ hàng!';
            showNotification(msg, 'success');
            updateCartCount(data.cart_count);
            return;
        }

        const errMsg = (data.message !== undefined && data.message !== null && data.message !== '')
            ? data.message
            : 'Có lỗi xảy ra!';
        showNotification(errMsg, 'danger');
    } catch (error) {
        console.error('[Cart] Error:', error);
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
// Toast Notification — Modern E-Commerce Style
// =====================================================

function showNotification(message, type = 'success') {
    // ─── DEBUG: Log all inputs ───
    console.log('[Toast DEBUG] Called with:', JSON.stringify({ message, type }));
    console.log('[Toast DEBUG] message type:', typeof message, '| value:', message);
    console.log('[Toast DEBUG] #toast-container exists:', !!document.getElementById('toast-container'));

    // ─── Null/undefined guard ───
    if (message === null || message === undefined || message === '') {
        console.warn('[Toast] Empty message received, using default fallback.');
        message = type === 'success'
            ? 'Thao tác thành công!'
            : type === 'danger'
            ? 'Đã xảy ra lỗi!'
            : 'Thông báo!';
        console.log('[Toast DEBUG] After null-guard, message is:', message);
    }

    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('[Toast FATAL] #toast-container not found in DOM!');
        return;
    }

    // ─── Icon config ───
    const icons = {
        success: { cls: 'fa-check-circle', color: '#22c55e' },
        danger:  { cls: 'fa-exclamation-circle', color: '#ef4444' },
        warning: { cls: 'fa-exclamation-triangle', color: '#f59e0b' },
        info:    { cls: 'fa-info-circle', color: '#3b82f6' },
    };
    const icon = icons[type] || icons.success;

    // ─── Build toast DOM ───
    const toast = document.createElement('div');
    toast.className = 'ts-toast ts-toast--' + type;
    toast.setAttribute('role', 'alert');

    // ─── Safe close handler (no inline onclick for escaping) ───
    const closeBtn = document.createElement('button');
    closeBtn.className = 'ts-toast__close';
    closeBtn.setAttribute('aria-label', 'Đóng');
    closeBtn.innerHTML = '<i class="fas fa-times"></i>';
    closeBtn.addEventListener('click', () => dismissToast(toast));

    const contentDiv = document.createElement('div');
    contentDiv.className = 'ts-toast__content';

    const iconSpan = document.createElement('span');
    iconSpan.className = 'ts-toast__icon';
    iconSpan.style.color = icon.color;
    iconSpan.innerHTML = '<i class="fas ' + icon.cls + '"></i>';

    const messageSpan = document.createElement('span');
    messageSpan.className = 'ts-toast__message';
    messageSpan.textContent = message; // textContent = automatic XSS safe, no escape needed
    console.log('[Toast DEBUG] messageSpan.textContent set to:', messageSpan.textContent);

    contentDiv.appendChild(iconSpan);
    contentDiv.appendChild(messageSpan);

    toast.appendChild(contentDiv);
    toast.appendChild(closeBtn);
    container.appendChild(toast);

    console.log('[Toast DEBUG] Toast element innerHTML:', toast.innerHTML);

    // Force reflow so animation triggers
    void toast.offsetHeight;

    // Enter animation
    requestAnimationFrame(() => {
        toast.classList.add('ts-toast--in');
    });

    // Auto dismiss
    const duration = type === 'danger' ? 5000 : 3000;
    setTimeout(() => dismissToast(toast), duration);

    console.debug('[Toast] Shown successfully:', { message, type });
}

function dismissToast(toast) {
    if (!toast || !toast.parentNode) return;
    toast.classList.remove('ts-toast--in');
    toast.classList.add('ts-toast--out');
    setTimeout(() => {
        if (toast.parentNode) toast.remove();
    }, 450);
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// =====================================================
// Notification (legacy wrapper)
// =====================================================

function showNotification_deprecated(message, type) {
    showNotification(message, type);
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
