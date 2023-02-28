#Import the libraries
import os
from pathlib import Path
import pandas as pd
import numpy as np 

from nba_api.stats.static import players
from nba_api.stats.static import teams 
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.library.parameters import NumberOfGames, SeasonAll, SeasonTypeAllStar, LeagueIDNullable

def get_fantasy_df():
    """
    Read in csv files from data file and return only valuable dataset to us.
    Will be automated to account for different years
    """
    csv_path = Path("data/2023.csv")
    player_df = pd.read_csv(csv_path)
    player_df['FPG'] = 1* player_df['PTS'] + 0.5*player_df['3P'] + 1.25*player_df['TRB'] + 1.5*player_df['AST'] + 2*player_df['STL'] + 2*player_df['BLK'] -0.5*player_df['TOV'] 
    player_df['FPM'] = player_df['FPG']/player_df['MP']
    fantasy_df = player_df[['Player', 'Tm', 'Pos', 'MP', 'PTS', '3P', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'FPG', 'FPM']]
    fantasy_df = fantasy_df.drop_duplicates(subset = ['Player'], keep='last')
    
    return fantasy_df

def get_lines_data():
    """
    2023 Lines data sourced from covers.com.
    Function reads and cleans csv file
    """
    csv_path = Path("data/Lines.csv")
    lines_df = pd.read_csv(csv_path)
    lines_df["AvL"] = lines_df['PPG'] + lines_df['PAG']
    lines_df = lines_df[['Tm','Team', 'AvL']]
    lines_df["Margin"] = lines_df["AvL"]/lines_df["AvL"].mean()

    return lines_df

def get_minutes_data():
    """
    Returns minutes of the last 10 games per player. 
    Use this as expected minutes.
    """
    csv_path = Path("data/NBA_minutes.csv")
    minutes_df = pd.read_csv(csv_path)
    minutes_df = minutes_df.drop_duplicates(subset = ['Player'], keep='first')
    minutes_df = minutes_df[['Player', 'L10']]
    
    return minutes_df

def get_projection_data():
    """
    Function reads through the 3 databases and cleans through to return 
    Player, Team, Postion and Projected Points
    """

    df = get_fantasy_df()
    line_df = get_lines_data()
    minutes_df = get_minutes_data()

    #Finding the Position and Player avg. points per game.
    group_team = df.groupby(["Tm", "Pos"])["FPG"].max()
    group_team_df = group_team.unstack(level="Pos")

    #Filling the null values with mean
    group_team_df = group_team_df.fillna(group_team_df.mean())
    
    #Finding Covers projections
    OVP_df = group_team_df.copy()
    OVP_df = OVP_df/OVP_df.mean()
    
    #Merging the dataframes to match OVP with correct player
    clean = df.copy()
    clean = pd.merge(OVP_df, clean, on=["Tm"])
    clean["OVP"] = clean.lookup(clean.index, clean.Pos)

    #Matching Lines and minutes with correct team and player respectively
    clean = pd.merge(line_df, clean, on=["Tm"])

    clean = pd.merge(minutes_df, clean, on=["Player"])
    
    #Calculating projected points
    clean = clean[['Player', 'Tm', 'Pos', 'FPG', 'FPM', 'OVP', 'Margin', 'L10']]
    clean["Projected_Pts"] = clean.FPM * clean.OVP * clean.Margin * clean.L10 
    
    #Returning a clean database
    clean = clean[['Player', 'Tm', 'Pos', 'Projected_Pts']]
    clean = clean.round({'Projected_Pts': 2})
    
    return clean

def get_player_logs(player_name, season, logs):
    """
    Returns game playerlogs for the required players.
    Input requires player name, season start date and number of games (logs)
    Inspiration from @christilbey, @yfkok5, @XuYanRong and @dhaameen 
    """
    player_dict = players.get_players()
    player = pd.DataFrame(player_dict)
    player = [player for player in player_dict if player['full_name'] == player_name][0]
    player_id = player['id']
    player_gamelog = playergamelog.PlayerGameLog(player_id = player_id, season = season)
    df_games = player_gamelog.get_data_frames()
    player_df = df_games[0]
    player_df['FPG'] = 1* player_df['PTS'] + 0.5*player_df['FG3M'] + 1.25*player_df['REB'] + 1.5*player_df['AST'] + 2*player_df['STL'] + 2*player_df['BLK'] - 0.5*player_df['TOV']
    player_df['FPM'] = player_df['FPG']/player_df['MIN']
    fantasy_df = player_df[['GAME_DATE', 'MATCHUP', 'MIN', 'PTS', 'FG3M', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FPG', 'FPM']]
    
    return fantasy_df.head(logs)