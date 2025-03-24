from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from PIL import Image
import io

app = Flask(__name__)

# Define model architecture exactly as used during training.
def create_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(3, activation='softmax')  # 3 classes: BHtrain, HMtrain, PQtrain
    ])
    return model

# Create the model and load the weights from the file.
model = create_model()
# Note: The weights filename must end with ".weights.h5"
model.load_weights("my_model.weights.h5")

# Mapping from predicted indices to class names.
class_mapping = {
    0: 'BHtrain',
    1: 'HMtrain',
    2: 'PQtrain'
}

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an image file is provided in the POST request.
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        # Open the image, ensure it's in RGB format.
        img = Image.open(file.stream).convert('RGB')
        # Resize the image to match the input shape expected by the model.
        img = img.resize((150, 150))
        # Convert image to numpy array and normalize pixel values.
        img_array = np.array(img) / 255.0
        # Add a batch dimension.
        img_array = np.expand_dims(img_array, axis=0)

        # Run model prediction.
        preds = model.predict(img_array)
        pred_index = np.argmax(preds[0])
        pred_class = class_mapping.get(pred_index, "Unknown")
        
        # Return the predicted class as JSON.
        return jsonify({'prediction': pred_class})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app on all network interfaces
    app.run(host='0.0.0.0', debug=True)
