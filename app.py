import streamlit as st
import requests

# --- Config ---
st.set_page_config(page_title="Cinema Scene Scout", page_icon="🦇")
st.title("🦇 Cinema Scene Scout")
st.markdown("---")
st.subheader("Search for scenes in *The Batman (2022)*")
st.write("Example: _'the part where he says he is vengeance'_")

# URL of your local API
API_URL = "http://127.0.0.1:8000/search"

user_query = st.text_input("Describe the scene:", key="search_box")

if user_query:
    with st.spinner("Contacting the Bat-Computer..."):
        try:
            # Send request to API
            payload = {"query": user_query}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                result = response.json().get("answer", "No answer provided.")
                st.success("Result:")
                st.write(result)
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Is 'uvicorn api:app' running?")
        except Exception as e:
            st.error(f"An error occurred: {e}")