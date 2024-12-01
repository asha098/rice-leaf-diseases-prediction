function predictDisease() {
    const fileInput = document.getElementById('leafImage');
    const predictionResult = document.getElementById('predictionResult');
    const imagePreview = document.getElementById('imagePreview');

    if (fileInput.files.length === 0) {
      alert("Please select an image to upload.");
      return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('leafImage', file);

    // Display image preview
    const reader = new FileReader();
    reader.onload = function (e) {
      imagePreview.innerHTML = `<img src="${e.target.result}" alt="Leaf Image" style="max-width: 300px; max-height: 300px;"/>`;
    };
    reader.readAsDataURL(file);

    // Call backend
    fetch('/predict', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        predictionResult.textContent = `Predicted Disease: ${data.prediction}`;
      })
      .catch(error => {
        console.error("Error:", error);
        predictionResult.textContent = "Error predicting the disease.";
      });
  }
