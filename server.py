import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image

app = Flask(__name__)

# کلید API از متغیر محیطی
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    prompt = request.form.get("prompt")  # پرامپت از آردینو

    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        img = Image.open(file.stream)
        response = model.generate_content([img, prompt])
        return jsonify({"answer": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
