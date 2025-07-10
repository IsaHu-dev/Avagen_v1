// Initialize Bootstrap components
$(function () {
  // Initialize popovers
  $('[data-toggle="popover"]').popover();
  
  // Initialize tooltips
  $('[data-toggle="tooltip"]').tooltip();
  
  // Auto-hide popups after 5 seconds
  setTimeout(function() {
    $('.popup').fadeOut();
  }, 5000);
}); 