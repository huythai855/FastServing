import streamlit as st
import requests
import time

st.write("Fill in the form below and click create  button to create a new deployment")

st.text("")
st.text("")

with st.form("create_form"):
    deployment_name = st.text_input("Deployment name")
    description = st.text_area("Description")
    model_url = st.text_input("Model URL (from Hugging Face)")
    image_url = st.text_input("Image URL (from Docker Hub)")
    port = st.number_input("Port", min_value=0, max_value=65535, value=1809)

    submitted = st.form_submit_button("Create")
    if submitted:
        with st.spinner('Creating deployment...'):
            response = requests.post(
                "http://127.0.0.1:1409/api/deployments/create",
                headers={"Content-Type": "application/json"},
                json={
                    "name": deployment_name,
                    "description": description,
                    "model_url": model_url,
                    "image_url": image_url,
                    "port": port
                }
            )
        if response.ok:
            st.toast("✅ Deployment created successfully!")
            time.sleep(3)
            st.markdown("Deployment created successfully!")
            st.link_button("Back to menu", "http://localhost:8501/")
        else:
            st.toast("❌ Error creating deployment")




