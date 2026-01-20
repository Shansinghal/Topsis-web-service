document.getElementById('topsisForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById('file');
    const weightsInput = document.getElementById('weights');
    const impactsInput = document.getElementById('impacts');
    const emailInput = document.getElementById('email');
    const errorMsg = document.getElementById('error-message');
    const successMsg = document.getElementById('success-message');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    // Reset messages
    errorMsg.textContent = '';
    successMsg.textContent = '';

    // Validation
    if (fileInput.files.length === 0) {
        errorMsg.textContent = 'Please select a file.';
        return;
    }

    const weights = weightsInput.value.split(',').map(w => w.trim());
    const impacts = impactsInput.value.split(',').map(i => i.trim());

    if (weights.length !== impacts.length) {
        errorMsg.textContent = 'Number of weights and impacts must be the same.';
        return;
    }

    const validImpacts = impacts.every(i => i === '+' || i === '-');
    if (!validImpacts) {
        errorMsg.textContent = 'Impacts must be either + or -';
        return;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(emailInput.value)) {
        errorMsg.textContent = 'Please enter a valid email address.';
        return;
    }

    // Prepare data
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('weights', weightsInput.value);
    formData.append('impacts', impactsInput.value);
    formData.append('email', emailInput.value);

    // Show loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    loader.style.display = 'block';

    // Determine the API URL
    // If we are on port 5000 (Flask), use relative path.
    // If we are on file:// or another port (e.g. Live Server), point to local Flask server.
    let submitUrl = '/submit';
    if (window.location.protocol === 'file:' ||
        (window.location.hostname === '127.0.0.1' && window.location.port !== '5000') ||
        (window.location.hostname === 'localhost' && window.location.port !== '5000')) {
        submitUrl = 'http://127.0.0.1:5000/submit';
    }

    try {
        const response = await fetch(submitUrl, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            successMsg.textContent = "Result file has been sent to your email successfully.";
            document.getElementById('topsisForm').reset();
        } else {
            errorMsg.textContent = data.error || 'An error occurred during processing.';
        }
    } catch (error) {
        console.error('Submission error:', error);
        errorMsg.textContent = `Failed to connect to the server (${submitUrl}). Check console for details.`;
    } finally {
        // Reset loading state
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        loader.style.display = 'none';
    }
});
