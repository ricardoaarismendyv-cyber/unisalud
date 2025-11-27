

// Espera a que el DOM esté completamente cargado
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
    const accessibilityIcon = document.getElementById('accessibility-icon');
    const accessibilitySidebar = document.getElementById('accessibility-sidebar');
    const closeSidebarBtn = document.getElementById('close-sidebar-btn');

    if (accessibilityIcon && closeSidebarBtn && accessibilitySidebar) {
        accessibilityIcon.addEventListener('click', () => accessibilitySidebar.style.width = '300px');
        closeSidebarBtn.addEventListener('click', () => accessibilitySidebar.style.width = '0');
    }

});
