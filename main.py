import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re

# =========================
# Load model + scaler
# =========================
model = pickle.load(open('laptop_price_predictor_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

# =========================
# MUST match training columns exactly
# =========================
model_columns = [
    'Inches', 'Ram', 'Weight', 'SSD', 'HDD', 'Flash', 'Hybrid',
    'CPU_GHz', 'IPS', 'Touchscreen', 'X_res', 'Y_res', 'Pixels',
    'Company_Acer', 'Company_Apple', 'Company_Asus', 'Company_Chuwi',
    'Company_Dell', 'Company_Fujitsu', 'Company_Google', 'Company_HP',
    'Company_Huawei', 'Company_LG', 'Company_Lenovo', 'Company_MSI',
    'Company_Mediacom', 'Company_Microsoft', 'Company_Razer',
    'Company_Samsung', 'Company_Toshiba', 'Company_Vero', 'Company_Xiaomi',
    'TypeName_Gaming', 'TypeName_Netbook', 'TypeName_Notebook',
    'TypeName_Ultrabook', 'TypeName_Workstation',
    'OpSys_Chrome OS', 'OpSys_Linux', 'OpSys_Mac OS X', 'OpSys_No OS',
    'OpSys_Windows 10', 'OpSys_Windows 10 S', 'OpSys_Windows 7',
    'OpSys_macOS',
    'CPU_Brand_Intel', 'CPU_Brand_Samsung',
    'CPU_Type_Other', 'CPU_Type_Pentium', 'CPU_Type_Ryzen',
    'CPU_Type_Xeon', 'CPU_Type_i3', 'CPU_Type_i5', 'CPU_Type_i7'
]

scale_cols = [
    'Inches', 'Ram', 'Weight',
    'CPU_GHz', 'Pixels',
    'SSD', 'HDD', 'Flash', 'Hybrid',
    'X_res', 'Y_res'
]

# =========================
# LOGICAL BRAND RULES
# =========================

BRAND_TYPES = {
    "Apple": ["Ultrabook", "Notebook"],
    "Dell": ["Ultrabook", "Notebook", "Gaming", "Workstation"],
    "HP": ["Ultrabook", "Notebook", "Gaming", "Workstation"],
    "Lenovo": ["Ultrabook", "Notebook", "Gaming", "Workstation"],
    "Asus": ["Notebook", "Gaming", "Ultrabook"],
    "Acer": ["Notebook", "Gaming", "Ultrabook"],
    "MSI": ["Gaming", "Workstation"],
    "Microsoft": ["Ultrabook"],
    "Razer": ["Gaming"],
    "Samsung": ["Ultrabook", "Notebook"],
    "Toshiba": ["Notebook", "Ultrabook"],
    "Xiaomi": ["Notebook", "Ultrabook"]
}

BRAND_CPU = {
    "Apple": ["i5", "i7"],
    "MSI": ["i7", "i9", "Xeon"],
    "Razer": ["i7", "i9"],
    "Microsoft": ["i5", "i7"],
    "Default": ["i3", "i5", "i7", "Ryzen"]
}

CPU_BRAND_MAP = {
    "i3": "Intel",
    "i5": "Intel",
    "i7": "Intel",
    "i9": "Intel",
    "Xeon": "Intel",
    "Pentium": "Intel",
    "Celeron": "Intel",
    "Ryzen": "AMD"
}

BRAND_OS = {
    "Apple": ["macOS"],
    "Microsoft": ["Windows 10"],
    "Google": ["Chrome OS"]
}

# =========================
# UI
# =========================
st.title("💻 Laptop Price Predictor (Logical Version)")

company = st.selectbox("Company", list(BRAND_TYPES.keys()))

type_name = st.selectbox(
    "Type",
    BRAND_TYPES.get(company, ["Notebook"])
)

ram = st.selectbox("RAM (GB)", [2, 4, 6, 8, 12, 16, 24, 32, 64])
weight = st.number_input("Weight (kg)", 0.5, 5.0, 1.5, 0.1)
inches = st.number_input("Screen Size", 10.0, 20.0, 15.6, 0.1)

cpu_type = st.selectbox(
    "CPU Type",
    BRAND_CPU.get(company, BRAND_CPU["Default"])
)

cpu_brand = CPU_BRAND_MAP[cpu_type]
cpu_ghz = st.number_input("CPU GHz", 1.0, 5.0, 2.5, 0.1)

ssd = st.number_input("SSD (GB)", 0, 2048, 256, 128)
hdd = st.number_input("HDD (GB)", 0, 2000, 0, 250)
flash = st.number_input("Flash (GB)", 0, 512, 0, 32)
hybrid = st.number_input("Hybrid (GB)", 0, 2000, 0, 500)

opsys = st.selectbox(
    "Operating System",
    BRAND_OS.get(company, ["Windows 10", "Linux", "No OS"])
)

screen = st.selectbox(
    "Resolution",
    ["1366x768", "1920x1080", "2560x1440", "3840x2160"]
)

# =========================
# PREDICTION
# =========================
if st.button("Predict Price"):

    # create clean input
    x = pd.DataFrame(0, index=[0], columns=model_columns)

    # numeric
    x["Inches"] = inches
    x["Ram"] = ram
    x["Weight"] = weight
    x["SSD"] = ssd
    x["HDD"] = hdd
    x["Flash"] = flash
    x["Hybrid"] = hybrid
    x["CPU_GHz"] = cpu_ghz

    # screen parsing (STRICT)
    w, h = map(int, screen.split("x"))
    x["X_res"] = w
    x["Y_res"] = h
    x["Pixels"] = w * h

    x["IPS"] = 0
    x["Touchscreen"] = 0

    # one-hot safe assignment
    def set_if_exists(col):
        if col in x.columns:
            x.loc[0, col] = 1

    set_if_exists(f"Company_{company}")
    set_if_exists(f"TypeName_{type_name}")
    set_if_exists(f"OpSys_{opsys}")
    set_if_exists(f"CPU_Type_{cpu_type}")
    set_if_exists(f"CPU_Brand_{cpu_brand}")

    # scaling ONLY trained columns
    x_scaled = x.copy()
    x_scaled[scale_cols] = scaler.transform(x_scaled[scale_cols])

    # prediction
    price = model.predict(x_scaled)[0][0]

    st.success(f"💰 Predicted Price: ${price:,.2f}")