import os

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Cognitive Load Detector", layout="wide")
st.title("Cognitive Load Detector — FLZK Simulator")

st.markdown(
    """
    Run a lightweight simulation of the FLZK protocol as described in the research paper.
    Configure the federated setup, select a proof backend, and launch a training run.
    Results include accuracy, loss, and the evolving privacy budget.
    """
)

with st.form("simulation"):
    col1, col2, col3 = st.columns(3)
    with col1:
        rounds = st.slider("Training rounds", min_value=1, max_value=50, value=10)
        num_peers = st.slider("Peers", min_value=3, max_value=20, value=6)
        samples_per_peer = st.slider("Samples per peer", min_value=32, max_value=1024, value=256, step=32)
    with col2:
        clip_norm = st.slider("Clip norm", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
        noise_multiplier = st.slider("Noise multiplier", min_value=0.5, max_value=3.0, value=1.2, step=0.1)
        learning_rate = st.slider("Learning rate", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
    with col3:
        batch_size = st.select_slider("Batch size", options=[16, 32, 64, 128, 256])
        num_features = st.slider("Feature dims", min_value=4, max_value=16, value=8)
        backend = st.selectbox("Proof backend", options=["mock", "snarkjs"], index=0)
        seed = st.number_input("Seed (optional)", value=0, step=1)

    submitted = st.form_submit_button("Run Simulation")

if submitted:
    payload = {
        "rounds": rounds,
        "num_peers": num_peers,
        "samples_per_peer": samples_per_peer,
        "clip_norm": clip_norm,
        "noise_multiplier": noise_multiplier,
        "learning_rate": learning_rate,
        "batch_size": batch_size,
        "num_features": num_features,
        "seed": int(seed),
        "proof_backend": backend,
    }
    api_url = os.getenv("CLD_API", "http://localhost:8000/simulate")
    with st.spinner("Simulating federated rounds..."):
        resp = requests.post(api_url, json=payload, timeout=120)
    if resp.status_code != 200:
        st.error(f"Simulation failed: {resp.text}")
    else:
        data = resp.json()
        df = pd.DataFrame(data["history"])
        st.success("Simulation complete")
        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
        metrics_col1.metric("Accuracy", f"{data['final_accuracy']:.3f}")
        metrics_col2.metric("Loss", f"{data['final_loss']:.3f}")
        metrics_col3.metric("Epsilon", f"{data['final_epsilon']:.3f}")

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.subheader("Accuracy per round")
            st.line_chart(df.set_index("round_idx")["accuracy"])
        with chart_col2:
            st.subheader("Privacy budget ε")
            st.line_chart(df.set_index("round_idx")["epsilon"])

        st.subheader("Raw history")
        st.dataframe(df)
else:
    st.info("Configure parameters then hit Run Simulation to reproduce the paper's training loop in miniature.")
