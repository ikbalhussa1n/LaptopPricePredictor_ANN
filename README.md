# 💻 Laptop Price Predictor (ANN + Streamlit)

A machine learning web application that predicts laptop prices based on hardware specifications using a trained Artificial Neural Network (ANN). Built with **Streamlit** for an interactive UI.

---

## 🚀 Live Demo

👉 https://laptoppricepredictorann-2azan2jfblzs97ooqrtdkt.streamlit.app/

---

## 📌 Project Overview

This project predicts laptop prices using a deep learning regression model trained on laptop specifications.

Users can select different configurations like:

- Brand (Company)
- Laptop Type
- RAM & Storage
- CPU Type & Speed
- Screen Resolution
- Operating System
- Weight and Screen Size

The model processes these inputs and outputs an estimated price in USD.

---

## 🧠 Machine Learning Model

- **Model Type:** Artificial Neural Network (ANN)
- **Framework:** TensorFlow / Keras
- **Scaler:** StandardScaler (scikit-learn)
- **Problem Type:** Regression

---

## 📁 Project Structure 

LaptopPricePredictor/
│
├── 📄 main.py
│     → Streamlit web application (UI + prediction logic)
│
├── 🤖 laptop_price_predictor_model.pkl
│     → Trained Artificial Neural Network (ANN) model
│
├── ⚙️ scaler.pkl
│     → StandardScaler used for feature scaling
│
├── 📦 requirements.txt
│     → List of required Python dependencies
│
└── 📘 README.md
      → Project documentation and usage guide


---

## ⚙️ Features Used

### 📊 Numerical Features
- Inches (Screen size)
- RAM (GB)
- Weight (kg)
- CPU Speed (GHz)
- SSD (GB)
- HDD (GB)
- Flash Storage (GB)
- Hybrid Storage (GB)
- Screen Resolution (X, Y pixels)
- Total Pixels

### 🖥️ Categorical Features
- Company (Brand)
- Type Name
- Operating System
- CPU Type
- CPU Brand

---

## 🧾 How It Works

1. User enters laptop specifications in UI
2. Input is converted into a structured feature vector
3. Feature scaling is applied using StandardScaler
4. ANN model predicts laptop price
5. Output is displayed instantly

---

## ▶️ Run Locally

### 1️⃣ Clone repository
```bash
git clone https://github.com/your-username/laptop-price-predictor.git

cd laptop-price-predictor

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run Streamlit app
streamlit run main.py

📦 Requirements
streamlit
pandas
numpy
scikit-learn
tensorflow
pickle-mixin

