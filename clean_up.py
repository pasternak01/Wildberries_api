import os
import glob
import streamlit as st
from streamlit import session_state

if 'session_id' in session_state:
    session_id = session_state['session_id']

def cleanup_session_files(session_id):
    files = glob.glob(f"uploaded_files/*_{session_id}.*")
    for f in files:
        try:
            os.remove(f)
        except Exception as ex:
            st.warning(f"Problem: {ex}")

def cleanup_all_temp_data():
    files  = glob.glob('uploaded_files/*')
    for f in files:
        try:
            os.remove(f)
        except Exception as ex:
            st.warning(f"Problem: {ex}")