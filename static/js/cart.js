// Handle back to top button
$('.btt-link').click(function(e) {
    window.scrollTo(0,0)
});

// Handle quantity increment/decrement
document.addEventListener("DOMContentLoaded", () => {
    // Handle increment/decrement buttons
    document.querySelectorAll(".increment-qty, .decrement-qty").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const input = document.getElementById(`id_qty_${itemId}`);
            let currentValue = parseInt(input.value);
            if (this.classList.contains("increment-qty")) {
                if (currentValue < parseInt(input.max)) input.value = currentValue + 1;
            } else {
                if (currentValue > parseInt(input.min)) input.value = currentValue - 1;
            }
            const form = document.getElementById(`update-form-${itemId}`);
            if (form) form.submit();
        });
    });

    // Handle update links
    document.querySelectorAll(".update-link").forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const form = document.getElementById(`update-form-${itemId}`);
            if (form) form.submit();
        });
    });

    // Handle remove item links
    document.querySelectorAll(".remove-item").forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const form = document.getElementById(`remove-form-${itemId}`);
            if (form && confirm("Are you sure you want to remove this item?")) {
                form.submit();
            }
        });
    });
}); 