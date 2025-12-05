

document.addEventListener('DOMContentLoaded', function () {
// --- Lógica para el modo oscuro ---
    const themeToggleButton = document.getElementById('theme-toggle-img');
    const moonIcon = document.getElementById('moon-icon');
    const body = document.getElementById('page-body');

// Las rutas a las imágenes se pasan desde el HTML a través de atributos data-*
    const toggleOffImg = themeToggleButton ? themeToggleButton.dataset.toggleOff : '';
    const toggleOnImg = themeToggleButton ? themeToggleButton.dataset.toggleOn : '';

    // Aplicar el tema guardado al cargar la página
    const savedTheme = localStorage.getItem('dark-mode');
    if (savedTheme === "enabled") {
        if (body) body.classList.add('dark-mode');
        if (themeToggleButton && toggleOnImg) themeToggleButton.src = toggleOnImg;
    } else {
        if (themeToggleButton && toggleOffImg) themeToggleButton.src = toggleOffImg;
    }

    function toggleTheme() {
        if (!body || !themeToggleButton) return;

        // Alternar la clase
        const isDarkNow = body.classList.toggle('dark-mode');

        // Cambiar src del toggle (si existen las rutas)
        if (isDarkNow) {
            if (toggleOnImg) themeToggleButton.src = toggleOnImg;
            localStorage.setItem('dark-mode', 'enabled');
        } else {
            if (toggleOffImg) themeToggleButton.src = toggleOffImg;
            localStorage.setItem('dark-mode', 'disabled');
        }
    }

    if (themeToggleButton && moonIcon) {
        themeToggleButton.addEventListener('click', toggleTheme);
        moonIcon.addEventListener('click', toggleTheme);
    }

    // --- Lógica para el menú de idiomas ---
    const langButton = document.getElementById('language-button');
    const langMenu = document.getElementById('language-menu');
    if (langButton && langMenu) {
        langButton.addEventListener('click', function(event) {
            event.stopPropagation(); 
            langMenu.style.display = langMenu.style.display === 'block' ? 'none' : 'block';
        });

        document.addEventListener('click', function() {
            if (langMenu.style.display === 'block') {
                langMenu.style.display = 'none';
            }
        });
    }

  // --- Lógica para la Barra Lateral de Accesibilidad ---
    const sidebar = document.getElementById('accessibility-sidebar');
    const openBtn = document.getElementById('accessibility-icon');
    const closeBtn = document.getElementById('close-sidebar-btn');

    // Botones internos
    const increaseBtn = document.getElementById('increase-font');
    const decreaseBtn = document.getElementById('decrease-font');
    const dyslexiaBtn = document.getElementById('dyslexia-font');
    const contrastBtn = document.getElementById('high-contrast');
    const daltonBtn = document.getElementById('daltonia-font');
    const resetBtn = document.getElementById('reset-accessibility');

    // Tamaño de fuente
    let currentFontSize = parseInt(localStorage.getItem('access_fontSize')) || 16;
    body.style.fontSize = currentFontSize + 'px';

    // Abrir/Cerrar sidebar
    if (openBtn && sidebar) {
        openBtn.addEventListener('click', () => {
            sidebar.style.width = '340px';
        });
    }
    if (closeBtn && sidebar) {
        closeBtn.addEventListener('click', () => {
            sidebar.style.width = '0';
        });
    }

    // Aumentar el tamaño de la letra
    if (increaseBtn) {
        increaseBtn.addEventListener('click', () => {
            currentFontSize = Math.min(currentFontSize + 2, 28);
            body.style.fontSize = currentFontSize + 'px';
            localStorage.setItem('access_fontSize', currentFontSize);
        });
    }

    // Disminuir el tamaño de la letra
    if (decreaseBtn) {
        decreaseBtn.addEventListener('click', () => {
            currentFontSize = Math.max(currentFontSize - 2, 10);
            body.style.fontSize = currentFontSize + 'px';
            localStorage.setItem('access_fontSize', currentFontSize);
        });
    }

    // Fuente para la Dislexia
    if (dyslexiaBtn) {
        dyslexiaBtn.addEventListener('click', () => {
            const active = body.classList.toggle('dyslexia-font');
            dyslexiaBtn.classList.toggle('active', active);
            localStorage.setItem('access_dyslexia', active ? '1' : '0');
        });
    }

    // Contraste alto
    if (contrastBtn) {
        contrastBtn.addEventListener('click', () => {
            const active = body.classList.toggle('high-contrast');
            contrastBtn.classList.toggle('active', active);
            localStorage.setItem('access_contrast', active ? '1' : '0');
        });
    }

    // Daltonismo
    if (daltonBtn) {
        daltonBtn.addEventListener('click', () => {
            const active = body.classList.toggle('color-blind-mode');
            daltonBtn.classList.toggle('active', active);
            localStorage.setItem('access_daltonismo', active ? '1' : '0');
        });
    }

    // Restablecer
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            currentFontSize = 16;
            body.style.fontSize = '16px';
            body.classList.remove('dyslexia-font', 'high-contrast', 'color-blind-mode');
            [dyslexiaBtn, contrastBtn, daltonBtn].forEach(btn => btn?.classList.remove('active'));
            localStorage.removeItem('access_fontSize');
            localStorage.removeItem('access_dyslexia');
            localStorage.removeItem('access_contrast');
            localStorage.removeItem('access_daltonismo');
        });
    }

    // Aplicar preferencias guardadas
    if (localStorage.getItem('access_fontSize')) {
        body.style.fontSize = localStorage.getItem('access_fontSize') + 'px';
    }
    if (localStorage.getItem('access_dyslexia') === '1') {
        body.classList.add('dyslexia-font');
        dyslexiaBtn?.classList.add('active');
    }
    if (localStorage.getItem('access_contrast') === '1') {
        body.classList.add('high-contrast');
        contrastBtn?.classList.add('active');
    }
    if (localStorage.getItem('access_daltonismo') === '1') {
        body.classList.add('color-blind-mode');
        daltonBtn?.classList.add('active');
    }
});