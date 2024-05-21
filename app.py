import streamlit as st
from predict_page import show_predict_page
from explore_page import show_explore_page
from visualize_page import show_visualize_page

page = st.sidebar.selectbox(":red[Predict or Explore or Visualize]", ("Predict", "Explore Disease Categories", "Visualize Infant Mortality Rates"))

if page == "Predict":
    show_predict_page()
if page == "Explore Disease Categories":
    show_explore_page()
if page == "Visualize Infant Mortality Rates":
    show_visualize_page()