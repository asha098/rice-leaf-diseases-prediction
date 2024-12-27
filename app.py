from flask import Flask, request, jsonify, render_template
import os
import random

# Flask app initialization
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create folder for file uploads
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simulated AI disease prediction function
def predict_disease():
    diseases = ['Bacterial Blight', 'Brown Spot', 'Blast']
    remedies = {
        'Bacterial Blight': 'Apply copper-based bactericides.',
        'Brown Spot': 'Use proper fungicides and nitrogen fertilizers.',
        'Blast': 'Apply carbendazim or tricyclazole-based fungicides.'
    }
    disease = random.choice(diseases)
    return {"disease": disease, "remedy": remedies[disease]}

# Routes
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"})

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Call prediction function (replace with actual AI model later)
        result = predict_disease()
        return jsonify(result)

    return jsonify({"error": "Invalid file format. Only PNG, JPG, and JPEG are allowed."})

if __name__ == '__main__':
    app.run(debug=True)
