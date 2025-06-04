window.addEventListener('DOMContentLoaded', () => {
        const sortControl = document.querySelector('#sort-options');
        sortControl?.addEventListener('change', () => {
            const selection = sortControl.value;
            const currentURL = new URL(window.location);

            if (!selection) {
                currentURL.searchParams.delete('sort');
            } else {
                currentURL.searchParams.set('sort', selection);
            }

            window.location.href = currentURL.toString();
        });
    });

