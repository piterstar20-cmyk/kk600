import os
from flask import Flask, request, jsonify, send_file
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__)

# کلید API در متغیر محیطی (محلی)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    prompt = request.form.get("prompt", "What is in this picture?")

    try:
        # باز کردن تصویر
        img = Image.open(file.stream)
        response = model.generate_content([img, prompt])
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)