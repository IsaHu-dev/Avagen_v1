/* jshint esversion: 6 */
/* global $ */

// Run when DOM is ready
window.addEventListener('DOMContentLoaded', function () {
    const sortControl = document.querySelector('#sort-options');

    if (sortControl) {
        sortControl.addEventListener('change', function () {
            const selection = sortControl.value;
            const currentURL = new URL(window.location);

            if (!selection) {
                currentURL.searchParams.delete('sort');
            } else {
                currentURL.searchParams.set('sort', selection);
            }

            window.location.href = currentURL.toString();
        });
    }
});
