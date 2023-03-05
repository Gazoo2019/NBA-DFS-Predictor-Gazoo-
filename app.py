# Import the libraries for Pandas and Streamlit
import streamlit as st
from functions import *
from graphs import *

st.write("# Gazoo Web Application")

st.title("SPAM")
st.markdown('''##### <span style="color:gray">Projected DFS points for NBA players</span>
            ''', unsafe_allow_html=True)

tab_player, tab_team = st.tabs(["Lineup", "Player Lookup"])


df = get_projection_data()
df = df.sort_values(by='Projected_Pts', ascending=False)
    # style = df.style.hide_index()

regular_search_term =df.Tm.unique().tolist()

choices = st.multiselect(" ",regular_search_term)

tab_player.write(df[df.Tm.isin(choices)].style.hide_index().to_html(), unsafe_allow_html=True)



player_search_term =df.Player.unique().tolist()
choices = tab_team.selectbox(" ",player_search_term)

tab_team.write(get_playerlog_plot(choices,2022,10))

col1, col2, col3 = st.sidebar.columns([1,8,1])
with col1:
    st.write("")
with col2:
    st.image('imgs/Gazoo.jpg',  use_column_width=True)
with col3:
    st.write("")
st.sidebar.markdown(" ## About Gazoo")
st.sidebar.markdown("Gazoo is Daily Fantasy Sports (DFS) forecasting dashboard. It projects points based on basic player stats that go into the calcuation of player fantasy points.\
                    Data is streamed from various static and dynamic sources with majority of the data coming from basketball-reference, rotowire and covers.com")              
st.sidebar.info("Read more about how the forecasts work and see the code on my [Github](https://github.com/Gazoo2019/NBA-DFS-Predictor-Gazoo-).", icon="ℹ️")


