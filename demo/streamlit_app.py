import streamlit as st
import requests, json

st.title("Cognitive Load Detector — Demo")
if st.button("Run Sample Inference"):
    payload = {"audio_feats":[0.1,0.2], "video_feats":[0.05,0.9], "clicks_per_min":12}
    r = requests.post("http://localhost:8000/infer", json=payload, timeout=10)
    st.json(r.json())