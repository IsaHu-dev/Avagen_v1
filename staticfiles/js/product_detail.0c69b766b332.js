// Product Detail Page JavaScript
// Handles license price updates and delete confirmation
/* jshint esversion: 6 */
/* global $ */


document.addEventListener('DOMContentLoaded', function() {
    // License price update functionality
    const licenseSelect = document.getElementById('license');
    const priceDisplay = document.getElementById('price-display');
    
    if (licenseSelect && priceDisplay) {
        // Get prices from data attributes (will be set by template)
        const priceMap = {
            'personal': parseFloat(licenseSelect.getAttribute('data-personal-price') || '0'),
            'indie': parseFloat(licenseSelect.getAttribute('data-indie-price') || '0'),
            'professional': parseFloat(licenseSelect.getAttribute('data-professional-price') || '0'),
        };

        licenseSelect.addEventListener('change', function() {
            const selected = this.value;
            const newPrice = priceMap[selected].toFixed(2);
            priceDisplay.innerText = "£" + newPrice;
        });
    }

    // Delete product confirmation
    const deleteLinks = document.querySelectorAll('.delete-product-link');
    
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productName = this.getAttribute('data-product-name');
            const confirmMessage = `Are you sure you want to delete "${productName}"?\n\nThis action cannot be undone and will permanently remove the product from the store.`;
            
            if (confirm(confirmMessage)) {
                window.location.href = this.href;
            }
        });
    });
}); 