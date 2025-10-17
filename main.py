import streamlit as st
import pandas as pd
import os
import io
import base64
from PIL import Image
from bot import chat_with_data
from supabase import create_client, Client
from security import DOS_prevention

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_message(chat_container):
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message.get("is_image"):
                    decoded_image = base64.b64decode(message["content"])
                    img = Image.open(io.BytesIO(decoded_image))
                    st.image(img)
                else:
                    st.markdown(message["content"])

def main_page(username):
    st.title("Data Lens")
    df = None

    uploaded_files = st.file_uploader(
        "Choose a file (xls/csv)",
        type=["csv", "xls"],
        accept_multiple_files=True
    ) ## extension validation

    for file in uploaded_files:
        if(not DOS_prevention(file, 50)):
            st.warning("Uploaded file is too larged")
            st.stop()

    if uploaded_files:
        files = [file.name for file in uploaded_files]
        selected_file = st.selectbox("Select file:", files)
        file_to_display = next((f for f in uploaded_files if f.name == selected_file), None)

        if file_to_display:
            if file_to_display.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(file_to_display)
            else:
                df = pd.read_csv(file_to_display)

            st.subheader(f"Preview: {selected_file}")
            no = st.number_input("Enter number of rows you want to view", step=1)
            st.write(df.head(int(no)))

    with st.expander("💬 Chat with your data", expanded=False):
        if "messages" not in st.session_state:
            st.session_state.messages = []
            res = supabase.table("messages").select("content, role, is_image").eq("username", username).execute()
            if res.data:
                st.session_state.messages = res.data
        chat_container = st.container(height=300)
        load_message(chat_container)

        if prompt := st.chat_input("Type here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # load_message(chat_container)
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)


            if df is None:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Please upload a file to unlock this feature 😁",
                })
                st.rerun()

            with st.spinner("Thinking..."):
                response = chat_with_data(df, prompt)

            if str(type(response)) == "<class 'pandasai.core.response.chart.ChartResponse'>":
                image = Image.open(response.value)
                output = io.BytesIO()
                image.save(output, format="png")
                image_bytes = output.getvalue()
                image_string = base64.b64encode(image_bytes).decode("utf-8")
                new_msg = {"role": "assistant", "content": image_string, "is_image": True}
            else:
                new_msg = {"role": "assistant", "content": str(response), "is_image": False}

            st.session_state.messages.append(new_msg)

            supabase.table("messages").upsert([
                {"username": username, "content": msg["content"], "role": msg["role"], "is_image": msg.get("is_image", False)}
                for msg in st.session_state.messages
            ]).execute()

            st.rerun()
            # load_message(chat_container)
