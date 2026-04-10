/**
 * Metal Price Ticker - Auto Update System
 * Fetches latest gold and silver prices via AJAX
 * Updates the ticker without page reload
 */

(function() {
    'use strict';

    // Configuration
    const UPDATE_INTERVAL = 300000; // 5 minutes in milliseconds
    const API_URL = '/api/metal-prices/';
    const REFRESH_URL = '/api/refresh-prices/';

    // DOM Elements
    let goldPriceEl, gold22kPriceEl, silverPriceEl;
    let goldChangeEl, silverChangeEl;
    let goldChangeValueEl, silverChangeValueEl;
    let lastUpdatedEl;

    /**
     * Initialize the ticker system
     */
    function initTicker() {
        // Get DOM elements
        goldPriceEl = document.getElementById('gold-price');
        gold22kPriceEl = document.getElementById('gold-22k-price');
        silverPriceEl = document.getElementById('silver-price');
        goldChangeEl = document.getElementById('gold-change');
        silverChangeEl = document.getElementById('silver-change');
        goldChangeValueEl = document.getElementById('gold-change-value');
        silverChangeValueEl = document.getElementById('silver-change-value');
        lastUpdatedEl = document.getElementById('last-updated');

        // Check if elements exist
        if (!goldPriceEl || !silverPriceEl) {
            console.warn('Price ticker elements not found');
            return;
        }

        // Initial fetch
        fetchMetalPrices();

        // Set up auto-refresh interval
        setInterval(fetchMetalPrices, UPDATE_INTERVAL);

        console.log('Metal price ticker initialized');
    }

    /**
     * Fetch latest metal prices from API
     */
    function fetchMetalPrices() {
        // Add loading state
        document.querySelector('.ticker-content')?.classList.add('ticker-loading');

        fetch(API_URL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    updateTicker(data);
                    removeLoadingState();
                } else {
                    console.error('Failed to fetch metal prices:', data.message);
                    showErrorState();
                }
            })
            .catch(error => {
                console.error('Error fetching metal prices:', error);
                showErrorState();
            });
    }

    /**
     * Update ticker with new price data
     */
    function updateTicker(data) {
        try {
            // Update Gold Price (24K)
            if (data.gold) {
                updatePrice(goldPriceEl, data.gold.price);
                updateChangeIndicator(goldChangeEl, goldChangeValueEl, data.gold.change_percent, data.gold.is_up);
                
                // Update 22K price if available
                if (gold22kPriceEl && data.gold.price_22k) {
                    updatePrice(gold22kPriceEl, data.gold.price_22k);
                }
            }

            // Update Silver Price
            if (data.silver) {
                updatePrice(silverPriceEl, data.silver.price);
                updateChangeIndicator(silverChangeEl, silverChangeValueEl, data.silver.change_percent, data.silver.is_up);
            }

            // Update last updated time
            if (data.gold && data.gold.last_updated) {
                if (lastUpdatedEl) {
                    lastUpdatedEl.textContent = data.gold.last_updated;
                }
            }

            // Update duplicate elements (for seamless loop)
            const goldPrice2El = document.getElementById('gold-price-2');
            const silverPrice2El = document.getElementById('silver-price-2');
            
            if (goldPrice2El && data.gold) {
                updatePrice(goldPrice2El, data.gold.price);
            }
            if (silverPrice2El && data.silver) {
                updatePrice(silverPrice2El, data.silver.price);
            }

        } catch (error) {
            console.error('Error updating ticker:', error);
        }
    }

    /**
     * Update price display
     */
    function updatePrice(element, newPrice) {
        if (!element) return;
        
        const oldPrice = parseFloat(element.textContent);
        const price = parseFloat(newPrice);

        // Animate price change
        element.style.transition = 'color 0.3s ease';
        
        if (!isNaN(oldPrice) && oldPrice !== price) {
            if (price > oldPrice) {
                element.style.color = '#00FF00'; // Green flash
            } else if (price < oldPrice) {
                element.style.color = '#FF4444'; // Red flash
            }

            // Reset color after animation
            setTimeout(() => {
                element.style.color = '#fff';
            }, 1000);
        }

        element.textContent = price.toFixed(2);
    }

    /**
     * Update change indicator (arrow and percentage)
     */
    function updateChangeIndicator(changeEl, valueEl, changePercent, isUp) {
        if (!changeEl || !valueEl) return;

        // Update arrow icon
        const icon = changeEl.querySelector('i');
        if (icon) {
            icon.className = isUp ? 'fas fa-arrow-up' : 'fas fa-arrow-down';
        }

        // Update color class
        changeEl.classList.remove('text-success', 'text-danger');
        changeEl.classList.add(isUp ? 'text-success' : 'text-danger');

        // Update percentage value
        valueEl.textContent = `${Math.abs(parseFloat(changePercent)).toFixed(2)}%`;
    }

    /**
     * Remove loading state
     */
    function removeLoadingState() {
        document.querySelector('.ticker-content')?.classList.remove('ticker-loading');
    }

    /**
     * Show error state
     */
    function showErrorState() {
        removeLoadingState();
        document.querySelector('.price-ticker')?.classList.add('ticker-error');
        
        // Remove error state after 3 seconds
        setTimeout(() => {
            document.querySelector('.price-ticker')?.classList.remove('ticker-error');
        }, 3000);
    }

    /**
     * Manual refresh function (can be called from button click)
     */
    window.refreshPrices = function() {
        fetch(REFRESH_URL, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                fetchMetalPrices();
                console.log('Prices refreshed successfully');
            } else {
                console.error('Failed to refresh prices:', data.message);
            }
        })
        .catch(error => {
            console.error('Error refreshing prices:', error);
        });
    };

    /**
     * Get CSRF token from cookies
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTicker);
    } else {
        initTicker();
    }

})();
