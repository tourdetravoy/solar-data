import streamlit as st
import inspect
import textwrap
import pandas as pd
import altair as alt

from urllib.error import URLError


def data_frame_demo():
    @st.experimental_memo
    def get_ember_data():
        df = pd.read_csv("embersolar2305.csv")
        return df.set_index("country_or_region")

    try:
        df = get_ember_data()
        countries = st.multiselect(
            "Choose country or region", list(df.index.unique()), ["China"]
        )
        if not countries:
            st.error("Please select at least one region.")

        else:
            data = df.loc[countries]

            chart = (
                alt.Chart(data, width=1200, height=600)
                .mark_bar(color='yellow')
                .encode(
                    x="date:T",
                    y=alt.Y("generation_pct:Q", stack=None),
                    tooltip=['date:T', 'generation_pct', 'generation_twh'],
                )
            )
            st.altair_chart(chart)

            st.write("### Electricity Generation - Solarpower Percentage (%)", data.sort_index())

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )

st.set_page_config(layout="wide", page_title="Solarpower Production", page_icon="📊", initial_sidebar_state="collapsed")
st.markdown("# Solarpower")
st.write(
"""This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [Ember Data Explorer](https://ember-climate.org/data/data-tools/data-explorer/).)"""
)

data_frame_demo()
