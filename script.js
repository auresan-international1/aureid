document.getElementById('order-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const name = document.getElementById('fullname').value;
    const phone = document.getElementById('phone').value;

    try {
        const response = await fetch('http://127.0.0.1:5000/submit-form', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone })
        });
        const result = await response.json();
        if (response.ok) {
            alert('Thank you! Your order has been received.');
            this.reset();
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    }
});