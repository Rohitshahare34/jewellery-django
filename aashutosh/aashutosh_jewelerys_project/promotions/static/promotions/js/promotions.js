/**
 * AASHUTOSH JEWELLERS - FESTIVAL & PROMOTION CAMPAIGN JS
 */

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. Real-time Countdown Timer ---
    const countdownEl = document.getElementById('promo-countdown-widget');
    if (countdownEl) {
        const endDateStr = countdownEl.getAttribute('data-end-date');
        if (endDateStr) {
            const targetDate = new Date(endDateStr).getTime();

            const daysEl = document.getElementById('promo-days');
            const hoursEl = document.getElementById('promo-hours');
            const minsEl = document.getElementById('promo-mins');
            const secsEl = document.getElementById('promo-secs');

            function updateCountdown() {
                const now = new Date().getTime();
                const distance = targetDate - now;

                if (distance < 0) {
                    if (daysEl) daysEl.innerText = "00";
                    if (hoursEl) hoursEl.innerText = "00";
                    if (minsEl) minsEl.innerText = "00";
                    if (secsEl) secsEl.innerText = "00";
                    return;
                }

                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);

                if (daysEl) daysEl.innerText = days < 10 ? '0' + days : days;
                if (hoursEl) hoursEl.innerText = hours < 10 ? '0' + hours : hours;
                if (minsEl) minsEl.innerText = minutes < 10 ? '0' + minutes : minutes;
                if (secsEl) secsEl.innerText = seconds < 10 ? '0' + seconds : seconds;
            }

            updateCountdown();
            setInterval(updateCountdown, 1000);
        }
    }

    // --- 2. Promotional Popup Modal ---
    const promoModal = document.getElementById('promo-modal-backdrop');
    if (promoModal) {
        const modalId = promoModal.getAttribute('data-campaign-id') || 'default';
        const storageKey = 'promo_dismissed_' + modalId;

        // Check if user already closed this modal in this session
        if (!sessionStorage.getItem(storageKey)) {
            setTimeout(function () {
                promoModal.classList.add('show');
            }, 1200);
        }

        const closeBtn = document.getElementById('promo-modal-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function () {
                promoModal.classList.remove('show');
                sessionStorage.setItem(storageKey, 'true');
            });
        }

        // Close when clicking outside content
        promoModal.addEventListener('click', function (e) {
            if (e.target === promoModal) {
                promoModal.classList.remove('show');
                sessionStorage.setItem(storageKey, 'true');
            }
        });
    }

    // --- 3. Top Announcement Close Button ---
    const annBar = document.getElementById('promo-announcement-bar');
    const annClose = document.getElementById('promo-announcement-close');
    if (annBar && annClose) {
        annClose.addEventListener('click', function () {
            annBar.style.display = 'none';
        });
    }

    // --- 4. Floating Video Reel Player (Movable / Draggable Anywhere) ---
    const reelWidget = document.getElementById('promo-floating-reel');
    if (reelWidget) {
        const minimizeBtn = document.getElementById('promo-reel-minimize');
        const closeBtn = document.getElementById('promo-reel-close');
        const reelVideo = document.getElementById('promo-reel-video-element');
        const dragHeader = reelWidget.querySelector('.promo-reel-header') || reelWidget;

        if (minimizeBtn) {
            minimizeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                reelWidget.classList.toggle('minimized');
                if (reelVideo) {
                    if (reelWidget.classList.contains('minimized')) {
                        reelVideo.pause();
                    } else {
                        reelVideo.play().catch(function(){});
                    }
                }
            });
        }

        if (closeBtn) {
            closeBtn.addEventListener('click', function (e) {
                e.stopPropagation();
                reelWidget.style.display = 'none';
                if (reelVideo) reelVideo.pause();
            });
        }

        // --- Draggable Movable Logic (Mouse & Touch) ---
        let isDragging = false;
        let hasMoved = false;
        let startX = 0, startY = 0;
        let initialLeft = 0, initialTop = 0;

        function onDragStart(e) {
            // Ignore minimize and close control buttons
            if (e.target.closest('.promo-reel-btn')) {
                return;
            }

            isDragging = true;
            hasMoved = false;
            reelWidget.classList.add('is-dragging');

            const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
            const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;

            startX = clientX;
            startY = clientY;

            const rect = reelWidget.getBoundingClientRect();
            initialLeft = rect.left;
            initialTop = rect.top;

            reelWidget.style.bottom = 'auto';
            reelWidget.style.right = 'auto';
            reelWidget.style.left = initialLeft + 'px';
            reelWidget.style.top = initialTop + 'px';

            document.addEventListener('mousemove', onDragMove);
            document.addEventListener('mouseup', onDragEnd);
            document.addEventListener('touchmove', onDragMove, { passive: false });
            document.addEventListener('touchend', onDragEnd);
        }

        function onDragMove(e) {
            if (!isDragging) return;

            const clientX = e.type.startsWith('touch') ? e.touches[0].clientX : e.clientX;
            const clientY = e.type.startsWith('touch') ? e.touches[0].clientY : e.clientY;

            const deltaX = clientX - startX;
            const deltaY = clientY - startY;

            if (Math.abs(deltaX) > 4 || Math.abs(deltaY) > 4) {
                hasMoved = true;
                if (e.cancelable) e.preventDefault();
            }

            if (hasMoved) {
                let newLeft = initialLeft + deltaX;
                let newTop = initialTop + deltaY;

                const maxLeft = window.innerWidth - reelWidget.offsetWidth - 10;
                const maxTop = window.innerHeight - reelWidget.offsetHeight - 10;

                newLeft = Math.max(10, Math.min(newLeft, maxLeft));
                newTop = Math.max(10, Math.min(newTop, maxTop));

                reelWidget.style.left = newLeft + 'px';
                reelWidget.style.top = newTop + 'px';
            }
        }

        function onDragEnd(e) {
            if (!isDragging) return;
            isDragging = false;
            reelWidget.classList.remove('is-dragging');

            document.removeEventListener('mousemove', onDragMove);
            document.removeEventListener('mouseup', onDragEnd);
            document.removeEventListener('touchmove', onDragMove);
            document.removeEventListener('touchend', onDragEnd);
        }

        // Attach drag listeners to both header and full widget container
        reelWidget.addEventListener('mousedown', onDragStart);
        reelWidget.addEventListener('touchstart', onDragStart, { passive: true });

        // Prevent link redirection if the user was dragging the element
        const overlayLink = reelWidget.querySelector('.promo-reel-overlay-link');
        if (overlayLink) {
            overlayLink.addEventListener('click', function (e) {
                if (hasMoved) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        }
    }

    // --- 5. One-Click Promo Code Copy ---
    const codePills = document.querySelectorAll('.promo-code-pill');
    codePills.forEach(function (pill) {
        pill.addEventListener('click', function () {
            const code = pill.getAttribute('data-code') || pill.innerText.trim();
            navigator.clipboard.writeText(code).then(function () {
                const originalText = pill.innerText;
                pill.innerText = "COPIED! ✓";
                setTimeout(function () {
                    pill.innerText = originalText;
                }, 2000);
            }).catch(function(){});
        });
    });

});
