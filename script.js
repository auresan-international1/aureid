document.getElementById('order-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    console.log('====================================');
    console.log('🟢 ORDER FORM SUBMISSION STARTED');
    console.log('====================================');

    const name = document.getElementById('fullname').value;
    const phone = document.getElementById('phone').value;

    console.log('📋 Form data:');
    console.log('Name:', name);
    console.log('Phone:', phone);

    const url = '/submit-form';

    console.log('🌐 Request URL:', url);
    console.log('🌐 Current page URL:', window.location.href);
    console.log('🌐 Current origin:', window.location.origin);

    const payload = { name, phone };

    console.log('📦 Request payload:', payload);

    try {
        console.log('🚀 Sending POST request...');

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log('✅ Fetch request completed');
        console.log('📡 Response status:', response.status);
        console.log('📡 Response status text:', response.statusText);
        console.log('📡 Response OK:', response.ok);
        console.log('📡 Response URL:', response.url);

        // Log response headers
        console.log('📋 Response headers:');
        for (const [key, value] of response.headers.entries()) {
            console.log(`${key}: ${value}`);
        }

        const responseText = await response.text();

        console.log('📄 Raw response:');
        console.log(responseText);

        let result;

        try {
            result = JSON.parse(responseText);
            console.log('📦 Parsed JSON response:', result);
        } catch (jsonError) {
            console.error('❌ Failed to parse response as JSON');
            console.error('JSON error:', jsonError);
            console.error('Raw response was:', responseText);

            alert('Server returned an invalid response. Check the browser console.');
            return;
        }

        if (response.ok) {
            console.log('🎉 ORDER SUBMITTED SUCCESSFULLY');
            console.log('Server response:', result);

            alert('Thank you! Your order has been received.');

            this.reset();

            console.log('🔄 Form reset completed');

        } else {
            console.error('❌ SERVER RETURNED AN ERROR');
            console.error('Status:', response.status);
            console.error('Error response:', result);

            alert('Error: ' + (result.error || 'Unknown server error'));
        }

    } catch (error) {
        console.error('🔥 FETCH REQUEST FAILED');
        console.error('Error:', error);
        console.error('Error name:', error.name);
        console.error('Error message:', error.message);
        console.error('Full error:', error);

        alert('Something went wrong. Please try again.');
    }

    console.log('====================================');
    console.log('🔴 ORDER FORM SUBMISSION FINISHED');
    console.log('====================================');
});