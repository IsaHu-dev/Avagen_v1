/* jshint esversion: 6 */
/* global $, Stripe */

const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

// Initialize Stripe with the public key
const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

// Define style for the card elements
const style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4' // Placeholder text color
        }
    },
    invalid: {
        color: '#dc3545', // Error text color
        iconColor: '#dc3545' // Error icon color
    }
};

// Create and mount the individual card input fields
const cardNumber = elements.create('cardNumber', { style });
cardNumber.mount('#card-number-element');

const cardExpiry = elements.create('cardExpiry', { style });
cardExpiry.mount('#card-expiry-element');

const cardCvc = elements.create('cardCvc', { style });
cardCvc.mount('#card-cvc-element');

// Function to show Stripe validation errors
function showError(errorMessage) {
    const errorDiv = document.getElementById('card-errors');
    errorDiv.innerHTML = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${errorMessage}</span>
    `;
}

// Set up real-time validation error handling for each card field
[cardNumber, cardExpiry, cardCvc].forEach(el => {
    el.on('change', event => {
        if (event.error) {
            showError(event.error.message); // Show validation message
        } else {
            document.getElementById('card-errors').textContent = ''; // Clear previous errors
        }
    });
});

// Get the payment form element
const form = document.getElementById('payment-form');

// Add form submission handler
form.addEventListener('submit', function (ev) {
    ev.preventDefault(); // Stop normal form submission

    // Validate postcode input (optional - not required for all countries)
    const postcodeInput = document.getElementById('manual-postcode');
    const postcode = $.trim(postcodeInput.value);
    
    // Only validate UK postcode format if postcode is provided and looks like UK format
    if (postcode && postcode.length > 0) {
        const postcodeRegex = /^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$/i;
        if (!postcodeRegex.test(postcode)) {
            showError('Enter a valid postcode format.');
            return;
        }
    }

    // Disable input fields and button to prevent duplicate submissions
    cardNumber.update({ disabled: true });
    cardExpiry.update({ disabled: true });
    cardCvc.update({ disabled: true });
    document.getElementById('submit-button').disabled = true;

    // Show loading overlay and hide form
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    // Gather data to be cached in the backend
    const saveInfo = $('#id-save-info').prop('checked');
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    const postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfo,
    };

    const url = '/checkout/cache_checkout_data/';

    // Send cached data to the backend
    $.post(url, postData).done(function () {
        // Confirm the payment with Stripe
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardNumber,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                        postal_code: postcode
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                    postal_code: postcode
                }
            }
        }).then(function (result) {
            if (result.error) {
                // Show Stripe error and re-enable form elements
                showError(result.error.message);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                cardNumber.update({ disabled: false });
                cardExpiry.update({ disabled: false });
                cardCvc.update({ disabled: false });
                document.getElementById('submit-button').disabled = false;
            } else {
                // Payment succeeded, submit form to complete process
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // Reload page on failure to post cached data
        location.reload();
    });
});
