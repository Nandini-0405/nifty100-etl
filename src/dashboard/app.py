import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Nifty 100 Analytics Dashboard")

st.markdown(
    """
    Welcome to the Nifty 100 Analytics dashboard.

    Use the sidebar to navigate between screens.
    """
)

st.sidebar.success(
    "Choose a page from the sidebar."
)