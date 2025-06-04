/*
    Stripe integration with separated card inputs (no embedded ZIP field)
*/

const stripePublicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

// Create separate elements
const cardNumber = elements.create('cardNumber', { style });
cardNumber.mount('#card-number-element');

const cardExpiry = elements.create('cardExpiry', { style });
cardExpiry.mount('#card-expiry-element');

const cardCvc = elements.create('cardCvc', { style });
cardCvc.mount('#card-cvc-element');

// Display Stripe validation errors
function showError(errorMessage) {
    const errorDiv = document.getElementById('card-errors');
    errorDiv.innerHTML = `
        <span class="icon" role="alert">
            <i class="fas fa-times"></i>
        </span>
        <span>${errorMessage}</span>
    `;
}

// Handle real-time validation
[cardNumber, cardExpiry, cardCvc].forEach(el => {
    el.on('change', event => {
        if (event.error) {
            showError(event.error.message);
        } else {
            document.getElementById('card-errors').textContent = '';
        }
    });
});

const form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();

    const postcodeInput = document.getElementById('manual-postcode');
    const postcode = $.trim(postcodeInput.value);
    const postcodeRegex = /^[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}$/i;

    if (!postcodeRegex.test(postcode)) {
        showError('Enter a valid UK postcode (e.g. W1A 1AA).');
        return;
    }

    cardNumber.update({ disabled: true });
    cardExpiry.update({ disabled: true });
    cardCvc.update({ disabled: true });
    document.getElementById('submit-button').disabled = true;

    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);

    const saveInfo = $('#id-save-info').prop('checked');
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    const postData = {
        csrfmiddlewaretoken: csrfToken,
        client_secret: clientSecret,
        save_info: saveInfo,
    };

    const url = '/checkout/cache_checkout_data/';

    $.post(url, postData).done(function () {
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
                showError(result.error.message);
                $('#payment-form').fadeToggle(100);
                $('#loading-overlay').fadeToggle(100);
                cardNumber.update({ disabled: false });
                cardExpiry.update({ disabled: false });
                cardCvc.update({ disabled: false });
                document.getElementById('submit-button').disabled = false;
            } else {
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        location.reload();
    });
});
