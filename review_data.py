import streamlit as st
import pandas as pd
import random

st.title("Review Page")

df = pd.DataFrame(
    {
        "Index":[1,2,3,4,5]
        "Document_name": ["Index", "", "Delete"],
        "url": ["https://roadmap.streamlit.app", "https://extras.streamlit.app", "https://issues.streamlit.app"],
        #"remove":
        "stars": [random.randint(0, 1000) for _ in range(3)],
        "views_history": [[random.randint(0, 5000) for _ in range(30)] for _ in range(3)],
    }
)

st.dataframe(
    df,
    column_config={
        "Document_name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    width=300,height=150
)