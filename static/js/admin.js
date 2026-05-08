// TechShop Admin - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Toggle (Mobile)
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const btnToggleSidebar = document.getElementById('btnToggleSidebar');

    function toggleSidebar() {
        if (sidebar) {
            sidebar.classList.toggle('active');
        }
        if (sidebarOverlay) {
            sidebarOverlay.classList.toggle('active');
        }
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }

    if (btnToggleSidebar) {
        btnToggleSidebar.addEventListener('click', toggleSidebar);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', toggleSidebar);
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // CSRF Token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

    // AJAX helper
    window.ajaxRequest = function(url, options = {}) {
        const defaultOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        return fetch(url, { ...defaultOptions, ...options })
            .then(response => response.json());
    };

    // Toast notification
    window.showToast = function(message, type = 'success') {
        const container = document.getElementById('toastContainer');
        if (!container) return;
        
        const id = 'toast-' + Date.now();
        const iconClass = type === 'success' ? 'check-circle text-success' : 
                         type === 'danger' ? 'x-circle text-danger' : 
                         type === 'warning' ? 'exclamation-triangle text-warning' : 
                         'info-circle text-info';
        
        const html = '<div id="' + id + '" class="toast show" role="alert"><div class="toast-body"><i class="bi bi-' + iconClass + ' me-2"></i>' + message + '</div></div>';
        container.insertAdjacentHTML('beforeend', html);
        
        setTimeout(function() {
            var toast = document.getElementById(id);
            if (toast) {
                toast.classList.remove('show');
                setTimeout(function() { toast.remove(); }, 300);
            }
        }, 4000);
    };
});

// Format currency VND with dot separator
function formatCurrency(amount) {
    return amount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.') + 'đ';
}

// Auto-format currency on page load
function autoFormatCurrency() {
    document.querySelectorAll('[data-currency]').forEach(function(el) {
        var value = parseFloat(el.dataset.currency);
        if (!isNaN(value)) {
            el.textContent = formatCurrency(value);
        }
    });
}

// Debounce helper
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
