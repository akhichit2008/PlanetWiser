from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

@app.route("/plant")
def plant():
    return render_template("plant.html")

@app.route('/detect', methods=['POST'])
def detect_disease():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        try:
            img = PIL.Image.open(file)
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            
            # Enhanced request to model for treatment and recommendation
            response = model.generate_content([
                "Analyze this plant image and provide treatment methods, recommended fertilizers or medicine to cure the disease.",
                img
            ])
            treatment_info = response.text
            treatment_info = re.sub(r'\*', '', treatment_info)
            treatment_info = re.sub(r'([^:\n]*:[^:\n]*\n)\s*:(.+)', r'\1\2', treatment_info)
            return jsonify({"result": treatment_info})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"error": "Failed to process image"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=7878)
