from flask import Flask, request, jsonify, render_template
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os

app = Flask(__name__)

# Load the trained ML model
MODEL_PATH = 'rice_leaf_model.h5'  # Path to your trained model
model = load_model(MODEL_PATH)

# Define allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']
    if file and allowed_file(file.filename):
        # Save the uploaded image temporarily
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Preprocess the image for prediction
        image = load_img(file_path, target_size=(128, 128))  # Resize to model's input size
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0) / 255.0  # Normalize pixel values

        # Predict using the model
        prediction = model.predict(image)
        os.remove(file_path)  # Clean up the saved image

        # Assuming the model outputs probabilities for 3 classes
        class_names = ['Bacterialblight', 'Brownspot', 'Blast','Tungro']
        predicted_class = class_names[np.argmax(prediction)]

        return jsonify({"prediction": predicted_class})

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
