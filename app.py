# app.py
# ========================================================================================
# COMPLETE STREAMLIT DASHBOARD + NGROK
# ========================================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
from pyngrok import ngrok
import threading
import subprocess
import time

warnings.filterwarnings('ignore')

# ----------------------------
# NGROK SETUP (Replace with your token)
# ----------------------------
NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN"  # <-- Replace this with your ngrok token
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Function to start ngrok tunnel
def start_ngrok():
    public_url = ngrok.connect(8501)
    print(f"🌐 Your Streamlit dashboard is live at: {public_url}")
    return public_url

# ----------------------------
# DASHBOARD CODE
# ----------------------------

# Helper functions for data cleaning
def clean_currency(value):
    if isinstance(value, str):
        return float(value.replace('$', '').replace(',', ''))
    return float(value)

def clean_percentage(value):
    if isinstance(value, str):
        return float(value.replace('%', ''))
    return float(value)

@st.cache_data
def load_sample_data():
    # B2C Social Media Performance Data
    social_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06'],
        'Spend (USD)': ['$125,441', '$126,198', '$120,458', '$125,973', '$125,412', '$120,042'],
        'Impressions': [12464777, 12975553, 12962575, 12401415, 13055242, 13234155],
        'Clicks to dolby.com landing': [90818, 101975, 102106, 101072, 107627, 114475],
        'Attributed sweeps signups on dolby.com': [4025, 4560, 4757, 4862, 5186, 5480]
    }
    
    website_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06'],
        'Website visits': [2450685, 2680483, 2920086, 3180870, 3460175, 3780668],
        'Uniques': [1680842, 1820119, 1980005, 2150509, 2340491, 2550671],
        'Average session duration (min)': [2.5, 2.6, 2.5, 2.8, 2.9, 2.6],
        'Demos completed': [42509, 42007, 46105, 48304, 60802, 63608],
        'Total sweeps signups': [10827, 11745, 12767, 13183, 13860, 14862]
    }
    
    events_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-05'],
        'Industry Event': ['CES', 'Mobile World Congress', 'SXSW', 'Game Asia'],
        'Event spend for Dolby Play': ['$750,000', '$250,000', '$250,000', '$650,000'],
        '# demos of Dolby Play conducted for mobile device partner contacts': [75, 55, 60, 60],
        '# new mobile device partner leads generated': [15, 5, 3, 5]
    }
    
    monitoring_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06'] * 3,
        'Platform': ['Instagram']*6 + ['LinkedIn']*6 + ['TikTok']*6,
        'Followers': [420068, 432010, 435100, 440089, 445035, 450047, 
                     95019, 96057, 96027, 97054, 97083, 97079,
                     80084, 83046, 85010, 87003, 93050, 96063],
        'Engagement rate': ['3.60%', '3.70%', '3.70%', '4.10%', '4.00%', '4.30%',
                           '2.20%', '1.90%', '1.80%', '1.80%', '1.90%', '2.00%',
                           '4.20%', '4.50%', '4.80%', '5.10%', '5.40%', '5.70%'],
        'Mentions': [5884, 6440, 6537, 6345, 6893, 6749,
                    1960, 1398, 1442, 1223, 1870, 1154,
                    3214, 3680, 4165, 4333, 4699, 4713],
        'Sentiment Score': [0.68, 0.71, 0.73, 0.72, 0.69, 0.72,
                           0.81, 0.76, 0.77, 0.75, 0.8, 0.77,
                           0.72, 0.74, 0.76, 0.78, 0.8, 0.82],
        'Share of Voice': ['15.70%', '16.80%', '16.30%', '15.60%', '17.30%', '17.40%',
                          '10.20%', '6.80%', '7.50%', '6.00%', '9.10%', '6.60%',
                          '8.90%', '9.80%', '10.90%', '12.10%', '13.50%', '15.00%']
    }
    
    brandpulse_data = {
        'Quarter': ['2024 Q4', '2025 Q1', '2025 Q2'] * 12,
        'Metric': ['Aided Awareness']*12 + ['Purchase Consideration']*12 + ['Unaided Awareness']*12,
        'Age Group': ['18-34', '18-34', '18-34', '35-54', '35-54', '35-54'] * 6,
        'Gender': ['Female', 'Female', 'Female', 'Female', 'Female', 'Female',
                   'Male', 'Male', 'Male', 'Male', 'Male', 'Male'] * 3,
        'Score': ['52.80%', '57.20%', '60.10%', '59.60%', '63.60%', '69.30%',
                 '67.20%', '67.40%', '68.10%', '72.40%', '71.30%', '73.10%',
                 '23.40%', '25.50%', '28.30%', '27.40%', '32.90%', '37.30%',
                 '34.80%', '34.30%', '37.00%', '36.00%', '39.20%', '41.10%',
                 '19.60%', '21.20%', '23.80%', '19.50%', '23.30%', '25.50%',
                 '23.20%', '24.50%', '24.90%', '28.40%', '29.30%', '29.20%'],
        'Comp. avg.': ['54.70%', '56.80%', '58.90%', '60.10%', '62.90%', '65.20%',
                      '58.30%', '60.10%', '62.10%', '63.20%', '65.40%', '67.80%',
                      '25.60%', '27.10%', '28.90%', '31.80%', '34.50%', '36.80%',
                      '28.90%', '30.20%', '32.10%', '35.20%', '37.80%', '40.20%',
                      '16.20%', '17.10%', '18.30%', '19.80%', '21.20%', '22.70%',
                      '18.50%', '19.20%', '20.10%', '22.10%', '23.50%', '24.80%']
    }
    
    return (pd.DataFrame(social_data), pd.DataFrame(website_data), pd.DataFrame(events_data),
            pd.DataFrame(monitoring_data), pd.DataFrame(brandpulse_data))

# ========================================================================================
# DATA PROCESSING FUNCTION
# ========================================================================================
def process_data(social_df, website_df, events_df, monitoring_df, brandpulse_df):
    social_df['Spend_Clean'] = social_df['Spend (USD)'].apply(clean_currency)
    social_df['CTR'] = (social_df['Clicks to dolby.com landing'] / social_df['Impressions']) * 100
    social_df['Click_to_Signup_Rate'] = (social_df['Attributed sweeps signups on dolby.com'] / social_df['Clicks to dolby.com landing']) * 100
    social_df['CPM'] = (social_df['Spend_Clean'] / social_df['Impressions']) * 1000
    social_df['CPC'] = social_df['Spend_Clean'] / social_df['Clicks to dolby.com landing']
    social_df['CPSignup'] = social_df['Spend_Clean'] / social_df['Attributed sweeps signups on dolby.com']
    
    website_df['Unique_to_Demo_Rate'] = (website_df['Demos completed'] / website_df['Uniques']) * 100
    website_df['Demo_to_Signup_Rate'] = (website_df['Total sweeps signups'] / website_df['Demos completed']) * 100
    
    events_df['Event_Spend_Clean'] = events_df['Event spend for Dolby Play'].apply(clean_currency)
    events_df['CPDemo'] = events_df['Event_Spend_Clean'] / events_df['# demos of Dolby Play conducted for mobile device partner contacts']
    events_df['CPL'] = events_df['Event_Spend_Clean'] / events_df['# new mobile device partner leads generated']
    events_df['Demo_to_Lead_Rate'] = (events_df['# new mobile device partner leads generated'] / events_df['# demos of Dolby Play conducted for mobile device partner contacts']) * 100
    
    monitoring_df['Engagement_Rate_Clean'] = monitoring_df['Engagement rate'].apply(clean_percentage)
    monitoring_df['Share_of_Voice_Clean'] = monitoring_df['Share of Voice'].apply(clean_percentage)
    
    brandpulse_df['Score_Clean'] = brandpulse_df['Score'].apply(clean_percentage)
    brandpulse_df['Comp_Avg_Clean'] = brandpulse_df['Comp. avg.'].apply(clean_percentage)
    
    return social_df, website_df, events_df, monitoring_df, brandpulse_df

# ========================================================================================
# STREAMLIT APP
# ========================================================================================
def main():
    # Page config
    st.set_page_config(page_title="Dolby Marketing Analytics Dashboard", page_icon="🎵", layout="wide")
    
    st.markdown('<h1 style="text-align:center;color:#1f77b4;">🎵 Dolby Marketing Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load and process data
    social_df, website_df, events_df, monitoring_df, brandpulse_df = load_sample_data()
    social_df, website_df, events_df, monitoring_df, brandpulse_df = process_data(
        social_df, website_df, events_df, monitoring_df, brandpulse_df
    )
    
    # Sidebar
    section = st.sidebar.selectbox(
        "Select Analysis Section:",
        ["🏠 Overview", "📱 Social Media Performance", "🌐 Website Engagement", 
         "🎯 B2B Events", "📊 Social Monitoring", "🎯 Brand Pulse Survey"]
    )
    
    st.write(f"### Selected Section: {section}")
    # ... Include all visualization code here (same as your original)
    st.info("Visualizations would go here (copy the Streamlit plotting code from your Colab version).")

if __name__ == "__main__":
    # Start ngrok tunnel in background
    threading.Thread(target=start_ngrok, daemon=True).start()
    
    # Run the Streamlit app
    main()
