/**
 * AASHUTOSH JEWELLERS - CAMPAIGN MANAGER ADMIN JS
 * Dynamic Field Toggling & 2-Column Hero Media Layout
 */

document.addEventListener('DOMContentLoaded', function () {

    // --- 1. Dynamic Photo vs Video Field Toggling ---
    function setupMediaToggle(typeSelectSelector, imageRowSelector, videoRowSelector) {
        const typeSelect = document.querySelector(typeSelectSelector);
        const imageRow = document.querySelector(imageRowSelector);
        const videoRow = document.querySelector(videoRowSelector);

        if (!typeSelect) return;

        function updateVisibility() {
            const val = typeSelect.value;
            if (val === 'IMAGE') {
                if (imageRow) imageRow.style.display = '';
                if (videoRow) videoRow.style.display = 'none';
            } else if (val === 'VIDEO') {
                if (imageRow) imageRow.style.display = 'none';
                if (videoRow) videoRow.style.display = '';
            } else if (val === 'NONE') {
                if (imageRow) imageRow.style.display = 'none';
                if (videoRow) videoRow.style.display = 'none';
            }
        }

        updateVisibility();
        typeSelect.addEventListener('change', updateVisibility);
    }

    // Hero Desktop Toggle
    setupMediaToggle(
        'select[name="hero_desktop_media_type"]',
        '.field-hero_desktop_image',
        '.field-hero_desktop_video'
    );

    // Hero Mobile Toggle
    setupMediaToggle(
        'select[name="hero_mobile_media_type"]',
        '.field-hero_mobile_image',
        '.field-hero_mobile_video'
    );

    // Popup Modal Toggle
    setupMediaToggle(
        'select[name="popup_media_type"]',
        '.field-popup_image',
        '.field-popup_video'
    );

    // Floating Widget Toggle
    setupMediaToggle(
        'select[name="floating_media_type"]',
        '.field-floating_image',
        '.field-floating_video'
    );

    // Inline Card Toggle
    setupMediaToggle(
        'select[name="inline_media_type"]',
        '.field-inline_image',
        '.field-inline_video'
    );


    // --- 2. Rearrange Hero Section into a 2-Column Grid ---
    const heroFieldset = Array.from(document.querySelectorAll('fieldset')).find(fs => {
        const h2 = fs.querySelector('h2');
        return h2 && h2.innerText.includes('Hero Section Override');
    });

    if (heroFieldset) {
        const desktopTypeRow = heroFieldset.querySelector('.field-hero_desktop_media_type');
        const desktopImgRow = heroFieldset.querySelector('.field-hero_desktop_image');
        const desktopVidRow = heroFieldset.querySelector('.field-hero_desktop_video');
        const desktopPrevRow = heroFieldset.querySelector('.field-desktop_hero_preview');

        const mobileTypeRow = heroFieldset.querySelector('.field-hero_mobile_media_type');
        const mobileImgRow = heroFieldset.querySelector('.field-hero_mobile_image');
        const mobileVidRow = heroFieldset.querySelector('.field-hero_mobile_video');
        const mobilePrevRow = heroFieldset.querySelector('.field-mobile_hero_preview');

        if (desktopTypeRow && mobileTypeRow) {
            const gridContainer = document.createElement('div');
            gridContainer.className = 'hero-media-grid';

            const desktopCard = document.createElement('div');
            desktopCard.className = 'hero-col-card desktop-col';
            desktopCard.innerHTML = '<div class="hero-col-title">💻 DESKTOP HERO MEDIA <span>Recommended 1920x960 px (~2:1)</span></div>';

            const mobileCard = document.createElement('div');
            mobileCard.className = 'hero-col-card mobile-col';
            mobileCard.innerHTML = '<div class="hero-col-title">📱 MOBILE HERO MEDIA <span>Recommended 1080x1350 px (~4:5)</span></div>';

            // Append Desktop Rows
            if (desktopTypeRow) desktopCard.appendChild(desktopTypeRow);
            if (desktopImgRow) desktopCard.appendChild(desktopImgRow);
            if (desktopVidRow) desktopCard.appendChild(desktopVidRow);
            if (desktopPrevRow) desktopCard.appendChild(desktopPrevRow);

            // Append Mobile Rows
            if (mobileTypeRow) mobileCard.appendChild(mobileTypeRow);
            if (mobileImgRow) mobileCard.appendChild(mobileImgRow);
            if (mobileVidRow) mobileCard.appendChild(mobileVidRow);
            if (mobilePrevRow) mobileCard.appendChild(mobilePrevRow);

            gridContainer.appendChild(desktopCard);
            gridContainer.appendChild(mobileCard);

            heroFieldset.appendChild(gridContainer);
        }
    }


    // --- 3. Collapsible Fieldset Cards ---
    const fieldsets = document.querySelectorAll('#content-main fieldset');
    fieldsets.forEach(function (fs, idx) {
        const h2 = fs.querySelector('h2');
        if (!h2) return;

        // Add toggle arrow indicator if missing
        if (!h2.querySelector('.fieldset-arrow')) {
            const arrow = document.createElement('span');
            arrow.className = 'fieldset-arrow';
            arrow.innerHTML = ' ▼';
            arrow.style.float = 'right';
            arrow.style.fontSize = '0.8rem';
            arrow.style.color = '#94a3b8';
            h2.appendChild(arrow);
        }

        // Keep Campaign Info, Hero, and Schedule open by default; collapse secondary fieldsets if desired
        if (idx >= 4) {
            fs.classList.add('collapsed');
            const fields = fs.querySelectorAll('.form-row, .hero-media-grid, .description');
            fields.forEach(f => f.style.display = 'none');
            const arrow = h2.querySelector('.fieldset-arrow');
            if (arrow) arrow.innerHTML = ' ▶';
        }

        h2.addEventListener('click', function () {
            const isCollapsed = fs.classList.contains('collapsed');
            const fields = fs.querySelectorAll('.form-row, .hero-media-grid, .description');
            const arrow = h2.querySelector('.fieldset-arrow');

            if (isCollapsed) {
                fs.classList.remove('collapsed');
                fields.forEach(f => f.style.display = '');
                if (arrow) arrow.innerHTML = ' ▼';
            } else {
                fs.classList.add('collapsed');
                fields.forEach(f => f.style.display = 'none');
                if (arrow) arrow.innerHTML = ' ▶';
            }
        });
    });

});
