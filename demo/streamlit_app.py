import os

import pandas as pd
import requests
import streamlit as st

API_URL = os.getenv("FLZK_API", "http://127.0.0.1:8000")

st.set_page_config(page_title="FLZK Demo", layout="wide")
st.title("FLZK Federated Simulation Demo")

st.write("Configure the simulation parameters and send them to the FastAPI backend.")

with st.form("sim"):
    rounds = st.slider("Rounds", min_value=1, max_value=20, value=5)
    num_peers = st.slider("Peers", min_value=2, max_value=10, value=4)
    proof_backend = st.selectbox("Proof backend", options=["mock", "snark"])
    submitted = st.form_submit_button("Run Simulation")

if submitted:
    payload = {"rounds": rounds, "num_peers": num_peers, "proof_backend": proof_backend}
    with st.spinner("Calling API..."):
        resp = requests.post(f"{API_URL}/simulate", json=payload, timeout=10)
    if resp.status_code != 200:
        st.error(resp.text)
    else:
        data = resp.json()
        st.success("Simulation complete")
        st.write(data)
        st.dataframe(pd.DataFrame(data["metrics"]))
else:
    st.info("Submit the form to run the simulation.")
