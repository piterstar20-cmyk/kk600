import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from PIL import Image
import logging

app = Flask(__name__)

# لاگ برای دیباگ
logging.basicConfig(level=logging.INFO)

# تنظیم API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in environment variables!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")  # یا gemini-2.0-flash-latest

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        file = request.files['image']
        prompt = request.form.get("prompt", "What is in this picture?")
        
        img = Image.open(file.stream)
        response = model.generate_content([prompt, img])
        
        return jsonify({"answer": response.text})
    
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
