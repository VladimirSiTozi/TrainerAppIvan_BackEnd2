document.querySelector('.checkout-form').addEventListener('submit', function (e) {
  e.preventDefault();
  const email = document.getElementById('email').value;
  if (!email.includes('@')) {
    alert('Please enter a valid email address.');
    return;
  }
  alert('Details submitted. Proceeding to payment...');
  // Redirect or process here
});
