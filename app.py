import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import pandas as pd
import av
from pyzbar.pyzbar import decode
import numpy as np
import cv2

# Ma'lumotlar bazasini yuklash
df = pd.read_csv("store_inventory.csv")

# Barcode aniqlovchi klass
class BarcodeScanner(VideoTransformerBase):
    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        barcodes = decode(image)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            x, y , w, h = barcode.rect
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(image, barcode_data, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 2)

            # Ma'lumotlar bazasida tekshirish
            if barcode_data in df["barcode"].values:
                idx = df[df["barcode"] == barcode_data].index[0]
                if df.at[idx, "quantity"] > 0:
                    df.at[idx, "quantity"] -= 1
                    st.success(f"{df.at[idx, 'name']} mahsuloti 1 taga kamaytirildi!")
                else:
                    st.warning(f"{df.at[idx, 'name']} tugagan!")
                df.to_csv("store_inventory.csv", index=False)

        return image

st.title("Shtrixkod asosidagi inventar nazorat")

webrtc_streamer(key="scanner", video_transformer_factory=BarcodeScanner)
