
/* jshint esversion: 6 */
/* global $ */

$('#sort-selector').change(function () {
    const selector = $(this);
    const currentUrl = new URL(window.location);
    const selectedVal = selector.val();

    if (selectedVal !== "reset") {
        const sort = selectedVal.split("_")[0];
        const direction = selectedVal.split("_")[1];
        currentUrl.searchParams.set("sort", sort);
        currentUrl.searchParams.set("direction", direction);
    } else {
        currentUrl.searchParams.delete("sort");
        currentUrl.searchParams.delete("direction");
    }

    window.location.replace(currentUrl);
});
