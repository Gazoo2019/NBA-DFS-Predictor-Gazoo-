import plotly.express as px
import plotly.graph_objects as go
from IPython.display import HTML
from plotly.colors import n_colors
from functions import *

def get_playerlog_plot(player_name, season, logs):
    """
    Returns player plot against average over time
    """
    df = get_player_logs(player_name, season, logs)
    fig = px.line(df, x="GAME_DATE", y="FPG", title="FPG")
    fig.add_hline(y=df["FPG"].mean(), line_width=3, line_dash="dash", line_color="green")
    return fig