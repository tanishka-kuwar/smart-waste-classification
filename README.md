# Smart Waste Classification System Using AI

A student project prototype that uses a pretrained image-classification model to predict common waste categories and display basic sorting guidance. The interface is built with HTML and CSS, and Flask connects the frontend to the Python AI model.

## Features
- Upload PNG/JPG/JPEG images
- AI-based image classification
- Predicted category and model confidence score
- Top-three model predictions
- Basic waste sorting guidance
- Responsive HTML/CSS interface

## Supported model categories
The selected pretrained model is intended for cardboard, glass, metal, paper, plastic, and trash. Model predictions can be wrong and should not be treated as verified disposal instructions.

## Requirements
- Python 3.10 recommended
- Internet connection for the first model download
- VS Code or another Python editor

## Run locally (Windows PowerShell)

Create and activate a virtual environment:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the app:

```powershell
python app.py
```

Open http://127.0.0.1:5000 in your browser. The first classification may take a while because the model downloads the first time it is used.

## GitHub upload
Do not upload the `.venv` folder or model cache. Commit the source code, templates, static assets, README, and requirements file.

## Limitations
- This is a prototype, not a certified waste-management tool.
- Predictions depend on image quality and model limitations.
- Confidence score is not the same as real-world accuracy.
- Sorting advice must be checked against local municipal rules.
