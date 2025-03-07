// Initialize Feather icons
document.addEventListener('DOMContentLoaded', function() {
    feather.replace();
});

// Add input focus effect
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.boxShadow = '0 1px 6px rgba(32,33,36,.28)';
        });

        searchInput.addEventListener('blur', function() {
            this.parentElement.style.boxShadow = 'none';
        });
    }
});
