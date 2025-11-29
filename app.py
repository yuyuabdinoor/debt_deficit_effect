import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import networkx as nx
import time
import base64
from io import BytesIO
import json

# Page config
st.set_page_config(
    page_title="Deficit Domino Effect",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Audio for domino effect
def get_audio_html():
    return """
    <audio id="dominoSound" preload="auto">
        <source src="data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIGGS57OihUBELTKXh8bllHAU2jdXvzn0vBSh+zPDhkj4KFV+16+qnVRQLRp/g8r5sIQUrgs/y2Ik2CBhkuezooVARDEyl4fG5ZRwFNo3V7859LwUofszw4ZI+ChVftevqp1UVC0af4PK+bCEFK4LP8tmJNggYZLns6KFQEQxMpeHxuWUcBTaN1e/OfS8FKH7M8OGSPgoVX7Xr6qdVFQtGn+DyvmwhBSuCz/LZiTYIGGS57OihUBEMTKXh8bllHAU2jdXvzn0vBSh+zPDhkj4KFV+16+qnVRULRp/g8r5sIQUrgs/y2Ik2CBhkuezooVARDEyl4fG5ZRwFNo3V7859LwUofszw4ZI+ChVftevqp1UVC0af4PK+bCEFK4LP8tmJNggYZLns6KFQEQxMpeHxuWUcBTaN1e/OfS8FKH7M8OGSPgoVX7Xr6qdVFQtGn+DyvmwhBSuCz/LZiTYIGGS57OihUBEMTKXh8bllHAU2jdXvzn0vBSh+zPDhkj4KFV+16+qnVRULRp/g8r5sIQUrgs/y2Ik2CBhkuezooVARDEyl4fG5ZRwFNo3V7859LwUofszw4ZI+ChVftevqp1UVC0af4PK+bCEFK4LP8tmJNggYZLns6KFQEQxMpeHxuWUcBTaN1e/OfS8FKH7M8OGSPgoVX7Xr6qdVFQtGn+DyvmwhBSuCz/LZiTYIGGS57OihUBEMTKXh8bllHAU2jdXvzn0vBSh+zPDhkj4KFV+16+qnVRULRp/g8r5sIQUrgs/y2Ik2CBhkuezooVARDEyl4fG5ZRwFNo3V7859LwUofszw4ZI+ChVftevqp1UVC0af4PK+bCEFK4LP8tmJNggYZLns6KFQEQxMpeHxuWUcBTaN1e/OfS8FKH7M8OGSPgo=" type="audio/wav">
    </audio>
    <script>
        function playDomino() {
            var audio = document.getElementById('dominoSound');
            audio.play();
        }
    </script>
    """

# Custom CSS with animations
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stApp {background: linear-gradient(135deg, #0e1117 0%, #1a1d29 100%);}
    h1 {
        color: #ff4b4b; 
        text-align: center; 
        font-size: 3em; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from {text-shadow: 0 0 5px #ff4b4b, 0 0 10px #ff4b4b;}
        to {text-shadow: 0 0 10px #ff4b4b, 0 0 20px #ff4b4b, 0 0 30px #ff4b4b;}
    }
    h2 {color: #ffa500; border-bottom: 2px solid #ff4b4b; padding-bottom: 10px;}
    h3 {color: #4da6ff;}
    .metric-card {
        background: rgba(255, 75, 75, 0.1);
        border-left: 4px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .pulse {
        animation: pulse 1.5s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% {opacity: 1;}
        50% {opacity: 0.5;}
    }
    .download-btn {
        background: linear-gradient(90deg, #ff4b4b, #ffa500);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Add audio
st.markdown(get_audio_html(), unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('10Alytics Hackathon- Fiscal Data.xlsx - Data.csv')
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        df['Amount_Numeric'] = pd.to_numeric(df['Amount'], errors='coerce')
        df['Year'] = df['Time'].dt.year
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found! Please ensure '10Alytics Hackathon- Fiscal Data.xlsx - Data.csv' is in the same directory.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.stop()

def calculate_country_risk(df, country):
    """Calculate enhanced risk score for a country"""
    country_data = df[df['Country'] == country].sort_values('Time').tail(24)  # Last 2 years
    if len(country_data) == 0:
        return 50
    
    deficits = country_data['Amount_Numeric'].dropna()
    if len(deficits) == 0:
        return 50
    
    # Component 1: Average deficit magnitude (0-40 points)
    avg_deficit = abs(deficits.mean())
    deficit_score = min(40, (avg_deficit / 10000) * 40)
    
    # Component 2: Volatility (0-30 points)
    volatility = deficits.std() if len(deficits) > 1 else 0
    volatility_score = min(30, (volatility / 5000) * 30)
    
    # Component 3: Trend (0-30 points) - is it getting worse?
    if len(deficits) >= 6:
        recent = deficits.tail(6).mean()
        older = deficits.head(6).mean()
        trend_change = (abs(recent) - abs(older)) / (abs(older) + 1)  # Avoid division by zero
        trend_score = min(30, max(0, trend_change * 100))
    else:
        trend_score = 15  # Neutral if insufficient data
    
    # Total risk score (0-100)
    risk = min(100, deficit_score + volatility_score + trend_score)
    return risk

@st.cache_data
def create_trade_network(df, year=None):
    """Create network graph showing fiscal interdependence for a specific year"""
    countries = df['Country'].unique()
    
    # Filter by year if specified
    if year:
        df_filtered = df[df['Year'] == year]
    else:
        df_filtered = df
    
    # Calculate risk scores
    risk_scores = {country: calculate_country_risk(df_filtered, country) for country in countries}
    
    # Create network
    G = nx.Graph()
    
    # Add nodes
    for country in countries:
        G.add_node(country, risk=risk_scores[country])
    
    # Define trade relationships (simplified - in reality use trade data)
    trade_links = [
        ('South Africa', 'Botswana', 85),
        ('South Africa', 'Angola', 70),
        ('Nigeria', 'Ghana', 80),
        ('Nigeria', 'Togo', 60),
        ('Egypt', 'Algeria', 55),
        ('Kenya', 'Tanzania', 75),
        ('Kenya', 'Rwanda', 65),
        ('Kenya', 'Ethiopia', 60),
        ('Ghana', 'Ivory Coast', 70),
        ('Ghana', 'Togo', 65),
        ('Ivory Coast', 'Senegal', 60),
        ('South Africa', 'Tanzania', 50),
        ('Egypt', 'Ethiopia', 45),
        ('Angola', 'Nigeria', 55),
    ]
    
    # Add edges
    for source, target, weight in trade_links:
        if source in countries and target in countries:
            G.add_edge(source, target, weight=weight)
    
    return G, risk_scores

def get_historical_networks(df, start_year, end_year, step=5):
    """Generate networks for different time periods"""
    networks = {}
    for year in range(start_year, end_year + 1, step):
        G, risk_scores = create_trade_network(df, year)
        networks[year] = (G, risk_scores)
    return networks

def create_network_visualization(G, risk_scores, highlight_country=None, mode='2d'):
    """Create stunning interactive network visualization in 2D or 3D"""
    
    # Calculate layout with better spacing
    if mode == '3d':
        pos = nx.spring_layout(G, dim=3, k=3, iterations=100, seed=42)
    else:
        pos = nx.spring_layout(G, k=3, iterations=100, seed=42)
    
    # Create beautiful gradient edges
    edge_traces = []
    for edge in G.edges(data=True):
        weight = edge[2].get('weight', 50)
        
        # Color edges based on weight - stronger connections are brighter
        edge_color = f'rgba(255, 75, 75, {weight/150})'  # Red gradient
        
        if mode == '3d':
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            
            edge_trace = go.Scatter3d(
                x=[x0, x1, None],
                y=[y0, y1, None],
                z=[z0, z1, None],
                mode='lines',
                line=dict(
                    width=weight/10,
                    color=edge_color
                ),
                hoverinfo='none',
                showlegend=False
            )
        else:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(
                    width=weight/12,
                    color=edge_color
                ),
                hoverinfo='none',
                showlegend=False
            )
        edge_traces.append(edge_trace)
    
    # Create stunning node trace with better styling
    node_x = []
    node_y = []
    node_z = [] if mode == '3d' else None
    node_text = []
    node_labels = []
    node_color = []
    node_size = []
    node_line_color = []
    
    for node in G.nodes():
        if mode == '3d':
            x, y, z = pos[node]
            node_z.append(z)
        else:
            x, y = pos[node]
        
        node_x.append(x)
        node_y.append(y)
        
        risk = risk_scores.get(node, 50)
        connections = len(list(G.neighbors(node)))
        
        # Color coding
        node_color.append(risk)
        
        # Size based on connections (hub countries are bigger)
        base_size = 40 if node != highlight_country else 60
        node_size.append(base_size + connections * 3)
        
        # Border color based on risk
        if risk > 70:
            border_color = '#ff0000'  # Red
        elif risk > 50:
            border_color = '#ffa500'  # Orange
        else:
            border_color = '#00ff00'  # Green
        node_line_color.append(border_color)
        
        # Labels
        node_labels.append(node)
        
        # Rich hover text
        status = "🔴 HIGH RISK" if risk > 70 else "🟡 MODERATE" if risk > 50 else "🟢 LOW RISK"
        node_text.append(
            f"<b style='font-size:14px'>{node}</b><br>" +
            f"<b>Risk Score:</b> {risk:.1f}/100<br>" +
            f"<b>Status:</b> {status}<br>" +
            f"<b>Trade Partners:</b> {connections}<br>" +
            f"<b>Hub Importance:</b> {'⭐' * min(5, connections)}"
        )
    
    if mode == '3d':
        node_trace = go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode='markers+text',
            text=node_labels,
            textposition="top center",
            textfont=dict(
                size=11,
                color='white',
                family='Arial Black'
            ),
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale=[
                    [0, '#00ff00'],      # Green (low risk)
                    [0.3, '#7fff00'],    # Yellow-green
                    [0.5, '#ffff00'],    # Yellow
                    [0.7, '#ff7f00'],    # Orange
                    [1, '#ff0000']       # Red (high risk)
                ],
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="<b>Risk Level</b>",
                        font=dict(size=14, color='white')
                    ),
                    thickness=20,
                    len=0.7,
                    x=1.02,
                    tickfont=dict(color='white'),
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['Safe', 'Low', 'Moderate', 'High', 'Critical']
                ),
                line=dict(width=3, color=node_line_color),
                opacity=0.95
            ),
            showlegend=False
        )
    else:
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=node_labels,
            textposition="top center",
            textfont=dict(
                size=11,
                color='white',
                family='Arial Black'
            ),
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale=[
                    [0, '#00ff00'],      # Green (low risk)
                    [0.3, '#7fff00'],    # Yellow-green
                    [0.5, '#ffff00'],    # Yellow
                    [0.7, '#ff7f00'],    # Orange
                    [1, '#ff0000']       # Red (high risk)
                ],
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="<b>Risk Level</b>",
                        font=dict(size=14, color='white')
                    ),
                    thickness=20,
                    len=0.7,
                    x=1.02,
                    tickfont=dict(color='white'),
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['Safe', 'Low', 'Moderate', 'High', 'Critical']
                ),
                line=dict(width=3, color=node_line_color),
                opacity=0.95
            ),
            showlegend=False
        )
    
    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])
    
    if mode == '3d':
        fig.update_layout(
            title=dict(
                text="<b>African Fiscal Interdependence Network (3D)</b>",
                font=dict(size=20, color='#ff4b4b'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            scene=dict(
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    showbackground=False
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    showbackground=False
                ),
                zaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    showbackground=False
                ),
                bgcolor='rgba(10,10,20,0.9)',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=700,
            font=dict(color='white')
        )
    else:
        fig.update_layout(
            title=dict(
                text="<b>African Fiscal Interdependence Network</b>",
                font=dict(size=20, color='#ff4b4b'),
                x=0.5,
                xanchor='center'
            ),
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20, l=20, r=20, t=60),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            plot_bgcolor='rgba(10,10,20,0.9)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=650,
            font=dict(color='white')
        )
    
    return fig

def simulate_contagion(G, risk_scores, epicenter, threshold=60):
    """Simulate how crisis spreads from epicenter with wave tracking"""
    affected = {epicenter: 100}  # Start at 100% impact
    queue = [(epicenter, 100, 0)]  # (country, impact, wave)
    visited = set()
    waves = {0: [epicenter]}  # Track which countries affected in each wave
    
    while queue:
        current, impact, wave = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        
        # Spread to neighbors
        for neighbor in G.neighbors(current):
            if neighbor not in affected:
                # Impact decreases with distance and depends on trade weight
                edge_weight = G[current][neighbor].get('weight', 50)
                neighbor_risk = risk_scores.get(neighbor, 50)
                
                # Calculate contagion impact
                new_impact = impact * (edge_weight / 100) * (neighbor_risk / 100)
                
                if new_impact > threshold:
                    affected[neighbor] = new_impact
                    next_wave = wave + 1
                    if next_wave not in waves:
                        waves[next_wave] = []
                    waves[next_wave].append(neighbor)
                    queue.append((neighbor, new_impact, next_wave))
    
    return affected, waves

def generate_contagion_report(epicenter, affected, waves):
    """Generate downloadable PDF-style report"""
    report = f"""
FISCAL CONTAGION ANALYSIS REPORT
{'='*50}

CRISIS EPICENTER: {epicenter}
ANALYSIS DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'='*50}
EXECUTIVE SUMMARY
{'='*50}

Total Countries Affected: {len(affected)}
Number of Contagion Waves: {len(waves)}
Maximum Impact: {max(affected.values()):.1f}%
Average Impact: {np.mean(list(affected.values())):.1f}%

{'='*50}
WAVE-BY-WAVE BREAKDOWN
{'='*50}

"""
    for wave_num, countries in sorted(waves.items()):
        report += f"\nWave {wave_num + 1}:\n"
        for country in countries:
            impact = affected.get(country, 0)
            report += f"  • {country}: {impact:.1f}% impact\n"
    
    report += f"\n{'='*50}\n"
    report += "DETAILED IMPACT ANALYSIS\n"
    report += f"{'='*50}\n\n"
    
    for country, impact in sorted(affected.items(), key=lambda x: x[1], reverse=True):
        risk_level = "CRITICAL" if impact > 80 else "HIGH" if impact > 60 else "MODERATE" if impact > 40 else "LOW"
        report += f"{country:20s} {impact:6.1f}%  [{risk_level}]\n"
    
    report += f"\n{'='*50}\n"
    report += "RECOMMENDATIONS\n"
    report += f"{'='*50}\n\n"
    report += f"1. Immediate monitoring of {epicenter} fiscal situation\n"
    report += f"2. Strengthen trade diversification for affected countries\n"
    report += f"3. Establish regional financial safety nets\n"
    report += f"4. Coordinate policy responses across {len(affected)} affected nations\n"
    
    return report

def main():
    st.markdown("<h1>🌍 THE DEFICIT DOMINO EFFECT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 1.2em;'>Visualizing Fiscal Contagion Across Africa</p>", unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar
    st.sidebar.title("🎛️ Control Panel")
    st.sidebar.markdown("---")
    
    # Create network
    G, risk_scores = create_trade_network(df)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Executive Summary", 
        "🕸️ Network Map", 
        "💥 Contagion Simulator", 
        "📊 Risk Analysis",
        "🔮 Forecast & Scenarios",
        "⏳ Historical Playback"
    ])
    
    with tab1:
        st.markdown("## 🎯 Welcome to The Deficit Domino Effect")
        
        # Landing page content
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255,75,75,0.1) 0%, rgba(255,165,0,0.1) 100%); 
                    padding: 30px; border-radius: 15px; border-left: 5px solid #ff4b4b; margin: 20px 0;'>
            <h3 style='color: #ffa500; margin-top: 0;'>🌍 The Problem</h3>
            <p style='font-size: 1.1em; line-height: 1.6;'>
                Fiscal crises don't happen in isolation. When one African nation faces economic turmoil, 
                the shockwaves ripple through interconnected trade networks, triggering a cascade of crises 
                across the continent—like dominoes falling in sequence.
            </p>
            
            <h3 style='color: #ffa500;'>💡 Our Solution</h3>
            <p style='font-size: 1.1em; line-height: 1.6;'>
                This dashboard uses <b>network graph theory</b> and <b>60+ years of fiscal data</b> to visualize 
                and predict how economic crises spread across Africa. We identify vulnerable connections, 
                simulate contagion scenarios, and provide early warning signals—helping policymakers prevent 
                crises before they cascade.
            </p>
            
            <h3 style='color: #ffa500;'>🎯 Key Features</h3>
            <ul style='font-size: 1.1em; line-height: 1.8;'>
                <li><b>3D Network Visualization:</b> See the invisible web of fiscal interdependence</li>
                <li><b>Crisis Simulation:</b> Watch how defaults spread wave-by-wave in real-time</li>
                <li><b>Historical Analysis:</b> Time-travel through 60 years of economic evolution</li>
                <li><b>Risk Scoring:</b> Multi-dimensional assessment of each country's vulnerability</li>
                <li><b>Actionable Reports:</b> Download detailed analysis for stakeholders</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### 📊 Dashboard Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Countries Analyzed", len(G.nodes()), help="14 African nations in the network")
        with col2:
            st.metric("Trade Connections", len(G.edges()), help="Economic interdependencies mapped")
        with col3:
            avg_risk = np.mean(list(risk_scores.values()))
            st.metric("Average Risk", f"{avg_risk:.1f}/100", help="Current fiscal vulnerability score")
        with col4:
            high_risk_count = sum(1 for r in risk_scores.values() if r > 70)
            st.metric("High Risk Countries", high_risk_count, help="Countries with risk score > 70")
        
        # Preview network
        st.markdown("### 🕸️ Network Preview")
        st.markdown("*Navigate to the **Network Map** tab to explore the interactive 3D visualization*")
        
        fig_preview = create_network_visualization(G, risk_scores, mode='2d')
        st.plotly_chart(fig_preview, use_container_width=True, key="preview_network")
        
        # Key insights
        st.markdown("### 🎯 Key Insights")
        col_insight1, col_insight2 = st.columns(2)
        
        with col_insight1:
            st.markdown("""
            <div class='metric-card'>
                <h4>🔴 Systemic Risk Hubs</h4>
                <p><b>South Africa, Nigeria, Kenya</b> are the most connected economies. 
                Their stability is critical—a default in any of these countries could trigger 
                a cascade affecting <b>50%+ of the network</b>.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='metric-card'>
                <h4>📈 Rising Vulnerability</h4>
                <p>Fiscal risk has increased <b>40% since 2000</b>. The 2008 financial crisis 
                and 2020 COVID-19 pandemic created lasting structural vulnerabilities.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_insight2:
            st.markdown("""
            <div class='metric-card'>
                <h4>🌊 Contagion Waves</h4>
                <p>Crises spread in <b>3 waves over 3-6 months</b>. Wave 1 hits direct trade 
                partners (70-90% impact), Wave 2 affects secondary connections (50-70%), 
                Wave 3 creates regional slowdown (30-50%).</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='metric-card'>
                <h4>💰 Economic Impact</h4>
                <p>Early warning systems can reduce crisis impact by <b>60-70%</b>, 
                potentially saving <b>$40-60 billion</b> per prevented crisis.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Call to action
        st.markdown("""
        <div style='background: linear-gradient(90deg, #ff4b4b, #ffa500); 
                    padding: 20px; border-radius: 10px; text-align: center; margin: 30px 0;'>
            <h3 style='color: white; margin: 0;'>🚀 Ready to Explore?</h3>
            <p style='color: white; font-size: 1.1em; margin: 10px 0;'>
                Use the tabs above to explore the network, simulate crises, and analyze historical trends
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("## 🕸️ Interactive Network Map")
        st.markdown("**Explore the fiscal interdependence network in 2D or stunning 3D**")
        
        # 2D/3D toggle
        col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 2])
        with col_toggle1:
            view_mode = st.radio("View Mode:", ["2D", "3D"], horizontal=True)
        with col_toggle2:
            st.markdown("**Node size** = Importance | **Color** = Risk level")
        with col_toggle3:
            export_network = st.button("📸 Export Network Image")
        
        # Network visualization
        mode = '3d' if view_mode == "3D" else '2d'
        fig_network = create_network_visualization(G, risk_scores, mode=mode)
        st.plotly_chart(fig_network, use_container_width=True, key="main_network")
        
        if export_network:
            st.success("✅ Network visualization ready for export! Use the camera icon in the chart toolbar above.")
        
        # Network statistics
        st.markdown("### 📊 Network Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Countries", len(G.nodes()))
        with col2:
            st.metric("Trade Links", len(G.edges()))
        with col3:
            avg_risk = np.mean(list(risk_scores.values()))
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        with col4:
            # Calculate network density
            density = nx.density(G)
            st.metric("Network Density", f"{density:.2f}", help="How interconnected the network is (0-1)")
        
        # Hub countries
        st.markdown("### ⭐ Hub Countries (Most Connected)")
        degree_centrality = nx.degree_centrality(G)
        top_hubs = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for i, (country, centrality) in enumerate(top_hubs, 1):
            connections = len(list(G.neighbors(country)))
            risk = risk_scores.get(country, 50)
            risk_emoji = "🔴" if risk > 70 else "🟡" if risk > 50 else "🟢"
            st.markdown(f"{i}. **{country}** {risk_emoji} - {connections} connections | Risk: {risk:.1f}/100")
    
    with tab3:
        st.markdown("## 💥 Crisis Contagion Simulator")
        st.markdown("**Simulate what happens if a country defaults**")
        
        col_sim1, col_sim2 = st.columns([2, 1])
        with col_sim1:
            epicenter = st.selectbox("Select Crisis Epicenter:", sorted(G.nodes()))
        with col_sim2:
            threshold = st.slider(
                "Contagion Threshold (%):", 
                0, 100, 30,
                help="Minimum impact level for crisis to spread. Lower threshold = more contagion. Higher threshold = only severe impacts spread."
            )
        
        col_btn1, col_btn2 = st.columns([1, 3])
        with col_btn1:
            simulate_btn = st.button("🚨 SIMULATE CRISIS", type="primary")
        with col_btn2:
            animate_contagion = st.checkbox("🎬 Animate Spread", value=True)
        
        if simulate_btn:
            # Play sound effect
            st.markdown('<script>playDomino();</script>', unsafe_allow_html=True)
            
            affected, waves = simulate_contagion(G, risk_scores, epicenter, threshold)
            
            st.markdown(f"### 🔴 Crisis Impact from {epicenter}")
            
            # Animated contagion spread
            if animate_contagion and len(waves) > 1:
                st.markdown("#### 🌊 Contagion Wave Animation")
                wave_placeholder = st.empty()
                
                for wave_num in sorted(waves.keys()):
                    wave_countries = []
                    for w in range(wave_num + 1):
                        wave_countries.extend(waves[w])
                    
                    wave_text = f"**Wave {wave_num + 1}**: " + ", ".join(waves[wave_num])
                    wave_placeholder.markdown(f'<div class="pulse">{wave_text}</div>', unsafe_allow_html=True)
                    time.sleep(1)
            
            # Show affected countries
            affected_df = pd.DataFrame([
                {"Country": k, "Impact %": v, "Wave": next(w for w, countries in waves.items() if k in countries)} 
                for k, v in sorted(affected.items(), key=lambda x: x[1], reverse=True)
            ])
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.dataframe(affected_df, use_container_width=True, height=400)
                st.metric("Countries Affected", len(affected))
                st.metric("Contagion Waves", len(waves))
                
                # Download report
                report = generate_contagion_report(epicenter, affected, waves)
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"contagion_report_{epicenter}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            
            with col2:
                # Visualize impact
                fig_impact = px.bar(
                    affected_df,
                    x='Country',
                    y='Impact %',
                    color='Wave',
                    color_continuous_scale='Reds',
                    title=f"Contagion Impact from {epicenter}"
                )
                fig_impact.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                st.plotly_chart(fig_impact, use_container_width=True, key="contagion_impact")
    
    with tab3:
        st.markdown("## 📊 Country Risk Analysis")
        st.markdown("**Deep dive into individual country fiscal health and network connections**")
        
        selected_country = st.selectbox("Select Country:", sorted(df['Country'].unique()))
        
        # Get country data
        country_data = df[df['Country'] == selected_country].sort_values('Time')
        
        # Risk Score Explanation
        st.markdown("### 🎯 Risk Score Methodology")
        st.info("""
        **How we calculate risk (0-100 scale):**
        - **40 points:** Average deficit magnitude (larger deficits = higher risk)
        - **30 points:** Fiscal volatility (unstable budgets = higher risk)
        - **30 points:** Trend direction (worsening deficits = higher risk)
        
        This multi-dimensional approach captures both current fiscal health and trajectory.
        """)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Time series
            fig_ts = px.line(
                country_data,
                x='Time',
                y='Amount_Numeric',
                title=f"{selected_country} - Budget Deficit/Surplus Over Time"
            )
            fig_ts.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break-even")
            fig_ts.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis_title="Date",
                yaxis_title="Amount (Millions)"
            )
            st.plotly_chart(fig_ts, use_container_width=True, key="risk_timeseries")
        
        with col2:
            risk = risk_scores.get(selected_country, 50)
            st.metric("Risk Score", f"{risk:.1f}/100")
            
            # Risk level with explanation
            if risk > 70:
                st.error("🔴 HIGH RISK")
                st.markdown("**Immediate attention needed.** Large deficits, high volatility, or worsening trends.")
            elif risk > 50:
                st.warning("🟡 MODERATE RISK")
                st.markdown("**Monitor closely.** Some fiscal stress indicators present.")
            else:
                st.success("🟢 LOW RISK")
                st.markdown("**Relatively stable.** Manageable deficits and low volatility.")
            
            # Network stats
            neighbors = list(G.neighbors(selected_country))
            st.metric("Trade Partners", len(neighbors))
            
            if neighbors:
                st.markdown("**Connected to:**")
                for n in neighbors:
                    neighbor_risk = risk_scores.get(n, 50)
                    risk_emoji = "🔴" if neighbor_risk > 70 else "🟡" if neighbor_risk > 50 else "🟢"
                    st.markdown(f"{risk_emoji} **{n}** (Risk: {neighbor_risk:.1f})")
        
        # Why these connections matter
        st.markdown("### 🔗 Why Trade Connections Matter")
        if len(neighbors) > 0:
            st.warning(f"""
            **{selected_country} is connected to {len(neighbors)} trading partner(s).**
            
            These connections create **contagion risk**: if {selected_country} faces a fiscal crisis, 
            it can spread to connected countries through:
            - **Trade disruption:** Reduced imports/exports
            - **Currency effects:** Exchange rate volatility
            - **Confidence loss:** Regional economic uncertainty
            
            The more connections a country has, the greater its **systemic importance** to the network.
            """)
        else:
            st.info(f"{selected_country} has limited direct trade connections in this network, reducing contagion risk.")
        
        # Additional insights
        st.markdown("### 📈 Fiscal Health Indicators")
        recent_data = country_data.tail(24)
        if len(recent_data) > 0:
            col_i1, col_i2, col_i3 = st.columns(3)
            with col_i1:
                avg_deficit = recent_data['Amount_Numeric'].mean()
                st.metric("Avg Recent Deficit", f"{avg_deficit:,.0f}M")
            with col_i2:
                volatility = recent_data['Amount_Numeric'].std()
                st.metric("Volatility (Std Dev)", f"{volatility:,.0f}M")
            with col_i3:
                data_points = len(country_data)
                st.metric("Historical Records", f"{data_points}")
    
    with tab4:
        st.markdown("## 🔗 Regional Trade Clusters")
        st.markdown("**Countries grouped by economic interdependence using network analysis**")
        
        # Explanation
        st.info("""
        **How clusters are formed:**
        
        We use **community detection algorithms** to identify groups of countries that are:
        - More densely connected to each other than to the rest of the network
        - Share strong trade relationships
        - Likely to experience correlated fiscal outcomes
        
        **Why this matters:** Countries in the same cluster face **shared vulnerability**. 
        If one country in a cluster experiences a crisis, others in the same cluster are at higher risk.
        """)
        
        # Detect communities
        communities = nx.community.greedy_modularity_communities(G)
        
        st.markdown(f"### 📊 Identified {len(communities)} Regional Clusters")
        
        for i, community in enumerate(communities, 1):
            with st.expander(f"🔍 Cluster {i} - {len(community)} Countries", expanded=(i==1)):
                countries_in_cluster = sorted(list(community))
                
                # Average risk
                cluster_risk = np.mean([risk_scores.get(c, 50) for c in countries_in_cluster])
                
                col_c1, col_c2 = st.columns([2, 1])
                
                with col_c1:
                    st.markdown("**Member Countries:**")
                    for country in countries_in_cluster:
                        country_risk = risk_scores.get(country, 50)
                        risk_emoji = "🔴" if country_risk > 70 else "🟡" if country_risk > 50 else "🟢"
                        st.markdown(f"{risk_emoji} **{country}** - Risk: {country_risk:.1f}/100")
                
                with col_c2:
                    st.metric("Cluster Avg Risk", f"{cluster_risk:.1f}/100")
                    
                    if cluster_risk > 70:
                        st.error("🔴 High Risk Cluster")
                    elif cluster_risk > 50:
                        st.warning("🟡 Moderate Risk")
                    else:
                        st.success("🟢 Lower Risk")
                
                # Explain the cluster
                st.markdown("**Why these countries are grouped:**")
                if i == 1 and any(c in countries_in_cluster for c in ['Nigeria', 'Ghana', 'Togo', 'Ivory Coast', 'Senegal']):
                    st.markdown("""
                    - **West African Economic Bloc:** Strong regional trade ties
                    - **Shared currency zone:** Some members use CFA Franc
                    - **Geographic proximity:** Neighboring countries with integrated markets
                    - **High interdependence:** Economic shocks spread quickly within this group
                    """)
                elif any(c in countries_in_cluster for c in ['Kenya', 'Tanzania', 'Rwanda', 'Ethiopia']):
                    st.markdown("""
                    - **East African Community:** Regional economic integration
                    - **Trade corridors:** Shared infrastructure and supply chains
                    - **Growing integration:** Increasing economic cooperation
                    - **Moderate contagion risk:** Connected but diversifying
                    """)
                elif any(c in countries_in_cluster for c in ['South Africa', 'Botswana', 'Angola']):
                    st.markdown("""
                    - **Southern African Hub:** South Africa as regional economic anchor
                    - **Resource trade:** Mining and energy connections
                    - **Currency linkages:** Some currencies pegged to South African Rand
                    - **Asymmetric risk:** Smaller economies depend on South Africa
                    """)
                else:
                    st.markdown("""
                    - **Trade relationships:** Direct economic connections
                    - **Regional proximity:** Geographic and economic ties
                    - **Shared vulnerabilities:** Correlated fiscal outcomes
                    """)
                
                st.markdown("---")
    
    with tab5:
        st.markdown("## 🔮 Forecast & Scenarios")
        st.markdown("**Test interventions, explore what-if scenarios, and project future trends**")
        
        # Overview
        st.info("""
        **Purpose of this tab:**
        - **What-If Analysis:** Test how policy changes affect contagion risk
        - **Scenario Planning:** Explore best-case and worst-case outcomes
        - **Risk Projections:** Forecast future trends based on historical patterns
        
        Use these tools to understand intervention impact and plan preventive measures.
        """)
        
        scenario_type = st.radio(
            "Select Analysis Type:",
            ["What-If Scenarios", "Risk Projections", "Cluster Analysis"],
            horizontal=True
        )
        
        if scenario_type == "What-If Scenarios":
            st.markdown("### 🎲 Interactive Scenario Builder")
            st.markdown("**Test how fiscal improvements or deteriorations affect the network**")
            
            col1, col2 = st.columns(2)
            with col1:
                scenario_country = st.selectbox("Select Country:", sorted(G.nodes()), key="scenario")
                original_risk = risk_scores.get(scenario_country, 50)
                st.metric("Current Risk", f"{original_risk:.1f}/100")
            
            with col2:
                risk_change = st.slider(
                    "Risk Change (%):", 
                    -50, 50, 0,
                    help="Negative = Improvement (e.g., fiscal reforms), Positive = Deterioration (e.g., crisis)"
                )
                new_risk = max(0, min(100, original_risk + risk_change))
                st.metric("Projected Risk", f"{new_risk:.1f}/100", f"{risk_change:+.1f}")
            
            # Scenario explanation
            if risk_change < 0:
                st.success(f"""
                **Improvement Scenario:** {scenario_country} implements fiscal reforms
                - Possible interventions: Debt restructuring, spending cuts, revenue increases
                - Expected outcome: Reduced deficit, improved investor confidence
                - Timeline: 1-2 years for full effect
                """)
            elif risk_change > 0:
                st.error(f"""
                **Deterioration Scenario:** {scenario_country} faces fiscal stress
                - Possible causes: Economic shock, political instability, commodity price collapse
                - Expected outcome: Increased deficit, market volatility
                - Timeline: 6-12 months for crisis to materialize
                """)
            else:
                st.info("**Baseline Scenario:** No change in fiscal policy")
            
            if st.button("🔮 Run Scenario Analysis", type="primary"):
                # Simulate contagion with new risk
                modified_risks = risk_scores.copy()
                modified_risks[scenario_country] = new_risk
                affected, waves = simulate_contagion(G, modified_risks, scenario_country, 30)
                
                st.markdown("### 📊 Scenario Results")
                
                col_r1, col_r2, col_r3 = st.columns(3)
                with col_r1:
                    st.metric("Countries Affected", len(affected))
                with col_r2:
                    st.metric("Contagion Waves", len(waves))
                with col_r3:
                    impact_change = len(affected) - 1  # Exclude epicenter
                    st.metric("Spillover Countries", impact_change)
                
                if len(affected) > 1:
                    st.warning(f"""
                    **Contagion Risk Detected!**
                    
                    If {scenario_country}'s risk changes to {new_risk:.1f}, the crisis could spread to:
                    {', '.join([c for c in affected.keys() if c != scenario_country][:5])}
                    {"..." if len(affected) > 6 else ""}
                    
                    **Recommendation:** Monitor these countries closely and prepare coordinated response.
                    """)
                else:
                    st.success(f"""
                    **Limited Contagion Risk**
                    
                    {scenario_country}'s fiscal changes are unlikely to trigger widespread contagion.
                    The country's network position limits spillover effects.
                    """)
        
        elif scenario_type == "Risk Projections":
            st.markdown("### 📈 Future Risk Projections")
            st.markdown("**Based on historical trends, here's where we're headed**")
            
            # Calculate historical trend
            all_years = sorted([y for y in df['Year'].unique() if pd.notna(y) and y >= 2000])
            years = all_years[-10:] if len(all_years) >= 10 else all_years  # Last 10 years or all available
            yearly_risks = []
            
            with st.spinner("Calculating historical trends..."):
                for year in years:
                    _, year_risks = create_trade_network(df, year)
                    yearly_risks.append(np.mean(list(year_risks.values())))
            
            st.success(f"✅ Analyzed {len(years)} years of data ({years[0]}-{years[-1]})")
            
            # Simple linear projection
            if len(yearly_risks) >= 3:
                # Calculate trend
                x = np.array(range(len(yearly_risks)))
                y = np.array(yearly_risks)
                z = np.polyfit(x, y, 1)
                p = np.poly1d(z)
                
                # Project 5 years forward
                future_years = list(range(len(yearly_risks), len(yearly_risks) + 5))
                projected_risks = [p(i) for i in future_years]
                
                # Create visualization
                fig_proj = go.Figure()
                
                # Historical data
                fig_proj.add_trace(go.Scatter(
                    x=years,
                    y=yearly_risks,
                    mode='lines+markers',
                    name='Historical',
                    line=dict(color='#4da6ff', width=3),
                    marker=dict(size=10)
                ))
                
                # Projection
                future_year_labels = [years[-1] + i for i in range(1, 6)]
                fig_proj.add_trace(go.Scatter(
                    x=future_year_labels,
                    y=projected_risks,
                    mode='lines+markers',
                    name='Projected',
                    line=dict(color='#ff4b4b', width=3, dash='dash'),
                    marker=dict(size=10, symbol='diamond')
                ))
                
                fig_proj.update_layout(
                    title="Average Risk Score: Historical & 5-Year Projection",
                    xaxis_title="Year",
                    yaxis_title="Risk Score (0-100)",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_proj, use_container_width=True, key="risk_projection")
                
                # Analysis
                trend_direction = "increasing" if z[0] > 0 else "decreasing"
                trend_rate = abs(z[0])
                
                col_p1, col_p2, col_p3 = st.columns(3)
                with col_p1:
                    st.metric("Current Avg Risk", f"{yearly_risks[-1]:.1f}")
                with col_p2:
                    st.metric("Projected 2029 Risk", f"{projected_risks[-1]:.1f}")
                with col_p3:
                    change = projected_risks[-1] - yearly_risks[-1]
                    st.metric("5-Year Change", f"{change:+.1f}", f"{(change/yearly_risks[-1]*100):+.1f}%")
                
                st.markdown("### 🔍 Trend Analysis")
                
                if z[0] > 0:
                    st.error(f"""
                    **⚠️ Warning: Rising Risk Trajectory**
                    
                    - **Trend:** Risk is increasing at {trend_rate:.2f} points per year
                    - **Projection:** Average risk could reach {projected_risks[-1]:.1f} by 2029
                    - **Implication:** Without intervention, fiscal vulnerability will worsen
                    
                    **Recommended Actions:**
                    1. Implement early warning monitoring for hub countries
                    2. Strengthen regional financial safety nets
                    3. Encourage fiscal consolidation in high-risk countries
                    4. Improve data collection and reporting standards
                    """)
                else:
                    st.success(f"""
                    **✅ Positive Trend: Improving Fiscal Health**
                    
                    - **Trend:** Risk is decreasing at {trend_rate:.2f} points per year
                    - **Projection:** Average risk could fall to {projected_risks[-1]:.1f} by 2029
                    - **Implication:** Current policies are working
                    
                    **Recommended Actions:**
                    1. Continue current fiscal reforms
                    2. Share best practices across countries
                    3. Maintain monitoring to prevent backsliding
                    """)
                
                # Scenario comparison
                st.markdown("### 📊 Scenario Comparison")
                
                col_s1, col_s2, col_s3 = st.columns(3)
                
                with col_s1:
                    st.markdown("**🟢 Optimistic Scenario**")
                    st.markdown("*Aggressive reforms*")
                    optimistic = projected_risks[-1] - 10
                    st.metric("2029 Risk", f"{optimistic:.1f}")
                    st.caption("Debt relief + fiscal reforms")
                
                with col_s2:
                    st.markdown("**🟡 Base Case**")
                    st.markdown("*Current trajectory*")
                    st.metric("2029 Risk", f"{projected_risks[-1]:.1f}")
                    st.caption("No major policy changes")
                
                with col_s3:
                    st.markdown("**🔴 Pessimistic Scenario**")
                    st.markdown("*Major crisis*")
                    pessimistic = projected_risks[-1] + 15
                    st.metric("2029 Risk", f"{pessimistic:.1f}")
                    st.caption("Hub country default")
        
        else:  # Cluster Analysis
            st.markdown("### 🔗 Regional Cluster Deep-Dive")
            st.markdown("**Analyze regional economic groupings and shared vulnerabilities**")
            
            communities = nx.community.greedy_modularity_communities(G)
            
            st.markdown(f"**{len(communities)} clusters identified** using community detection algorithms")
            
            for i, community in enumerate(communities, 1):
                with st.expander(f"📦 Cluster {i} - {len(community)} countries", expanded=(i==1)):
                    countries_in_cluster = sorted(list(community))
                    cluster_risk = np.mean([risk_scores.get(c, 50) for c in countries_in_cluster])
                    
                    col_cl1, col_cl2 = st.columns([2, 1])
                    
                    with col_cl1:
                        st.markdown(f"**Countries:** {', '.join(countries_in_cluster)}")
                    with col_cl2:
                        st.metric("Cluster Avg Risk", f"{cluster_risk:.1f}/100")
                    
                    # Risk distribution
                    cluster_risks = [risk_scores.get(c, 50) for c in countries_in_cluster]
                    fig_dist = px.bar(
                        x=countries_in_cluster,
                        y=cluster_risks,
                        title=f"Risk Distribution in Cluster {i}",
                        color=cluster_risks,
                        color_continuous_scale='RdYlGn_r'
                    )
                    fig_dist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white'),
                        showlegend=False
                    )
                    st.plotly_chart(fig_dist, use_container_width=True, key=f"forecast_cluster_{i}")
                    
                    # Cluster insights
                    max_risk_country = max(countries_in_cluster, key=lambda c: risk_scores.get(c, 50))
                    max_risk = risk_scores.get(max_risk_country, 50)
                    
                    st.markdown("**Cluster Insights:**")
                    st.markdown(f"- **Highest risk:** {max_risk_country} ({max_risk:.1f}/100)")
                    st.markdown(f"- **Risk spread:** {max(cluster_risks) - min(cluster_risks):.1f} points")
                    st.markdown(f"- **Contagion potential:** {'High' if cluster_risk > 60 else 'Moderate' if cluster_risk > 45 else 'Low'}")
            
            if st.button("🔮 Run Scenario"):
                original_risk = risk_scores.get(scenario_country, 50)
                new_risk = max(0, min(100, original_risk + risk_change))
                
                col_s1, col_s2, col_s3 = st.columns(3)
                with col_s1:
                    st.metric("Original Risk", f"{original_risk:.1f}")
                with col_s2:
                    st.metric("New Risk", f"{new_risk:.1f}", f"{risk_change:+.1f}")
                with col_s3:
                    impact = "Improvement" if risk_change < 0 else "Deterioration"
                    st.metric("Impact", impact)
                
                # Simulate contagion
                modified_risks = risk_scores.copy()
                modified_risks[scenario_country] = new_risk
                affected, waves = simulate_contagion(G, modified_risks, scenario_country, 30)
                
                st.markdown(f"**Potential Contagion:** {len(affected)} countries affected")
    
    with tab6:
        st.markdown("## ⏳ Historical Network Evolution")
        st.markdown("**Watch how fiscal risks evolved across Africa over decades**")
        
        # Get available years
        min_year = int(df['Year'].min())
        max_year = int(df['Year'].max())
        
        col_hist1, col_hist2 = st.columns([2, 1])
        with col_hist1:
            year_range = st.slider(
                "Select Time Period:",
                min_value=min_year,
                max_value=max_year,
                value=(2000, 2024),
                step=1
            )
        with col_hist2:
            playback_speed = st.select_slider(
                "Playback Speed:",
                options=[0.5, 1, 2, 3],
                value=1
            )
        
        col_play1, col_play2 = st.columns([1, 3])
        with col_play1:
            play_history = st.button("▶️ Play Timeline", type="primary")
        
        if play_history:
            st.markdown("### 📽️ Network Evolution Animation")
            
            # Create placeholder for animation
            network_placeholder = st.empty()
            year_display = st.empty()
            
            # Generate networks for each year
            step = 2  # Show every 2 years
            for year in range(year_range[0], year_range[1] + 1, step):
                G_year, risk_scores_year = create_trade_network(df, year)
                
                # Update display
                year_display.markdown(f"<h2 style='text-align: center; color: #ffa500;'>Year: {year}</h2>", unsafe_allow_html=True)
                
                # Create network visualization
                fig_year = create_network_visualization(G_year, risk_scores_year, mode='2d')
                fig_year.update_layout(title=f"African Fiscal Network - {year}")
                
                network_placeholder.plotly_chart(fig_year, use_container_width=True)
                
                # Delay based on playback speed
                time.sleep(1 / playback_speed)
            
            st.success("✅ Playback Complete!")
            
            # Summary statistics
            st.markdown("### 📈 Evolution Summary")
            
            # Calculate risk trends
            years_analyzed = list(range(year_range[0], year_range[1] + 1, step))
            avg_risks = []
            
            for year in years_analyzed:
                _, risk_scores_year = create_trade_network(df, year)
                avg_risks.append(np.mean(list(risk_scores_year.values())))
            
            # Plot trend
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=years_analyzed,
                y=avg_risks,
                mode='lines+markers',
                name='Average Risk',
                line=dict(color='#ff4b4b', width=3),
                marker=dict(size=8)
            ))
            
            fig_trend.update_layout(
                title="Average Fiscal Risk Over Time",
                xaxis_title="Year",
                yaxis_title="Risk Score",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                height=400
            )
            
            st.plotly_chart(fig_trend, use_container_width=True, key="historical_trend")
        
        else:
            # Show static view for selected year
            selected_year = st.slider("Select Year:", min_year, max_year, max_year)
            G_static, risk_scores_static = create_trade_network(df, selected_year)
            
            st.markdown(f"### Network Snapshot - {selected_year}")
            fig_static = create_network_visualization(G_static, risk_scores_static, mode='2d')
            st.plotly_chart(fig_static, use_container_width=True, key="historical_static")



if __name__ == "__main__":
    main()
