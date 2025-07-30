import base64
import streamlit as st
import pickle
import pandas as pd

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load background image
img = get_img_as_base64("background.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:image/png;base64,{img}");
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    color: #AAFF00; /* Light text color */
}}

[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{img}");
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
    color: #AAFF00; /* Light text color */
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

.stButton > button {{
    background-color: #4caf50; /* Button color */
    color: white; /* Button text color */
    border: none;
    border-radius: 10px; /* Rounded button */
    padding: 15px 25px; /* Increased padding */
    font-size: 18px; /* Increased font size */
    transition: background-color 0.3s ease, transform 0.2s ease;
}}

.stButton > button:hover {{
    background-color: #45a049; /* Lighter button color on hover */
    transform: scale(1.05); /* Slightly increase size on hover */
}}

.stMarkdown {{
    font-size: 28px; /* Increased font size for headers */
    color: #AAFF00; /* Ensure headers are visible */
    font-weight: bold;
}}

input[type="text"], input[type="number"], select {{
    border: 2px solid #4caf50; /* Input border color */
    border-radius: 5px; /* Rounded input fields */
    padding: 12px; /* Increased padding */
    font-size: 18px; /* Increased font size */
    color: #ffffff; /* Light text color */
    background-color: rgba(0, 0, 0, 0.7); /* Dark input background */
}}

input[type="text"]:focus, input[type="number"]:focus, select:focus {{
    border-color: #45a049; /* Border color on focus */
    outline: none; /* Remove default outline */
}}

.table {{
    border-collapse: collapse;
    width: 100%; /* Full width */
    margin-top: 20px; /* Margin for spacing */
}}

.table th, .table td {{
    border: 1px solid #4caf50; /* Table border color */
    text-align: left;
    padding: 10px;
    color: #ffffff; /* Light text color */
}}

.table th {{
    background-color: rgba(76, 175, 80, 0.8); /* Table header background color */
    font-weight: bold; /* Bold text for header */
}}

.table tr:nth-child(even) {{
    background-color: rgba(255, 255, 255, 0.1); /* Light background for even rows */
}}

.table tr:hover {{
    background-color: rgba(76, 175, 80, 0.3); /* Highlight row on hover */
}}

.input-container {{
    display: flex;
    flex-direction: column;
    align-items: center; /* Center align items */
    margin: 10px 0; /* Margin for spacing */
}}

.input-title {{
    font-size: 22px; /* Title font size */
    color: #AAFF00; /* Title color */
    margin-bottom: 5px; /* Space between title and input */
}}

/* Additional Table Styles */
.stTable {{
    color: #ffffff;  /* Text color for the entire table */
}}

/* Style for table headers */
.stTable th {{
    color: #ffffff;  /* White text color for header */
    border: 2px solid #ffffff; /* White border for table headers */
}}

/* Style for table cells */
.stTable td {{
    color: #ffffff;  /* White text color for table cells */
    border: 2px solid #ffffff; /* White border for table cells */
    padding: 10px;  /* Padding for table cells */
}}
</style>

"""




cities = ['Mumbai', 'Delhi', 'Chennai', 'Abu Dhabi', 'Visakhapatnam', 'Hyderabad', 'Chandigarh', 
          'Ahmedabad', 'Bangalore', 'Jaipur', 'Kolkata', 'Port Elizabeth', 'Cuttack', 'Navi Mumbai', 
          'Centurion', 'Bengaluru', 'Pune', 'Johannesburg', 'Dubai', 'Cape Town', 'Lucknow', 'Durban', 
          'Dharamsala', 'Indore', 'East London', 'Sharjah', 'Guwahati', 'Raipur', 'Ranchi', 'Nagpur', 
          'Kimberley', 'Bloemfontein']

teams = ['Kolkata Knight Riders', 'Chennai Super Kings', 'Punjab Kings', 'Rajasthan Royals', 'Mumbai Indians', 
         'Delhi Capitals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad', 'Lucknow Super Giants', 
         'Gujarat Titans']


match_stats_df = pd.read_csv('matches.csv')

# Load model
pipe = pickle.load(open('pipe.pkl', 'rb'))
pipe_player_of_match = pickle.load(open('pipe_player_of_match.pkl', 'rb'))

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<h1 style='color: #AAFF00;'>IPL VICTORY PREDICTOR</h1>", unsafe_allow_html=True)

# Select batting team
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h2 style='color: #AAFF00;'>Select Batting Team</h2>", unsafe_allow_html=True)
    batting_team = st.selectbox('', teams)

# Select bowling team
with col2:
    st.markdown("<h2 style='color: #AAFF00;'>Select Bowling Team</h2>", unsafe_allow_html=True)
    if batting_team == '--- select ---':
        bowling_team = st.selectbox('', teams)
    else:
        filtered_teams = [team for team in teams if team != batting_team]
        bowling_team = st.selectbox('', filtered_teams)

# Select venue
st.markdown("<h2 style='color: #AAFF00;'>Select Venue</h2>", unsafe_allow_html=True)
selected_city = st.selectbox('', cities)

# Target input 
st.markdown("<h2 style='color: #AAFF00;'>Target</h2>", unsafe_allow_html=True)
target = st.number_input('', key='target_input', step=1, format="%d")  

# Score, Overs, and Wickets input
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='input-container'><div class='input-title'>Score</div>", unsafe_allow_html=True)
    score = st.number_input('', key='score_input', step=1, format="%d")  
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='input-container'><div class='input-title'>Overs Completed</div>", unsafe_allow_html=True)
    overs = st.number_input("", key='overs_input', step=1, format="%d")  
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<div class='input-container'><div class='input-title'>Wickets Down</div>", unsafe_allow_html=True)
    wickets = st.number_input("", key='wickets_input', step=1, format="%d")  
    st.markdown("</div>", unsafe_allow_html=True)


if st.button('Predict Winning Probability'):
    try:
        runs_left = target - score
        balls_left = 120 - (overs * 6)
        wickets_remaining = 10 - wickets
        crr = score / overs if overs > 0 else 0 
        rrr = runs_left / (balls_left / 6) if balls_left > 0 else 0 
        input_data = pd.DataFrame({
            'batting_team': [batting_team],
            'bowling_team': [bowling_team],
            'city': [selected_city],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets_remaining': [wickets_remaining],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

 # Displaying historical match statistics
       

        # Filter matches based on selected teams
        filtered_matches = match_stats_df[
            ((match_stats_df['team1'] == batting_team) & (match_stats_df['team2'] == bowling_team)) |
            ((match_stats_df['team1'] == bowling_team) & (match_stats_df['team2'] == batting_team))
        ]

        # Count wins for each team and draws/no result
        batting_team_wins = filtered_matches[filtered_matches['winner'] == batting_team].shape[0]
        bowling_team_wins = filtered_matches[filtered_matches['winner'] == bowling_team].shape[0]
        draws = filtered_matches[filtered_matches['result'] == 'no result'].shape[0] + filtered_matches[filtered_matches['result'] == 'No Result'].shape[0]
        total_matches = filtered_matches.shape[0]

        # Display statistics
        st.markdown("<h2 style='color: #AAFF00;'>Match Statistics:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #AAFF00;'>Total Matches Played: {total_matches}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #AAFF00;'>{batting_team} Wins: {batting_team_wins}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #AAFF00;'>{bowling_team} Wins: {bowling_team_wins}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #AAFF00;'>Draws/No Result: {draws}</h3>", unsafe_allow_html=True)
        # Debugging: Print the input data
        st.write("Input Data for Prediction:")
        st.write(input_data.style.set_table_attributes('class="table"'))  

        # Predicting match winner
        result = pipe.predict_proba(input_data)

        loss = result[0][0]  # Probability of loss
        win = result[0][1]   # Probability of win

        st.markdown(f"<h2 style='color: #AAFF00;'>Winning Probability:</h2>", unsafe_allow_html=True)

        # Batting team progress
        st.markdown(f"<h3 style='color: #AAFF00;'>{batting_team} = {round(win * 100)}%</h3>", unsafe_allow_html=True)
        batting_team_progress = st.progress(win)  # Progress based on win probability

        # Bowling team progress
        st.markdown(f"<h3 style='color: #AAFF00;'>{bowling_team} = {round(loss * 100)}%</h3>", unsafe_allow_html=True)
        bowling_team_progress = st.progress(loss)  # Progress based on loss probability

        # Predicting player of the
        # Predicting player of the match
        player_of_match_data = pipe_player_of_match.predict(input_data)
        player_of_match = player_of_match_data[0]

       

        if not filtered_matches.empty:
                                      filtered_matches.reset_index(drop=True, inplace=True)  # Reset index to get a clean DataFrame
                                      filtered_matches['Serial No'] = range(1, len(filtered_matches) + 1)  # Create a new column for serial numbers
                                      filtered_matches = filtered_matches[['Serial No', 'season', 'date', 'winner']]
                                      st.markdown(f"<h2 class='matches-heading' style='color: #AAFF00;'>Matches played between {batting_team} and {bowling_team}</h2>", unsafe_allow_html=True)
                                      st.table(filtered_matches)  
        else:
                                      st.markdown(f"<p class='no-matches' style='color: #AAFF00;' >No matches found between {batting_team} and {bowling_team}</p>", unsafe_allow_html=True)

    except Exception as e:
                        st.error(f"Error occurred during prediction: {e}")

