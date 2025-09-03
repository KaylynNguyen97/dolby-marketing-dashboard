import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Dolby Marketing Analytics Dashboard",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions for data cleaning
def clean_currency(value):
    """Convert currency strings to numeric values"""
    if isinstance(value, str):
        return float(value.replace('$', '').replace(',', ''))
    return float(value)

def clean_percentage(value):
    """Convert percentage strings to numeric values"""
    if isinstance(value, str):
        return float(value.replace('%', ''))
    return float(value)

# Data loading function (using sample data)
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
    
    # B2C Website Engagement Data
    website_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06'],
        'Website visits': [2450685, 2680483, 2920086, 3180870, 3460175, 3780668],
        'Uniques': [1680842, 1820119, 1980005, 2150509, 2340491, 2550671],
        'Average session duration (min)': [2.5, 2.6, 2.5, 2.8, 2.9, 2.6],
        'Demos completed': [42509, 42007, 46105, 48304, 60802, 63608],
        'Total sweeps signups': [10827, 11745, 12767, 13183, 13860, 14862]
    }
    
    # B2B Industry Events Data
    events_data = {
        'Month': ['2025-01', '2025-02', '2025-03', '2025-05'],
        'Industry Event': ['CES', 'Mobile World Congress', 'SXSW', 'Game Asia'],
        'Event spend for Dolby Play': ['$750,000', '$250,000', '$250,000', '$650,000'],
        '# demos of Dolby Play conducted for mobile device partner contacts': [75, 55, 60, 60],
        '# new mobile device partner leads generated': [15, 5, 3, 5]
    }
    
    # Social Media Monitoring Data
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
    
    # Brand Pulse Survey Data
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
    
    # Convert to DataFrames
    social_df = pd.DataFrame(social_data)
    website_df = pd.DataFrame(website_data)
    events_df = pd.DataFrame(events_data)
    monitoring_df = pd.DataFrame(monitoring_data)
    brandpulse_df = pd.DataFrame(brandpulse_data)
    
    return social_df, website_df, events_df, monitoring_df, brandpulse_df

def process_data(social_df, website_df, events_df, monitoring_df, brandpulse_df):
    """Process and clean all datasets"""
    
    # Clean Social Media Data
    social_df['Spend_Clean'] = social_df['Spend (USD)'].apply(clean_currency)
    social_df['CTR'] = (social_df['Clicks to dolby.com landing'] / social_df['Impressions']) * 100
    social_df['Click_to_Signup_Rate'] = (social_df['Attributed sweeps signups on dolby.com'] / social_df['Clicks to dolby.com landing']) * 100
    social_df['CPM'] = (social_df['Spend_Clean'] / social_df['Impressions']) * 1000
    social_df['CPC'] = social_df['Spend_Clean'] / social_df['Clicks to dolby.com landing']
    social_df['CPSignup'] = social_df['Spend_Clean'] / social_df['Attributed sweeps signups on dolby.com']
    
    # Clean Website Data
    website_df['Unique_to_Demo_Rate'] = (website_df['Demos completed'] / website_df['Uniques']) * 100
    website_df['Demo_to_Signup_Rate'] = (website_df['Total sweeps signups'] / website_df['Demos completed']) * 100
    
    # Clean Events Data
    events_df['Event_Spend_Clean'] = events_df['Event spend for Dolby Play'].apply(clean_currency)
    events_df['CPDemo'] = events_df['Event_Spend_Clean'] / events_df['# demos of Dolby Play conducted for mobile device partner contacts']
    events_df['CPL'] = events_df['Event_Spend_Clean'] / events_df['# new mobile device partner leads generated']
    events_df['Demo_to_Lead_Rate'] = (events_df['# new mobile device partner leads generated'] / events_df['# demos of Dolby Play conducted for mobile device partner contacts']) * 100
    
    # Clean Monitoring Data
    monitoring_df['Engagement_Rate_Clean'] = monitoring_df['Engagement rate'].apply(clean_percentage)
    monitoring_df['Share_of_Voice_Clean'] = monitoring_df['Share of Voice'].apply(clean_percentage)
    
    # Clean Brand Pulse Data
    brandpulse_df['Score_Clean'] = brandpulse_df['Score'].apply(clean_percentage)
    brandpulse_df['Comp_Avg_Clean'] = brandpulse_df['Comp. avg.'].apply(clean_percentage)
    
    return social_df, website_df, events_df, monitoring_df, brandpulse_df

def main():
    # Title
    st.markdown('<h1 class="main-header">🎵 Dolby Marketing Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Load and process data
    social_df, website_df, events_df, monitoring_df, brandpulse_df = load_sample_data()
    social_df, website_df, events_df, monitoring_df, brandpulse_df = process_data(social_df, website_df, events_df, monitoring_df, brandpulse_df)
    
    # Sidebar
    st.sidebar.title("📊 Dashboard Controls")
    
    # Navigation
    section = st.sidebar.selectbox(
        "Select Analysis Section:",
        ["🏠 Overview", "📱 Social Media Performance", "🌐 Website Engagement", 
         "🎯 B2B Events", "📊 Social Monitoring", "🎯 Brand Pulse Survey"]
    )
    
    if section == "🏠 Overview":
        st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)
        
        # KPI Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_spend = social_df['Spend_Clean'].sum()
            st.metric("Total Social Spend", f"${total_spend:,.0f}")
            
        with col2:
            total_signups = social_df['Attributed sweeps signups on dolby.com'].sum()
            st.metric("Total Signups", f"{total_signups:,}")
            
        with col3:
            avg_ctr = social_df['CTR'].mean()
            st.metric("Average CTR", f"{avg_ctr:.2f}%")
            
        with col4:
            total_website_visits = website_df['Website visits'].sum()
            st.metric("Total Website Visits", f"{total_website_visits:,}")
        
        # Overview Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Social Media Spend Over Time
            fig = px.line(social_df, x='Month', y='Spend_Clean', 
                         title='Social Media Spend Over Time',
                         labels={'Spend_Clean': 'Spend ($)'})
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Website Traffic Growth
            fig = px.line(website_df, x='Month', y='Website visits',
                         title='Website Visits Growth',
                         labels={'Website visits': 'Visits'})
            fig.update_traces(line=dict(width=3))
            st.plotly_chart(fig, use_container_width=True)
    
    elif section == "📱 Social Media Performance":
        st.markdown('<div class="section-header">📱 B2C Social Media Performance</div>', unsafe_allow_html=True)
        
        # Metrics selection
        metric_type = st.selectbox(
            "Select Metric Type:",
            ["Engagement Metrics", "Cost Metrics", "Volume Metrics"]
        )
        
        if metric_type == "Engagement Metrics":
            col1, col2 = st.columns(2)
            
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['CTR'],
                                       mode='lines+markers', name='CTR (%)',
                                       line=dict(width=3)))
                fig.update_layout(title='Click-Through Rate Over Time',
                                xaxis_title='Month', yaxis_title='CTR (%)')
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['Click_to_Signup_Rate'],
                                       mode='lines+markers', name='Signup Rate (%)',
                                       line=dict(width=3, color='orange')))
                fig.update_layout(title='Click-to-Signup Rate Over Time',
                                xaxis_title='Month', yaxis_title='Signup Rate (%)')
                st.plotly_chart(fig, use_container_width=True)
        
        elif metric_type == "Cost Metrics":
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['CPM'],
                                   mode='lines+markers', name='CPM'))
            fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['CPC'],
                                   mode='lines+markers', name='CPC'))
            fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['CPSignup'],
                                   mode='lines+markers', name='Cost per Signup'))
            fig.update_layout(title='Cost Metrics Over Time',
                            xaxis_title='Month', yaxis_title='Cost ($)')
            st.plotly_chart(fig, use_container_width=True)
        
        else:  # Volume Metrics
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['Impressions']/1000000,
                                   mode='lines+markers', name='Impressions (M)'),
                         secondary_y=False)
            fig.add_trace(go.Scatter(x=social_df['Month'], y=social_df['Clicks to dolby.com landing']/1000,
                                   mode='lines+markers', name='Clicks (K)'),
                         secondary_y=True)
            fig.update_layout(title='Volume Metrics Over Time')
            fig.update_yaxes(title_text="Impressions (M)", secondary_y=False)
            fig.update_yaxes(title_text="Clicks (K)", secondary_y=True)
            st.plotly_chart(fig, use_container_width=True)
    
    elif section == "🌐 Website Engagement":
        st.markdown('<div class="section-header">🌐 B2C Website Engagement</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Website visits'],
                                   mode='lines+markers', name='Total Visits'))
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Uniques'],
                                   mode='lines+markers', name='Unique Visits'))
            fig.update_layout(title='Website Traffic Over Time',
                            xaxis_title='Month', yaxis_title='Visits')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Average session duration (min)'],
                                   mode='lines+markers', name='Avg Session Duration',
                                   line=dict(color='green', width=3)))
            fig.update_layout(title='Average Session Duration',
                            xaxis_title='Month', yaxis_title='Duration (min)')
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Demos completed'],
                                   mode='lines+markers', name='Demos Completed'))
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Total sweeps signups'],
                                   mode='lines+markers', name='Total Signups'))
            fig.update_layout(title='Demos vs Signups Over Time',
                            xaxis_title='Month', yaxis_title='Count')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Unique_to_Demo_Rate'],
                                   mode='lines+markers', name='Unique to Demo Rate'))
            fig.add_trace(go.Scatter(x=website_df['Month'], y=website_df['Demo_to_Signup_Rate'],
                                   mode='lines+markers', name='Demo to Signup Rate'))
            fig.update_layout(title='Conversion Rates Over Time',
                            xaxis_title='Month', yaxis_title='Rate (%)')
            st.plotly_chart(fig, use_container_width=True)
    
    elif section == "🎯 B2B Events":
        st.markdown('<div class="section-header">🎯 B2B Industry Events</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(events_df, x='Industry Event', y='Event_Spend_Clean',
                        title='Event Spend by Event',
                        labels={'Event_Spend_Clean': 'Spend ($)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=events_df['Industry Event'], 
                               y=events_df['# demos of Dolby Play conducted for mobile device partner contacts'],
                               name='Demos', offsetgroup=1))
            fig.add_trace(go.Bar(x=events_df['Industry Event'], 
                               y=events_df['# new mobile device partner leads generated'],
                               name='Leads', offsetgroup=2))
            fig.update_layout(title='Demos vs Leads by Event',
                            xaxis_title='Event', yaxis_title='Count')
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=events_df['Industry Event'], y=events_df['CPDemo'],
                               name='Cost per Demo'))
            fig.add_trace(go.Bar(x=events_df['Industry Event'], y=events_df['CPL'],
                               name='Cost per Lead'))
            fig.update_layout(title='Cost Efficiency by Event',
                            xaxis_title='Event', yaxis_title='Cost ($)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(events_df, x='Industry Event', y='Demo_to_Lead_Rate',
                        title='Demo to Lead Conversion Rate',
                        labels={'Demo_to_Lead_Rate': 'Conversion Rate (%)'})
            st.plotly_chart(fig, use_container_width=True)
    
    elif section == "📊 Social Monitoring":
        st.markdown('<div class="section-header">📊 Social Media Monitoring</div>', unsafe_allow_html=True)
        
        # Platform selection
        selected_platforms = st.multiselect(
            "Select Platforms:",
            options=monitoring_df['Platform'].unique(),
            default=monitoring_df['Platform'].unique()
        )
        
        filtered_monitoring = monitoring_df[monitoring_df['Platform'].isin(selected_platforms)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(filtered_monitoring, x='Month', y='Followers', 
                         color='Platform', title='Followers Growth by Platform')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(filtered_monitoring, x='Month', y='Engagement_Rate_Clean',
                         color='Platform', title='Engagement Rate by Platform',
                         labels={'Engagement_Rate_Clean': 'Engagement Rate (%)'})
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(filtered_monitoring, x='Month', y='Sentiment Score',
                         color='Platform', title='Sentiment Score by Platform')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(filtered_monitoring, x='Month', y='Share_of_Voice_Clean',
                         color='Platform', title='Share of Voice by Platform',
                         labels={'Share_of_Voice_Clean': 'Share of Voice (%)'})
            st.plotly_chart(fig, use_container_width=True)
    
    elif section == "🎯 Brand Pulse Survey":
        st.markdown('<div class="section-header">🎯 Brand Pulse Survey Analysis</div>', unsafe_allow_html=True)
        
        # Metric selection
        selected_metric = st.selectbox(
            "Select Metric:",
            options=brandpulse_df['Metric'].unique()
        )
        
        metric_data = brandpulse_df[brandpulse_df['Metric'] == selected_metric]
        
        # Create demographic segment identifier
        metric_data['Demographic'] = metric_data['Age Group'] + ' ' + metric_data['Gender']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(metric_data, x='Quarter', y='Score_Clean',
                         color='Demographic', title=f'{selected_metric} - Dolby Scores',
                         labels={'Score_Clean': 'Score (%)'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(metric_data, x='Quarter', y='Comp_Avg_Clean',
                         color='Demographic', title=f'{selected_metric} - Competitor Average',
                         labels={'Comp_Avg_Clean': 'Score (%)'})
            st.plotly_chart(fig, use_container_width=True)
        
        # Gap analysis
        metric_data['Gap'] = metric_data['Score_Clean'] - metric_data['Comp_Avg_Clean']
        
        fig = px.bar(metric_data, x='Quarter', y='Gap', color='Demographic',
                    title=f'{selected_metric} - Dolby vs Competitor Gap',
                    labels={'Gap': 'Gap (% points)'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("📊 **Dolby Marketing Analytics Dashboard** | Powered by Streamlit")

if __name__ == "__main__":
    main()
