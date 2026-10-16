from flask import Flask, render_template, request
from PIL import Image
from transformers import pipeline
from werkzeug.utils import secure_filename
import io
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Model downloads the first time it is used. CPU inference is used for compatibility.
from functools import lru_cache

@lru_cache(maxsize=1)
def get_classifier():
    print("Loading AI model... Please wait.")
    classifier = pipeline(
        "image-classification",
        model="yangy50/garbage-classification",
        device=-1
    )
    print("AI model loaded successfully!")
    return classifier

GUIDANCE = {
    "cardboard": "Keep cardboard clean and dry. Flatten boxes and check local paper/cardboard recycling rules.",
    "glass": "Handle broken glass carefully. Check whether your local collection accepts this type of glass.",
    "metal": "Empty containers where practical and check local metal recycling rules.",
    "paper": "Keep paper clean and dry. Greasy or contaminated paper may not be recyclable.",
    "plastic": "Empty the item and check local recycling rules. Not every plastic item is accepted for recycling.",
    "trash": "Check whether the item can be reused or recycled locally before placing it in general waste."
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        file = request.files.get("waste_image")

        if not file or file.filename == "":
            error = "Please choose an image first."
        elif not allowed_file(file.filename):
            error = "Please upload a PNG, JPG, or JPEG image."
        else:
            try:
                image_bytes = file.read()
                image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
                predictions = get_classifier()(image, top_k=3)
                best = predictions[0]
                category = best["label"].strip().lower()

                result = {
                    "filename": secure_filename(file.filename),
                    "category": category.title(),
                    "confidence": round(float(best["score"]) * 100, 1),
                    "guidance": GUIDANCE.get(
                        category,
                        "Check local waste-sorting guidance for this item."
                    ),
                    "predictions": [
                        {
                            "label": item["label"].replace("_", " ").title(),
                            "score": round(float(item["score"]) * 100, 1)
                        }
                        for item in predictions
                    ]
                }
            except Exception as exc:
                app.logger.exception("Classification failed")
                error = (
                    "The AI model could not classify this image. "
                    "Check your internet connection and terminal output, then try again."
                )

    return render_template("index.html", result=result, error=error)

@app.errorhandler(413)
def too_large(_error):
    return render_template(
        "index.html",
        result=None,
        error="That image is too large. Please upload an image smaller than 8 MB."
    ), 413

if __name__ == "__main__":
    app.run(debug=True)
