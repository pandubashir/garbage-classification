# 🗑️ Garbage Classification

A deep learning web application that classifies waste images into 6 categories using Transfer Learning with ResNet50. Built with TensorFlow and deployed via Flask on Railway.

**Live Demo:** [your-app.up.railway.app](https://your-app.up.railway.app) ← *update after deploy*

---

## 📌 Project Overview

Improper waste sorting is one of the key barriers to effective recycling. This project demonstrates how computer vision can automate waste classification — a task that is repetitive, error-prone when done manually, and critical for environmental impact.

Given an image of a waste item, the model identifies which of 6 categories it belongs to, along with a confidence score and Top-3 predictions.

---

## 🧩 Categories

| Class | Description |
|-------|-------------|
| 📦 Cardboard | Boxes, packaging, cartons |
| 🫙 Glass | Bottles, jars, containers |
| 🔩 Metal | Cans, foil, scrap metal |
| 📄 Paper | Newspapers, magazines, office paper |
| 🧴 Plastic | Bottles, bags, containers |
| 🗑️ Trash | General waste, non-recyclable items |

---

## 📊 Model Performance

**Validation Accuracy: 92.4%** &nbsp;|&nbsp; **Validation Loss: 0.231**

### Classification Report

| Class | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Cardboard | 1.00 | 0.90 | 0.95 | 40 |
| Glass | 0.96 | 0.86 | 0.91 | 50 |
| Metal | 0.89 | 0.98 | 0.93 | 41 |
| Paper | 0.91 | 0.98 | 0.94 | 59 |
| Plastic | 0.92 | 0.92 | 0.92 | 48 |
| Trash | 0.85 | 0.85 | 0.85 | 13 |
| **Weighted Avg** | **0.93** | **0.92** | **0.92** | **251** |

**Key observations:**
- Cardboard achieves perfect precision (1.00) — no false positives
- Metal has the highest recall (0.98) — rarely missed
- Trash has the lowest F1 (0.85), likely due to its small support (only 13 samples)

> 📓 Full training process, confusion matrix, and training history are documented in [`notebook/Garbage_Classification_ResNet.ipynb`](notebook/Garbage_Classification_ResNet.ipynb)

---

## 🏗️ Model Architecture

**Base Model:** ResNet50 (pre-trained on ImageNet, `include_top=False`)

```
ResNet50 (frozen)           → Feature extractor
GlobalAveragePooling2D      → Spatial pooling
Dense(512, relu)            → Classification head
BatchNormalization + Dropout(0.2)
Dense(128, relu)
BatchNormalization + Dropout(0.2)
Dense(6, softmax)           → Output: 6 classes
```

**Input size:** 224 × 224 × 3

---

## 🔁 Transfer Learning Strategy

Training was done in two phases:

**Phase 1 — Feature Extraction**
- ResNet50 base frozen (weights locked)
- Only the custom head is trained
- Optimizer: Adam (lr=0.0001)
- Allows fast convergence without overfitting

**Phase 2 — Fine-Tuning**
- ResNet50 base unfrozen
- Full network trained end-to-end with a lower learning rate
- Callbacks: `EarlyStopping`, `ReduceLROnPlateau`

This two-phase approach is standard practice for transfer learning on small datasets — it stabilizes training and consistently outperforms training from scratch.

---

## 📁 Project Structure

```
garbage-classification/
│
├── app.py                  # Flask app factory + configuration
├── routes/
│   ├── __init__.py
│   └── prediction.py       # Route handlers
├── utils/
│   ├── __init__.py
│   ├── predictor.py        # Model loading + inference logic
│   └── file_handler.py     # File validation + upload handling
├── model/
│   └── garbage_cnn.h5      # Trained model weights
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── uploads/
├── templates/
│   └── index.html
├── notebook/
│   └── Garbage_Classification_ResNet.ipynb
│
├── requirements.txt
├── Procfile
├── runtime.txt
└── .gitignore
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Deep Learning | TensorFlow 2.12, Keras |
| Base Model | ResNet50 (ImageNet weights) |
| Web Framework | Flask 2.3 |
| Production Server | Gunicorn |
| Deployment | Railway |
| Language | Python 3.10 |

---

## ⚙️ Local Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/garbage-classification.git
cd garbage-classification
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

> ⚠️ TensorFlow 2.12 requires approximately 1–1.5 GB of RAM when running. Ensure your machine has at least 4 GB available.

**4. Verify model file exists**
```
model/garbage_cnn.h5
```

**5. Run the app**
```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🚀 Deploy to Railway

**1. Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/garbage-classification.git
git push -u origin main
```

**2. Deploy on Railway**
- Go to [railway.app](https://railway.app) → New Project
- Select **Deploy from GitHub repo**
- Choose your repository
- Railway auto-detects Python via `requirements.txt`

**3. Set environment variable** *(optional but recommended)*
```
SECRET_KEY = your-random-secret-key
```

**4. Generate domain**
- Settings → Networking → **Generate Domain**

> The app may take 60–90 seconds on first load (cold start) while TensorFlow loads the model into memory. Subsequent requests are fast.

---

## 📦 Dataset

- **Source:** [Garbage Classification Dataset](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification) on Kaggle
- **Classes:** 6 (cardboard, glass, metal, paper, plastic, trash)
- **Split:** 90% training / 10% validation (`validation_split=0.1`)

---

## 🔮 Future Improvements

- [ ] Add more waste categories (e-waste, organic, hazardous)
- [ ] Expand dataset — current trash class has only 13 validation samples
- [ ] Export model to TFLite for mobile deployment
- [ ] Add batch prediction endpoint (`/api/predict`)
- [ ] Add Grad-CAM visualization to highlight which part of the image the model focused on

---

## 👤 Author

**[Your Name]**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)

---

*Built as part of a Machine Learning Engineering portfolio project.*
