/* jshint esversion: 6 */
/* global $ */

$('.btt-link').click(function(e) { window.scrollTo(0, 0); });

function getKeys(el) {
  const cartKey = el.getAttribute('data-cart_key') || el.dataset.cartKey || el.dataset.cart_key || el.dataset.cartkey || '';
  const itemId  = el.getAttribute('data-item_id') || el.dataset.itemId || '';
  return { cartKey, itemId };
}
function byId(id){ return document.getElementById(id); }
function findQtyInput(k){ return byId(`id_qty_${k.cartKey}`) || byId(`id_qty_${k.itemId}`); }
function findUpdateForm(k){ return byId(`update-form-${k.cartKey}`) || byId(`update-form-${k.itemId}`); }
function findRemoveForm(k){ return byId(`remove-form-${k.cartKey}`) || byId(`remove-form-${k.itemId}`); }

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.increment-qty, .decrement-qty').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const k = getKeys(btn);
      const input = findQtyInput(k);
      if (!input) return;
      const min = parseInt(input.getAttribute('min') || '1', 10);
      const max = parseInt(input.getAttribute('max') || '99', 10);
      let val = parseInt(input.value || '0', 10);
      if (isNaN(val)) val = min;
      val = btn.classList.contains('increment-qty') ? Math.min(max, val + 1) : Math.max(min, val - 1);
      input.value = val;
      const form = findUpdateForm(k);
      if (form) form.submit();
    });
  });

  document.querySelectorAll('.qty_input').forEach(input => {
    input.addEventListener('change', () => {
      const form = input.closest('form');
      if (form) form.submit();
    });
  });

  document.querySelectorAll('.update-link').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const form = findUpdateForm(getKeys(link));
      if (form) form.submit();
    });
  });

  document.querySelectorAll('.remove-item').forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const form = findRemoveForm(getKeys(link));
      if (form) form.submit();
    });
  });
});
