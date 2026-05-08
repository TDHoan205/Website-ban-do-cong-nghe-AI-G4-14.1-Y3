/**
 * TechShop Admin SPA - Single Page Application Navigation
 * Xử lý AJAX load nội dung khi click sidebar links
 */
(function() {
    'use strict';

    // SPA Navigation Handler
    function initSPANavigation() {
        // Chỉ áp dụng cho sidebar menu
        const sidebarLinks = document.querySelectorAll('.sidebar-menu .nav-link');

        sidebarLinks.forEach(function(link) {
            // Bỏ qua links có target="_blank" hoặc href="#"
            if (link.getAttribute('target') === '_blank' || link.getAttribute('href') === '#') {
                return;
            }

            link.addEventListener('click', function(e) {
                const href = this.getAttribute('href');

                // Bỏ qua nếu không có href hoặc là anchor/hash
                if (!href || href.startsWith('#') || href.startsWith('javascript:')) {
                    return;
                }

                // Bỏ qua nếu là link ngoài (có protocol như http://)
                if (href.match(/^https?:\/\//)) {
                    return;
                }

                e.preventDefault();

                // Highlight active link
                sidebarLinks.forEach(function(l) {
                    l.classList.remove('active');
                });
                this.classList.add('active');

                // Show loading state
                const pageContent = document.querySelector('.page-content');
                if (pageContent) {
                    pageContent.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-3 text-muted">Đang tải...</p></div>';
                }

                // Fetch new content
                fetch(href, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(function(response) {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(function(html) {
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html');

                    // Extract page content
                    const newContent = doc.querySelector('.page-content')?.innerHTML ||
                                       doc.querySelector('main')?.innerHTML ||
                                       doc.querySelector('#content')?.innerHTML;

                    if (newContent && pageContent) {
                        pageContent.innerHTML = newContent;

                        // Update page title
                        const newTitle = doc.querySelector('title')?.textContent;
                        if (newTitle) {
                            document.title = newTitle;
                        }

                        // Update URL without reload
                        window.history.pushState({}, '', href);

                        // Re-initialize Bootstrap components
                        initBootstrapComponents();

                        // Re-apply currency formatting
                        if (typeof autoFormatCurrency === 'function') {
                            autoFormatCurrency();
                        }

                        // Scroll to top
                        window.scrollTo({ top: 0, behavior: 'smooth' });

                        // Trigger custom event for other scripts
                        document.dispatchEvent(new CustomEvent('spa:contentLoaded', {
                            detail: { url: href }
                        }));
                    } else {
                        // Fallback: full page reload
                        window.location.href = href;
                    }
                })
                .catch(function(error) {
                    console.error('SPA Navigation Error:', error);
                    // Fallback: full page reload on error
                    window.location.href = href;
                });
            });
        });

        // Handle browser back/forward buttons
        window.addEventListener('popstate', function(e) {
            const currentPath = window.location.pathname;
            if (currentPath) {
                loadPage(currentPath, true);
            }
        });
    }

    // Load page content (used for popstate)
    function loadPage(url, skipHistory) {
        const pageContent = document.querySelector('.page-content');
        if (pageContent) {
            pageContent.innerHTML = '<div class="text-center py-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-3 text-muted">Đang tải...</p></div>';

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(function(response) { return response.text(); })
            .then(function(html) {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContent = doc.querySelector('.page-content')?.innerHTML ||
                                   doc.querySelector('main')?.innerHTML;

                if (newContent && pageContent) {
                    pageContent.innerHTML = newContent;
                    if (!skipHistory) {
                        window.history.pushState({}, '', url);
                    }
                    initBootstrapComponents();
                    if (typeof autoFormatCurrency === 'function') {
                        autoFormatCurrency();
                    }
                }
            })
            .catch(function() {
                window.location.href = url;
            });
        }
    }

    // Re-initialize Bootstrap components after AJAX load
    function initBootstrapComponents() {
        // Re-init tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        tooltipTriggerList.forEach(function(tooltipTriggerEl) {
            new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Re-init popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        popoverTriggerList.forEach(function(popoverTriggerEl) {
            new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSPANavigation);
    } else {
        initSPANavigation();
    }
})();
