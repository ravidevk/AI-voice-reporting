import streamlit as st
# Inject custom CSS to style the group headers
st.markdown("""
    <style>
    .st-emotion-cache-1lcbmhc, .st-emotion-cache-18ni7ap {
        font-size: 5.2rem !important;   /* Increase size */
        font-weight: bold;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)
pages = {
    "🙍🏻‍ Your account": [
        st.Page("login.py", title="🏠 Home"),
        st.Page("pages/dashboard.py", title="📊 Generate Dashboard"),
    ],
    "📑 Resources": [
        st.Page("pages/notes.py", title="📄️Notes"),

    ],
    "📑 AI Assistant": [
        st.Page("pages/voice_report.py", title="🤖️AI Voice Reporting"),

    ],
}

pg = st.navigation(pages)
pg.run()


