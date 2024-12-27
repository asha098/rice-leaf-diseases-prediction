const uploadForm = document.getElementById('uploadForm');
const imagePreview = document.getElementById('imagePreview');
const predictionResult = document.getElementById('predictionResult');

// Image Upload Form
uploadForm.addEventListener('submit', function (e) {
    e.preventDefault();//read loading the page

    const fileInput = document.getElementById('leafImage');
    const file = fileInput.files[0];
    const reader = new FileReader();

    if (file) {
        // Preview the uploaded image
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.innerHTML = `
                <img src="${e.target.result}" alt="Leaf Image" style="max-width: 300px; max-height: 300px;" />
            `;
        };
        reader.readAsDataURL(file);

        predictionResult.textContent = 'Processing...';

        // Send the file to the backend (Flask API)
        const formData = new FormData();
        formData.append('file', file);


        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
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
    } else {
        predictionResult.textContent = 'Please upload an image of the rice leaf.';
    }
});


