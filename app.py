from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io

# Initialize Flask app
app = Flask(__name__)
CORS(app)
# Set the directory to serve static files (images)
app.config['UPLOAD_FOLDER'] = 'saved_images'
app.config['STATIC_FOLDER'] = 'static'  # Flask will serve files from here

# Load the YOLO model
model = YOLO('8024.pt')  # Update with your model path

# Create a folder for saving images if it doesn't exist
output_folder = app.config['UPLOAD_FOLDER']
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Endpoint to handle image upload and object detection
@app.route('/detect', methods=['POST'])
def detect():
    # Check if a file is provided in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        # Read the uploaded image
        img = Image.open(file.stream)

        # Run the image through the YOLO model
        results = model(img)

        # Extract the first result (image detection result)
        result = results[0]

        # Use the 'to_df()' method to convert detection results to a Pandas DataFrame
        detections = result.to_df()  # Get detection results as a Pandas DataFrame

        # Count occurrences of each detected class
        class_counts = {}
        for _, row in detections.iterrows():
            class_name = row['name']  # Get the class name from the 'name' column
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        # Prepare the result description as a string
        result_description = ", ".join([f"{count} {class_name}" for class_name, count in class_counts.items()])
        
        # Define the path for saving the result image
        result_image_name = 'result_image.png'
        result_image_path = os.path.join(output_folder, result_image_name)
        
        # Save the result image (with detections) to a file on the server
        result.save(result_image_path)

        # Return the result object with class counts and the image link
        return jsonify({
            'result_description': result_description,
            'result_image_path': f'/static/{result_image_name}'  # Serving image as static file
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Serve static files from the 'saved_images' directory
@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory(output_folder, filename)


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

