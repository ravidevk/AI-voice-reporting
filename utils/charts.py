import pandas as pd
import plotly.express as px
import streamlit as st

def render_chart_from_query(query, df):
    if "bar chart" in query.lower():
        col_x, col_y = df.columns[0], df.columns[1]
        fig = px.bar(df, x=col_x, y=col_y)
        st.plotly_chart(fig)
    elif "line chart" in query.lower():
        col_x, col_y = df.columns[0], df.columns[1]
        fig = px.line(df, x=col_x, y=col_y)
        st.plotly_chart(fig)
    elif "pie chart" in query.lower():
        col_names = df.columns[:2]
        fig = px.pie(df, names=col_names[0], values=col_names[1])
        st.plotly_chart(fig)