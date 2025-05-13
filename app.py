import streamlit as st
import pandas as pd
from pyzbar.pyzbar import decode
import cv2
import numpy as np

# CSV faylini o'qish (ma'lumotlar bazasi)
df = pd.read_csv("store_inventory.csv")

# Kamera inputi
st.title("Shtrixkodni skanerlang")

video = st.camera_input("Kameradan video olish")

if video:
    # Videodan rasm olish
    img = cv2.imdecode(np.frombuffer(video.read(), np.uint8), -1)
    barcodes = decode(img)  # Shtrixkodlarni aniqlash

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')  # Shtrixkodni o'qish
        st.write(f"Shtrixkod skanerlandi: {barcode_data}")

        # Ma'lumotlar bazasidan mahsulotni qidirish
        product = df[df['barcode'] == barcode_data]

        if not product.empty:
            # Mahsulotni topdik, miqdorini kamaytirish
            new_quantity = product['quantity'].values[0] - 1
            if new_quantity >= 0:
                df.loc[df['barcode'] == barcode_data, 'quantity'] = new_quantity
                st.write(f"Mahsulot {product['name'].values[0]} miqdori kamaytirildi. Yangi miqdor: {new_quantity}.")
            else:
                # Agar mahsulotda yetarli miqdor bo'lmasa
                st.write(f"{product['name'].values[0]} uchun etarli miqdor yo'q.")
        else:
            st.write("Shtrixkodga mos mahsulot topilmadi.")

        # Yangi ma'lumotlarni CSV faylga saqlash
        df.to_csv("store_inventory.csv", index=False)
