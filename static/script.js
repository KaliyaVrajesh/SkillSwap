// Add this to your dark mode toggle script, after the theme change
document.querySelectorAll('.card, .alert, .form-control, .dropdown-menu').forEach(el => {
    el.style.transition = 'all 0.3s ease';
});
