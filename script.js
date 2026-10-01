document.getElementById('order-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const name = document.getElementById('fullname').value;
    const phone = document.getElementById('phone').value;

    const url = '/submit-form';

    const payload = { name, phone, productname: 'DiaFormula' };

    try {

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Log response headers
        for (const [key, value] of response.headers.entries()) {
            console.log(`${key}: ${value}`);
        }

        const responseText = await response.text();

        let result;

        try {
            result = JSON.parse(responseText);
        } catch (jsonError) {
         
            alert('Server returned an invalid response. Check the browser console.');
            return;
        }

        if (response.ok) {            

            alert('Thank you! Your order has been received.');

            this.reset();

        } else {            
            alert('Error: ' + (result.error || 'Unknown server error'));
        }

    } catch (error) {       

        alert('Something went wrong. Please try again.');
    }
});