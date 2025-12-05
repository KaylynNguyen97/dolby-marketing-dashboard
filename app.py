# app.py - FIXED VERSION USING PLOTLY
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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #374151;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #E5E7EB;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #F9FAFB;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">📊 DOLBY MARKETING PERFORMANCE DASHBOARD</h1>', unsafe_allow_html=True)

# Sidebar for navigation and filters
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Dolby_Laboratories_logo.svg/1280px-Dolby_Laboratories_logo.svg.png", 
             width=200)
    st.markdown("### 📈 Dashboard Navigation")
    
    dashboard_choice = st.selectbox(
        "Select Dashboard View",
        ["📊 Executive Summary", 
         "🎯 Market Position & Lead Gen", 
         "⭐ Product Experience",
         "🤝 Partner Value & Enablement",
         "💡 Innovation Leadership",
         "🎨 Creator Advocacy"]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Filters")
    
    # Date range filter
    date_range = st.selectbox(
        "Time Period",
        ["Last 12 Months", "Last 6 Months", "Last Quarter", "Year to Date", "All Time"]
    )
    
    # Market filter (if applicable)
    market_options = ["All Markets", "North America", "Europe", "Asia Pacific", "Latin America"]
    selected_market = st.selectbox("Market", market_options)
    
    st.markdown("---")
    st.markdown("### 📊 Data Status")
    st.info("Using simulated data for demonstration")
    
    if st.button("🔄 Refresh Data"):
        st.rerun()

# Helper function for data loading
@st.cache_data
def load_simulated_data():
    """Generate simulated data for demonstration"""
    
    # Generate dates
    dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='M')
    quarters = [f'Q{(i%4)+1} 202{3 if i<4 else 4}' for i in range(len(dates))]
    
    # Brand Health Index
    brand_health = pd.DataFrame({
        'Date': quarters[:8],
        'Composite_Brand_Health_Score': [78.2, 79.5, 81.3, 82.1, 83.4, 84.2, 85.0, 85.5]
    })
    
    # Digital Brand Presence
    markets = ['North America', 'Europe', 'Asia Pacific']
    digital_presence = pd.DataFrame({
        'Market': np.repeat(markets, 4),
        'Composite_Digital_Presence_Score': [85.3, 87.2, 82.4, 86.1, 83.2, 84.5, 81.3, 85.6, 79.4, 81.2, 78.5, 80.3]
    })
    
    # Marketing Qualified Leads
    mql_data = []
    sources = ['Organic Search', 'Paid Social', 'Email', 'Events']
    for i, date in enumerate(dates[:6]):
        for source in sources:
            base = 200 + i * 50
            total = base + np.random.randint(-20, 50)
            mql_count = int(total * (0.25 + i * 0.03))
            mql_data.append({
                'Date': date,
                'Lead_Source': source,
                'Total_Leads': total,
                'MQL_Count': mql_count,
                'Lead_Score_Average': 68 + i * 3 + np.random.randint(-5, 5),
                'Conversion_Rate': mql_count / total
            })
    mql_df = pd.DataFrame(mql_data)
    
    # Product NPS
    touchpoints = ['Website Demo', 'Product Tour', 'Trial Signup', 'First Login']
    product_nps_data = []
    for i, quarter in enumerate(quarters[:8]):
        for j, touchpoint in enumerate(touchpoints):
            product_nps_data.append({
                'Date': quarter,
                'Year_Quarter': quarter,
                'Touchpoint': touchpoint,
                'NPS_Score': 45 + i * 3 + j * 2,
                'Value_Communication_Score': 4.0 + i * 0.1 + j * 0.05,
                'Ease_Of_Understanding_Score': 4.2 + i * 0.08 + j * 0.03,
                'Brand_Clarity_Score': 4.1 + i * 0.09 + j * 0.04,
                'Entertainment_Value_Score': 4.3 + i * 0.07 + j * 0.06,
                'Promoters_Pct': 50 + i * 2 + j * 1,
                'Passives_Pct': 30 - i * 1,
                'Detractors_Pct': 20 - i * 1 - j * 0.5
            })
    product_nps_df = pd.DataFrame(product_nps_data)
    
    # Partner NPS
    regions = ['NA', 'EMEA', 'APAC']
    partner_types = ['Technology', 'Channel', 'Strategic']
    partner_nps_data = []
    for year in [2022, 2023]:
        for region in regions:
            for p_type in partner_types:
                partner_nps_data.append({
                    'Year': year,
                    'Region': region,
                    'Partner_Type': p_type,
                    'NPS_Score': 55 + (year-2022) * 5 + np.random.randint(-10, 10),
                    'Brand_Awareness_Score': 4.1 + (year-2022) * 0.2 + np.random.uniform(-0.1, 0.1),
                    'Innovation_Leadership_Score': 4.2 + (year-2022) * 0.3 + np.random.uniform(-0.1, 0.1)
                })
    partner_nps_df = pd.DataFrame(partner_nps_data)
    
    # Partner Mentions
    partners = ['Partner A', 'Partner B', 'Partner C', 'Partner D']
    partner_mentions_data = []
    for i, date in enumerate(dates[:6]):
        for partner in partners:
            partner_mentions_data.append({
                'Date': date,
                'Partner_Name': partner,
                'Mention_Count': 100 + i * 40 + np.random.randint(-20, 50),
                'Estimated_Reach': 500000 + i * 200000 + np.random.randint(-100000, 300000),
                'Co_Branded': np.random.choice(['Yes', 'No'], p=[0.6, 0.4])
            })
    partner_mentions_df = pd.DataFrame(partner_mentions_data)
    
    # Innovation Leadership
    categories = ['Audio Tech', 'Immersive Experience', 'Cinema Innovation', 'Gaming Tech']
    audiences = ['Consumers', 'Professionals', 'Developers', 'Partners']
    innovation_data = []
    for i, date in enumerate(dates[:6]):
        for j, category in enumerate(categories):
            for audience in audiences:
                innovation_data.append({
                    'Date': date,
                    'Innovation_Category': category,
                    'Audience': audience,
                    'Innovation_Leadership_Index': 70 + i * 3 + j * 2,
                    'Association_Share_Pct': 30 + i * 5 + j * 3,
                    'Positive_Sentiment_Pct': 70 + i * 2,
                    'Negative_Sentiment_Pct': 10 - i * 0.5,
                    'Neutral_Sentiment_Pct': 20 - i * 1.5,
                    'Category_Sentiment_Score': 4.0 + i * 0.1 + j * 0.05,
                    'Total_Mentions': 200 + i * 100 + j * 50
                })
    innovation_df = pd.DataFrame(innovation_data)
    
    # Creator NPS
    content_types = ['Video Tutorial', 'Case Study', 'Social Campaign', 'Event Content']
    cohorts = ['Cohort 1', 'Cohort 2', 'Cohort 3', 'Cohort 4']
    creator_nps_data = []
    for i, quarter in enumerate(quarters[:8]):
        for j, content_type in enumerate(content_types):
            creator_nps_data.append({
                'Date': quarter,
                'Quarter': quarter,
                'Content_Type': content_type,
                'Cohort': cohorts[j % 4],
                'NPS_Score': 52 + i * 2 + j * 1,
                'Program_Value_Score': 4.2 + i * 0.1 + j * 0.05,
                'Workflow_Efficiency_Score': 4.1 + i * 0.08 + j * 0.03,
                'Promoters_Pct': 55 + i * 2 + j * 1,
                'Passives_Pct': 30 - i * 1,
                'Detractors_Pct': 15 - i * 1 - j * 0.5,
                'Response_Count': 80 + i * 20 + j * 10
            })
    creator_nps_df = pd.DataFrame(creator_nps_data)
    
    return {
        'Brand_Health_Index': brand_health,
        'Digital_Brand_Presence': digital_presence,
        'Marketing_Qualified_Leads': mql_df,
        'Product_NPS': product_nps_df,
        'Partner_NPS': partner_nps_df,
        'Partner_Brand_Mentions': partner_mentions_df,
        'Creator_Lab_NPS': creator_nps_df,
        'Innovation_Leadership_Index': innovation_df
    }

# Load data
with st.spinner("Loading data..."):
    data = load_simulated_data()

# Extract dataframes
brand_health_df = data.get('Brand_Health_Index', pd.DataFrame())
digital_presence_df = data.get('Digital_Brand_Presence', pd.DataFrame())
mql_df = data.get('Marketing_Qualified_Leads', pd.DataFrame())
product_nps_df = data.get('Product_NPS', pd.DataFrame())
partner_nps_df = data.get('Partner_NPS', pd.DataFrame())
partner_mentions_df = data.get('Partner_Brand_Mentions', pd.DataFrame())
creator_nps_df = data.get('Creator_Lab_NPS', pd.DataFrame())
innovation_df = data.get('Innovation_Leadership_Index', pd.DataFrame())

# EXECUTIVE SUMMARY DASHBOARD
def show_executive_summary():
    st.markdown('<h2 class="sub-header">📈 Executive Summary</h2>', unsafe_allow_html=True)
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = brand_health_df['Composite_Brand_Health_Score'].mean()
        st.metric(
            label="Brand Health Index",
            value=f"{avg_score:.1f}",
            delta="+8.1% YoY"
        )
    
    with col2:
        total_mqls = mql_df['MQL_Count'].sum()
        st.metric(
            label="Total MQLs",
            value=f"{total_mqls:,.0f}",
            delta="+15% vs last period"
        )
    
    with col3:
        avg_nps = product_nps_df['NPS_Score'].mean()
        st.metric(
            label="Product NPS",
            value=f"{avg_nps:.0f}",
            delta="+12 points"
        )
    
    with col4:
        avg_innovation = innovation_df['Innovation_Leadership_Index'].mean()
        st.metric(
            label="Innovation Index",
            value=f"{avg_innovation:.1f}",
            delta="+7.2%"
        )
    
    # Second row of metrics
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        overall_rate = (mql_df['MQL_Count'].sum() / mql_df['Total_Leads'].sum() * 100)
        st.metric(
            label="MQL Conversion",
            value=f"{overall_rate:.1f}%",
            delta="+2.3%"
        )
    
    with col6:
        total_mentions = partner_mentions_df['Mention_Count'].sum()
        st.metric(
            label="Brand Mentions",
            value=f"{total_mentions:,.0f}",
            delta="+42%"
        )
    
    with col7:
        avg_partner_nps = partner_nps_df['NPS_Score'].mean()
        st.metric(
            label="Partner NPS",
            value=f"{avg_partner_nps:.0f}",
            delta="+9 points"
        )
    
    with col8:
        avg_creator_nps = creator_nps_df['NPS_Score'].mean()
        st.metric(
            label="Creator NPS",
            value=f"{avg_creator_nps:.0f}",
            delta="+11 points"
        )
    
    # Charts Row
    st.markdown('<h3 class="sub-header">Performance Trends</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Brand Health Trend")
        fig = px.line(brand_health_df, x='Date', y='Composite_Brand_Health_Score',
                     markers=True, line_shape='linear')
        fig.update_layout(
            xaxis_title='Quarter',
            yaxis_title='Composite Score',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("MQL Conversion Trend")
        conversion_trend = mql_df.groupby('Date')['Conversion_Rate'].mean().reset_index()
        fig = px.line(conversion_trend, x='Date', y='Conversion_Rate',
                     markers=True, line_shape='linear')
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Conversion Rate (%)',
            yaxis_tickformat='.1%',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

# MARKET POSITION DASHBOARD
def show_market_position_dashboard():
    st.markdown('<h2 class="sub-header">🎯 Market Position & Lead Generation</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Performance", "🎯 Lead Quality"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Brand Health Index Trend")
            fig = px.line(brand_health_df, x='Date', y='Composite_Brand_Health_Score',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Quarter',
                yaxis_title='Composite Score',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Lead Score Trend")
            lead_score_trend = mql_df.groupby('Date')['Lead_Score_Average'].mean().reset_index()
            fig = px.line(lead_score_trend, x='Date', y='Lead_Score_Average',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Average Lead Score',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Digital Brand Presence by Market")
            digital_presence_summary = digital_presence_df.groupby('Market')['Composite_Digital_Presence_Score'].mean().reset_index()
            fig = px.bar(digital_presence_summary, x='Market', y='Composite_Digital_Presence_Score',
                        color='Market', text_auto='.1f')
            fig.update_layout(
                yaxis_title='Composite Score',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("MQL Volume by Month")
            mql_volume = mql_df.groupby('Date').agg({
                'Total_Leads': 'sum',
                'MQL_Count': 'sum'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=mql_volume['Date'],
                y=mql_volume['Total_Leads'],
                name='Total Leads',
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                x=mql_volume['Date'],
                y=mql_volume['MQL_Count'],
                name='MQLs',
                marker_color='orange'
            ))
            fig.update_layout(
                barmode='group',
                xaxis_title='Month',
                yaxis_title='Count',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("MQL Performance by Lead Source")
        mql_summary = mql_df.groupby('Lead_Source').agg({
            'Total_Leads': 'sum',
            'MQL_Count': 'sum'
        }).reset_index()
        mql_summary['Conversion_Rate'] = (mql_summary['MQL_Count'] / mql_summary['Total_Leads']) * 100
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add bars for counts
        fig.add_trace(
            go.Bar(x=mql_summary['Lead_Source'], y=mql_summary['Total_Leads'],
                  name='Total Leads', marker_color='lightblue'),
            secondary_y=False
        )
        fig.add_trace(
            go.Bar(x=mql_summary['Lead_Source'], y=mql_summary['MQL_Count'],
                  name='MQLs', marker_color='orange'),
            secondary_y=False
        )
        
        # Add line for conversion rate
        fig.add_trace(
            go.Scatter(x=mql_summary['Lead_Source'], y=mql_summary['Conversion_Rate'],
                      name='Conversion Rate', mode='lines+markers',
                      line=dict(color='red', width=2)),
            secondary_y=True
        )
        
        fig.update_layout(
            xaxis_title='Lead Source',
            title='MQL Performance by Lead Source',
            barmode='group',
            height=500
        )
        fig.update_yaxes(title_text="Count", secondary_y=False)
        fig.update_yaxes(title_text="Conversion Rate (%)", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)

# PRODUCT EXPERIENCE DASHBOARD
def show_product_experience_dashboard():
    st.markdown('<h2 class="sub-header">⭐ Product Experience - "First Meet" NPS</h2>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📈 NPS Trends", "🎯 Experience Metrics"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("NPS Score Trend by Touchpoint")
            nps_by_touchpoint = product_nps_df.pivot_table(
                index='Year_Quarter', 
                columns='Touchpoint', 
                values='NPS_Score',
                aggfunc='mean'
            ).reset_index()
            
            # Sort chronologically
            quarter_order = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 
                           'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
            nps_by_touchpoint['Year_Quarter'] = pd.Categorical(nps_by_touchpoint['Year_Quarter'], 
                                                              categories=quarter_order, ordered=True)
            nps_by_touchpoint = nps_by_touchpoint.sort_values('Year_Quarter')
            
            fig = go.Figure()
            touchpoints = [col for col in nps_by_touchpoint.columns if col != 'Year_Quarter']
            for touchpoint in touchpoints:
                fig.add_trace(go.Scatter(
                    x=nps_by_touchpoint['Year_Quarter'],
                    y=nps_by_touchpoint[touchpoint],
                    mode='lines+markers',
                    name=touchpoint
                ))
            
            fig.update_layout(
                xaxis_title='Quarter',
                yaxis_title='NPS Score',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("NPS Distribution")
            categories = ['Promoters_Pct', 'Passives_Pct', 'Detractors_Pct']
            
            latest_quarter = product_nps_df['Year_Quarter'].max()
            latest_data = product_nps_df[product_nps_df['Year_Quarter'] == latest_quarter]
            avg_distribution = latest_data[categories].mean().values
            
            fig = px.pie(
                values=avg_distribution,
                names=['Promoters', 'Passives', 'Detractors'],
                color=['Promoters', 'Passives', 'Detractors'],
                color_discrete_map={'Promoters': '#2ecc71', 'Passives': '#f39c12', 'Detractors': '#e74c3c'},
                title=f'NPS Distribution ({latest_quarter})'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Experience Metrics")
        
        latest_quarter = product_nps_df['Year_Quarter'].max()
        latest_data = product_nps_df[product_nps_df['Year_Quarter'] == latest_quarter]
        
        experience_metrics = ['Value_Communication_Score', 'Ease_Of_Understanding_Score', 
                             'Brand_Clarity_Score', 'Entertainment_Value_Score']
        
        experience_scores = latest_data[experience_metrics].mean().reset_index()
        experience_scores.columns = ['Metric', 'Average_Score']
        experience_scores['Metric'] = experience_scores['Metric'].str.replace('_Score', '').str.replace('_', ' ')
        
        # Display as a bar chart
        fig = px.bar(experience_scores, x='Metric', y='Average_Score',
                     text_auto='.2f', color='Metric')
        fig.update_layout(
            yaxis_title='Average Score (1-5)',
            yaxis_range=[3.5, 5],
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Also show as a dataframe
        st.dataframe(experience_scores, use_container_width=True)

# PARTNER DASHBOARD
def show_partner_dashboard():
    st.markdown('<h2 class="sub-header">🤝 Partner Value & Enablement</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 NPS Analysis", "📣 Brand Mentions", "🌐 Regional View"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Partner NPS Trend")
            nps_trend = partner_nps_df.groupby('Year')['NPS_Score'].mean().reset_index()
            fig = px.line(nps_trend, x='Year', y='NPS_Score',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Average NPS Score',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Brand Perception by Partner Type")
            avg_scores = partner_nps_df.groupby('Partner_Type').agg({
                'Brand_Awareness_Score': 'mean',
                'Innovation_Leadership_Score': 'mean'
            }).reset_index()
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=avg_scores['Partner_Type'],
                y=avg_scores['Brand_Awareness_Score'],
                name='Brand Awareness',
                marker_color='lightblue'
            ))
            fig.add_trace(go.Bar(
                x=avg_scores['Partner_Type'],
                y=avg_scores['Innovation_Leadership_Score'],
                name='Innovation Leadership',
                marker_color='orange'
            ))
            fig.update_layout(
                barmode='group',
                xaxis_title='Partner Type',
                yaxis_title='Average Score',
                yaxis_range=[3.5, 5],
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Partner Brand Mentions Trend")
            mentions_trend = partner_mentions_df.groupby('Date').agg({
                'Mention_Count': 'sum',
                'Estimated_Reach': 'sum'
            }).reset_index()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                go.Scatter(x=mentions_trend['Date'], y=mentions_trend['Mention_Count'],
                          mode='lines+markers', name='Mention Count',
                          line=dict(color='#2ecc71', width=2)),
                secondary_y=False
            )
            fig.add_trace(
                go.Scatter(x=mentions_trend['Date'], y=mentions_trend['Estimated_Reach']/1000000,
                          mode='lines+markers', name='Estimated Reach (M)',
                          line=dict(color='#e74c3c', width=2)),
                secondary_y=True
            )
            
            fig.update_layout(
                xaxis_title='Month',
                title='Partner Brand Mentions Trend',
                height=400
            )
            fig.update_yaxes(title_text="Mention Count", secondary_y=False)
            fig.update_yaxes(title_text="Estimated Reach (Millions)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Brand Mentions by Partner")
            mentions_by_partner = partner_mentions_df.groupby('Partner_Name')['Mention_Count'].sum().reset_index()
            mentions_by_partner = mentions_by_partner.sort_values('Mention_Count', ascending=True)
            
            fig = px.bar(mentions_by_partner, x='Mention_Count', y='Partner_Name',
                        orientation='h', text_auto=True, color='Mention_Count',
                        color_continuous_scale='viridis')
            fig.update_layout(
                xaxis_title='Total Mention Count',
                yaxis_title='Partner Name',
                height=400,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Partner NPS Score Heatmap")
        partner_nps_pivot = partner_nps_df.pivot_table(
            index='Region',
            columns='Partner_Type',
            values='NPS_Score',
            aggfunc='mean'
        )
        
        fig = px.imshow(partner_nps_pivot,
                       text_auto='.1f',
                       color_continuous_scale='YlOrRd',
                       title='Partner NPS Score Heatmap')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# INNOVATION DASHBOARD
def show_innovation_dashboard():
    st.markdown('<h2 class="sub-header">💡 Innovation Leadership</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Index Trends", "🧭 Category Analysis", "🎯 Sentiment Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Innovation Leadership Index Trend")
            innovation_trend = innovation_df.groupby('Date')['Innovation_Leadership_Index'].mean().reset_index()
            
            fig = px.line(innovation_trend, x='Date', y='Innovation_Leadership_Index',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Innovation Leadership Index',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Total Innovation Mentions Trend")
            mentions_trend = innovation_df.groupby('Date')['Total_Mentions'].sum().reset_index()
            
            fig = px.line(mentions_trend, x='Date', y='Total_Mentions',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Total Mentions',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Innovation Category Performance")
        
        latest_date = innovation_df['Date'].max()
        latest_innovation = innovation_df[innovation_df['Date'] == latest_date]
        
        category_performance = latest_innovation.groupby('Innovation_Category').agg({
            'Innovation_Leadership_Index': 'mean',
            'Association_Share_Pct': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=category_performance['Innovation_Category'],
            y=category_performance['Innovation_Leadership_Index'],
            name='Leadership Index',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=category_performance['Innovation_Category'],
            y=category_performance['Association_Share_Pct'],
            name='Association Share %',
            marker_color='orange'
        ))
        
        fig.update_layout(
            barmode='group',
            xaxis_title='Innovation Category',
            yaxis_title='Score / Percentage',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Sentiment Analysis")
        
        sentiment_cols = ['Positive_Sentiment_Pct', 'Negative_Sentiment_Pct', 'Neutral_Sentiment_Pct']
        latest_date = innovation_df['Date'].max()
        latest_innovation = innovation_df[innovation_df['Date'] == latest_date]
        
        sentiment_by_category = latest_innovation.groupby('Innovation_Category')[sentiment_cols].mean().reset_index()
        
        fig = go.Figure()
        colors = ['#2ecc71', '#e74c3c', '#f39c12']
        for i, col in enumerate(sentiment_cols):
            fig.add_trace(go.Bar(
                x=sentiment_by_category['Innovation_Category'],
                y=sentiment_by_category[col],
                name=col.replace('_Sentiment_Pct', ''),
                marker_color=colors[i]
            ))
        
        fig.update_layout(
            barmode='stack',
            xaxis_title='Innovation Category',
            yaxis_title='Sentiment Percentage',
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# CREATOR DASHBOARD
def show_creator_dashboard():
    st.markdown('<h2 class="sub-header">🎨 Creator Advocacy</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 NPS Analysis", "📈 Program Performance", "👥 Cohort Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Average NPS by Content Type")
            nps_by_content = creator_nps_df.groupby('Content_Type')['NPS_Score'].mean().reset_index()
            nps_by_content = nps_by_content.sort_values('NPS_Score', ascending=False)
            
            fig = px.bar(nps_by_content, x='Content_Type', y='NPS_Score',
                        text_auto='.1f', color='Content_Type')
            fig.update_layout(
                xaxis_title='Content Type',
                yaxis_title='Average NPS Score',
                yaxis_range=[0, 60],
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Creator NPS Trend")
            creator_nps_df['Quarter'] = creator_nps_df['Date']
            nps_trend = creator_nps_df.groupby('Quarter')['NPS_Score'].mean().reset_index()
            
            # Sort chronologically
            quarter_order = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023', 
                           'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
            nps_trend['Quarter'] = pd.Categorical(nps_trend['Quarter'], categories=quarter_order, ordered=True)
            nps_trend = nps_trend.sort_values('Quarter')
            
            fig = px.line(nps_trend, x='Quarter', y='NPS_Score',
                         markers=True, line_shape='linear')
            fig.update_layout(
                xaxis_title='Quarter',
                yaxis_title='Average NPS Score',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Program Evaluation by Content Type")
        
        avg_scores = creator_nps_df.groupby('Content_Type').agg({
            'Program_Value_Score': 'mean',
            'Workflow_Efficiency_Score': 'mean'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=avg_scores['Content_Type'],
            y=avg_scores['Program_Value_Score'],
            name='Program Value',
            marker_color='lightblue'
        ))
        fig.add_trace(go.Bar(
            x=avg_scores['Content_Type'],
            y=avg_scores['Workflow_Efficiency_Score'],
            name='Workflow Efficiency',
            marker_color='orange'
        ))
        
        fig.update_layout(
            barmode='group',
            xaxis_title='Content Type',
            yaxis_title='Average Score',
            yaxis_range=[3.5, 5],
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("NPS Score by Cohort")
            cohort_performance = creator_nps_df.groupby('Cohort')['NPS_Score'].mean().reset_index()
            cohort_order = ['Cohort 1', 'Cohort 2', 'Cohort 3', 'Cohort 4']
            cohort_performance['Cohort'] = pd.Categorical(cohort_performance['Cohort'], 
                                                        categories=cohort_order, ordered=True)
            cohort_performance = cohort_performance.sort_values('Cohort')
            
            fig = px.bar(cohort_performance, x='Cohort', y='NPS_Score',
                        text_auto='.1f', color='Cohort')
            fig.update_layout(
                yaxis_title='Average NPS Score',
                yaxis_range=[0, 60],
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Total Survey Responses by Content Type")
            response_by_type = creator_nps_df.groupby('Content_Type')['Response_Count'].sum().reset_index()
            response_by_type = response_by_type.sort_values('Response_Count', ascending=True)
            
            fig = px.bar(response_by_type, x='Response_Count', y='Content_Type',
                        orientation='h', text_auto=True, color='Response_Count',
                        color_continuous_scale='coolwarm')
            fig.update_layout(
                xaxis_title='Total Response Count',
                yaxis_title='Content Type',
                height=400,
                coloraxis_showscale=False
            )
            st.plotly_chart(fig, use_container_width=True)

# Main app routing
if dashboard_choice == "📊 Executive Summary":
    show_executive_summary()
elif dashboard_choice == "🎯 Market Position & Lead Gen":
    show_market_position_dashboard()
elif dashboard_choice == "⭐ Product Experience":
    show_product_experience_dashboard()
elif dashboard_choice == "🤝 Partner Value & Enablement":
    show_partner_dashboard()
elif dashboard_choice == "💡 Innovation Leadership":
    show_innovation_dashboard()
elif dashboard_choice == "🎨 Creator Advocacy":
    show_creator_dashboard()

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    st.caption("© 2024 Dolby Marketing Analytics Dashboard | Data refreshes hourly")
