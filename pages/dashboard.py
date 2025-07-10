import streamlit as st
import pandas as pd
import time

from utils.auth import require_role

# RBA - Role Based Access.
if require_role(["admin", "user"]) and st.user.is_logged_in:
    st.error("UNAUTHORIZED ACCESS")
    st.stop()

# Page config
st.set_page_config(
    page_title="🏠 Home | Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS for Pro Look ----------
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    header, .reportview-container .main footer {visibility: hidden;}
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        padding: 10px;
        color: #999999;
        text-align: center;
        font-size: 0.8rem;
        border-top: 1px solid #eee;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 style='text-align:center;'>🏠 Welcome to the Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Build smarter apps with clean UI, filters, and insights</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------- KPI / Metric Row ----------
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Active Users", value="1,245", delta="+5.3%")
kpi2.metric(label="Tests Taken", value="389", delta="+12")
kpi3.metric(label="Skill Coverage", value="92%", delta="-1.2%")

st.markdown("---")

# ---------- Main Interactive Section ----------
st.subheader("📌 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("➕ Create New Test")
    st.success("💡 AI Skill Extractor Available")
    st.write("Auto-generate questions based on resume.")

with col2:
    st.button("📤 Upload Resume")
    uploaded_file = st.file_uploader("Upload File", type=["pdf", "docx"])
    if uploaded_file:
        st.success("File uploaded!")

with col3:
    st.button("📄 View Reports")
    st.write("Export your results, question history and insights.")

st.markdown("---")

# ---------- Data Section ----------
st.subheader("📊 Sample User Data")

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Role": ["Student", "Admin", "Teacher"],
    "Score": [87, 92, 78],
    "Completed": [True, True, False]
})
st.dataframe(df, use_container_width=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    © 2025 MyCompany. All rights reserved. &nbsp; | &nbsp;
    <a href="#" target="_blank">Privacy Policy</a> &nbsp; | &nbsp;
    <a href="#" target="_blank">Terms</a>
</div>
""", unsafe_allow_html=True)
