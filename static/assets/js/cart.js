// Update totals when the page loads
document.addEventListener("DOMContentLoaded", function() {
    updateTotals();
  });

  // Remove item functionality
  document.querySelectorAll('.remove-btn').forEach(button => {
    button.addEventListener('click', function () {
      this.closest('.cart-item').remove();
      updateTotals();
    });
  });

  // Calculate and update subtotal & total
  function updateTotals() {
    let subtotal = 0;

    document.querySelectorAll('.cart-item').forEach(item => {
      const priceText = item.querySelector('.item-price').textContent;
      const price = parseFloat(priceText.replace('$', ''));
      subtotal += price; // Since quantity is always 1 (disabled input)
    });

    document.getElementById('subtotal').textContent = `$${subtotal.toFixed(2)}`;
    document.getElementById('total').textContent = `$${subtotal.toFixed(2)}`; // No shipping
  }