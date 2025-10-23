"""
Personalized Symptom Timeline - Track and visualize symptom progression
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random


def render_symptom_timeline():
    """Render personalized symptom timeline page."""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)

    # Page header
    st.markdown(
        """
    <div class="main-header">
        <h1>📈 Your Symptom Timeline</h1>
        <p style="color: var(--medium-gray);">Track your journey and see patterns in your symptoms</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize timeline data
    if "symptom_timeline" not in st.session_state:
        st.session_state.symptom_timeline = generate_sample_timeline_data()

    # Main sections
    col1, col2 = st.columns([3, 1])

    with col1:
        render_timeline_charts()
        render_symptom_patterns()

    with col2:
        render_timeline_controls()
        render_insights_panel()


def render_timeline_charts():
    """Render interactive timeline charts."""
    st.markdown("### 📊 Symptom Severity Over Time")
    
    # Get timeline data
    df = pd.DataFrame(st.session_state.symptom_timeline)
    df['date'] = pd.to_datetime(df['date'])
    
    # Create multi-line chart for all symptoms
    fig = go.Figure()
    
    symptoms = ['hot_flashes', 'night_sweats', 'mood_changes', 'sleep_quality', 'cognitive_issues', 'energy_level']
    colors = ['#E53935', '#FF7043', '#FFB300', '#26A69A', '#9C27B0', '#2196F3']
    
    for i, symptom in enumerate(symptoms):
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[symptom],
            mode='lines+markers',
            name=symptom.replace('_', ' ').title(),
            line=dict(color=colors[i], width=3),
            marker=dict(size=6),
            hovertemplate=f"<b>{symptom.replace('_', ' ').title()}</b><br>" +
                         "Date: %{x}<br>" +
                         "Severity: %{y}/10<extra></extra>"
        ))
    
    fig.update_layout(
        title="Your Symptom Journey",
        xaxis_title="Date",
        yaxis_title="Severity (0-10)",
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        font={'color': "#424242"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Individual symptom charts
    render_individual_symptom_charts(df)


def render_individual_symptom_charts(df):
    """Render individual symptom charts."""
    st.markdown("### 🔍 Individual Symptom Analysis")
    
    symptoms = ['hot_flashes', 'night_sweats', 'mood_changes', 'sleep_quality', 'cognitive_issues', 'energy_level']
    
    # Create tabs for each symptom
    tabs = st.tabs([symptom.replace('_', ' ').title() for symptom in symptoms])
    
    for i, (tab, symptom) in enumerate(zip(tabs, symptoms)):
        with tab:
            # Create individual chart
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[symptom],
                mode='lines+markers',
                name=symptom.replace('_', ' ').title(),
                line=dict(color=['#E53935', '#FF7043', '#FFB300', '#26A69A', '#9C27B0', '#2196F3'][i], width=4),
                marker=dict(size=8),
                fill='tonexty' if i > 0 else 'tozeroy',
                fillcolor='rgba(0,100,80,0.1)'
            ))
            
            # Add trend line
            z = np.polyfit(range(len(df)), df[symptom], 1)
            p = np.poly1d(z)
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=p(range(len(df))),
                mode='lines',
                name='Trend',
                line=dict(color='rgba(0,0,0,0.3)', dash='dash')
            ))
            
            fig.update_layout(
                title=f"{symptom.replace('_', ' ').title()} Over Time",
                xaxis_title="Date",
                yaxis_title="Severity (0-10)",
                height=300,
                font={'color': "#424242"},
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show statistics
            render_symptom_statistics(df, symptom)


def render_symptom_statistics(df, symptom):
    """Render statistics for a specific symptom."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_severity = df[symptom].mean()
        st.metric("Average", f"{avg_severity:.1f}/10")
    
    with col2:
        max_severity = df[symptom].max()
        st.metric("Peak", f"{max_severity:.1f}/10")
    
    with col3:
        min_severity = df[symptom].min()
        st.metric("Lowest", f"{min_severity:.1f}/10")
    
    with col4:
        # Calculate trend
        recent_avg = df.tail(7)[symptom].mean()
        older_avg = df.head(7)[symptom].mean()
        trend = "↗️ Improving" if recent_avg < older_avg else "↘️ Worsening"
        st.metric("Trend", trend)


def render_symptom_patterns():
    """Render symptom pattern analysis."""
    st.markdown("### 🔍 Pattern Recognition")
    
    df = pd.DataFrame(st.session_state.symptom_timeline)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week patterns
        st.markdown("#### 📅 Day of Week Patterns")
        day_patterns = df.groupby('day_of_week')['hot_flashes'].mean().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        fig = px.bar(
            x=day_patterns.index,
            y=day_patterns.values,
            title="Average Hot Flashes by Day",
            color=day_patterns.values,
            color_continuous_scale="Reds"
        )
        fig.update_layout(
            height=300,
            font={'color': "#424242"},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Symptom correlations
        st.markdown("#### 🔗 Symptom Correlations")
        symptoms = ['hot_flashes', 'night_sweats', 'mood_changes', 'sleep_quality', 'cognitive_issues', 'energy_level']
        corr_matrix = df[symptoms].corr()
        
        fig = px.imshow(
            corr_matrix,
            title="Symptom Correlation Matrix",
            color_continuous_scale="RdBu",
            aspect="auto"
        )
        fig.update_layout(
            height=300,
            font={'color': "#424242"},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)


def render_timeline_controls():
    """Render timeline control panel."""
    st.markdown("### 🎛️ Timeline Controls")
    
    # Date range selector
    df = pd.DataFrame(st.session_state.symptom_timeline)
    df['date'] = pd.to_datetime(df['date'])
    
    min_date = df['date'].min()
    max_date = df['date'].max()
    
    date_range = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Symptom filter
    symptoms = ['hot_flashes', 'night_sweats', 'mood_changes', 'sleep_quality', 'cognitive_issues', 'energy_level']
    selected_symptoms = st.multiselect(
        "Select Symptoms to Display",
        options=symptoms,
        default=symptoms,
        format_func=lambda x: x.replace('_', ' ').title()
    )
    
    # Add new entry button
    if st.button("➕ Add New Entry", use_container_width=True):
        add_symptom_entry()
    
    # Export data
    if st.button("📊 Export Data", use_container_width=True):
        export_timeline_data()


def render_insights_panel():
    """Render insights and recommendations panel."""
    st.markdown("### 💡 Insights & Recommendations")
    
    df = pd.DataFrame(st.session_state.symptom_timeline)
    
    # Generate insights
    insights = generate_timeline_insights(df)
    
    for insight in insights:
        st.markdown(
            f"""
            <div class="info-card" style="margin: 0.5rem 0;">
                <h4>{insight['icon']} {insight['title']}</h4>
                <p>{insight['description']}</p>
                <p style="font-style: italic; color: var(--medium-gray); font-size: 0.9rem;">
                    {insight['recommendation']}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def generate_sample_timeline_data():
    """Generate sample timeline data for demonstration."""
    data = []
    base_date = datetime.now() - timedelta(days=30)
    
    # Generate realistic symptom data with patterns
    for i in range(30):
        date = base_date + timedelta(days=i)
        
        # Create realistic patterns
        day_of_week = date.weekday()
        is_weekend = day_of_week >= 5
        
        # Base levels with some randomness
        hot_flashes = max(0, min(10, 3 + random.uniform(-1, 2) + (0.5 if is_weekend else 0)))
        night_sweats = max(0, min(10, 2 + random.uniform(-1, 1.5) + (0.3 if is_weekend else 0)))
        mood_changes = max(0, min(10, 2 + random.uniform(-1, 1.5) + (0.4 if is_weekend else 0)))
        sleep_quality = max(0, min(10, 6 + random.uniform(-1, 1) - (0.5 if is_weekend else 0)))
        cognitive_issues = max(0, min(10, 1 + random.uniform(-0.5, 1) + (0.2 if is_weekend else 0)))
        energy_level = max(0, min(10, 6 + random.uniform(-1, 1) - (0.3 if is_weekend else 0)))
        
        data.append({
            "date": date.strftime("%Y-%m-%d"),
            "hot_flashes": round(hot_flashes, 1),
            "night_sweats": round(night_sweats, 1),
            "mood_changes": round(mood_changes, 1),
            "sleep_quality": round(sleep_quality, 1),
            "cognitive_issues": round(cognitive_issues, 1),
            "energy_level": round(energy_level, 1)
        })
    
    return data


def add_symptom_entry():
    """Add new symptom entry."""
    with st.form("add_symptom_entry"):
        st.markdown("#### 📝 Add New Symptom Entry")
        
        date = st.date_input("Date", value=datetime.now().date())
        
        col1, col2 = st.columns(2)
        
        with col1:
            hot_flashes = st.slider("Hot Flashes", 0, 10, 3)
            night_sweats = st.slider("Night Sweats", 0, 10, 2)
            mood_changes = st.slider("Mood Changes", 0, 10, 2)
        
        with col2:
            sleep_quality = st.slider("Sleep Quality", 0, 10, 6)
            cognitive_issues = st.slider("Cognitive Issues", 0, 10, 1)
            energy_level = st.slider("Energy Level", 0, 10, 6)
        
        if st.form_submit_button("💾 Save Entry"):
            new_entry = {
                "date": date.strftime("%Y-%m-%d"),
                "hot_flashes": hot_flashes,
                "night_sweats": night_sweats,
                "mood_changes": mood_changes,
                "sleep_quality": sleep_quality,
                "cognitive_issues": cognitive_issues,
                "energy_level": energy_level
            }
            
            st.session_state.symptom_timeline.append(new_entry)
            st.success("✅ Entry added successfully!")
            st.rerun()


def export_timeline_data():
    """Export timeline data."""
    df = pd.DataFrame(st.session_state.symptom_timeline)
    
    # Convert to CSV
    csv = df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"symptom_timeline_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


def generate_timeline_insights(df):
    """Generate insights from timeline data."""
    insights = []
    
    # Hot flashes insight
    hot_flashes_avg = df['hot_flashes'].mean()
    if hot_flashes_avg > 5:
        insights.append({
            "icon": "🔥",
            "title": "Hot Flashes Pattern",
            "description": f"Your hot flashes average {hot_flashes_avg:.1f}/10, which is above moderate levels.",
            "recommendation": "Consider keeping a fan nearby and wearing layers you can remove easily."
        })
    
    # Sleep quality insight
    sleep_avg = df['sleep_quality'].mean()
    if sleep_avg < 5:
        insights.append({
            "icon": "😴",
            "title": "Sleep Quality Concern",
            "description": f"Your sleep quality averages {sleep_avg:.1f}/10, indicating potential sleep issues.",
            "recommendation": "Try maintaining a cool bedroom temperature and consistent bedtime routine."
        })
    
    # Energy level insight
    energy_avg = df['energy_level'].mean()
    if energy_avg < 5:
        insights.append({
            "icon": "⚡",
            "title": "Energy Level",
            "description": f"Your energy levels average {energy_avg:.1f}/10, which may be affecting your daily activities.",
            "recommendation": "Consider light exercise and balanced nutrition to boost energy naturally."
        })
    
    # Trend analysis
    recent_avg = df.tail(7)['hot_flashes'].mean()
    older_avg = df.head(7)['hot_flashes'].mean()
    
    if recent_avg < older_avg:
        insights.append({
            "icon": "📈",
            "title": "Positive Trend",
            "description": "Your hot flashes have been decreasing over time - great progress!",
            "recommendation": "Keep up whatever strategies are working for you."
        })
    elif recent_avg > older_avg:
        insights.append({
            "icon": "📉",
            "title": "Increasing Symptoms",
            "description": "Your hot flashes have been increasing recently.",
            "recommendation": "Consider discussing symptom management strategies with your healthcare provider."
        })
    
    return insights
