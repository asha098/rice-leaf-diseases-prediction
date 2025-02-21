const uploadForm = document.getElementById('uploadForm');
const imagePreview = document.getElementById('imagePreview');
const predictionResult = document.getElementById('predictionResult');

uploadForm.addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent page reload

    const fileInput = document.getElementById('leafImage');
    const file = fileInput.files[0];

    if (!file) {
        predictionResult.textContent = 'Please upload an image of the rice leaf.';
        return;
    }

    // Preview the uploaded image
    const reader = new FileReader();
    reader.onload = function (e) {
        imagePreview.innerHTML = `
            <img src="${e.target.result}" alt="Leaf Image" style="max-width: 300px; max-height: 300px;" />
        `;
    };
    reader.readAsDataURL(file);

    predictionResult.textContent = 'Processing...';

    // Send file to Flask API
    const formData = new FormData();
    formData.append('file', file);

    fetch('/predict', {  // Ensure this URL matches Flask API
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Response Data:", data); // Debugging
        if (data.error) {
            predictionResult.textContent = `Error: ${data.error}`;
        } else {
            predictionResult.innerHTML = `
                Detected Disease: <strong>${data.disease}</strong><br>
                Remedy: ${data.remedy}
            `;
        }
    })
    .catch(error => {
        predictionResult.textContent = 'Error: Something went wrong.';
        console.error('Error:', error);
    });
});
