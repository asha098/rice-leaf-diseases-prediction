from flask import Flask, request, jsonify, render_template
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load trained deep learning model
MODEL_PATH = "rice_leaf_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Define class labels and remedies
CLASS_LABELS = ['Bacterial Blight', 'Blast', 'Brown Spot', 'Tungro']
REMEDIES = {
    'Bacterial Blight': 'Use resistant varieties and avoid excessive nitrogen fertilizer.',
    'Blast': 'Apply fungicides and maintain proper field drainage.',
    'Brown Spot': 'Use balanced fertilizer and avoid water stress.',
    'Tungro': 'Control vector insects and use resistant rice varieties.'
}

# **Flask Routes for Pages**
@app.route('/')
def index():
    return render_template('index.html')  # Fixed function name

@app.route('/resources')
def resources():
    return render_template('resources.html')  # Fixed function name

@app.route('/about')
def about():
    return render_template('about.html')  # Fixed function name

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')  # Fixed function name

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Fixed function name

# **Function to Preprocess the Image**
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(128, 128))  # Resize image
    img_array = image.img_to_array(img)  # Convert to array
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize
    return img_array

# **Flask Route for Prediction**
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # Secure the filename and save the file
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    # Preprocess and predict
    img_array = preprocess_image(file_path)
    predictions = model.predict(img_array)
    
    predicted_class_index = np.argmax(predictions, axis=1)[0]  # Get class index
    confidence = float(np.max(predictions))  # Get confidence score

    if predicted_class_index >= len(CLASS_LABELS):
        return jsonify({'error': 'Invalid class index predicted'}), 400

    predicted_class = CLASS_LABELS[predicted_class_index]
    remedy = REMEDIES.get(predicted_class, "No remedy available.")

    return jsonify({
        'disease': predicted_class,
        'confidence': confidence,
        'remedy': remedy
    })

# **Run Flask app**
if __name__ == '__main__':
    app.run(debug=True)
