# 🌍 The Deficit Domino Effect

**An Interactive Network Visualization of Fiscal Contagion Across Africa**

## 🎯 Concept

This dashboard visualizes how fiscal crises cascade across African economies through trade and economic interdependence. Using network graph theory, it shows:

- **Fiscal Interdependence**: How countries are connected through trade
- **Crisis Contagion**: Simulate what happens when one country defaults
- **Risk Propagation**: Visualize how fiscal problems spread like dominoes
- **Regional Clusters**: Identify economically linked country groups

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

## 📊 Features

### 1. Network Map 🕸️
- **2D & 3D Views**: Toggle between 2D and stunning 3D network visualizations
- Interactive network graph showing all 14 African countries
- Node color = Risk level (Red = High, Green = Low)
- Edge thickness = Trade relationship strength
- Hover for detailed country information
- Rotate, zoom, and explore in 3D space

### 2. Contagion Simulator 💥
- **Animated Crisis Spread**: Watch contagion spread wave-by-wave in real-time
- **Sound Effects**: Domino falling sounds when crisis triggers
- Select any country as "crisis epicenter"
- Adjust contagion threshold to see different scenarios
- **Wave Tracking**: See which countries affected in each wave
- **Download Reports**: Export detailed PDF-style analysis reports
- Quantify impact percentage on each affected country

### 3. Risk Analysis 📊
- Individual country risk scores (0-100)
- Historical deficit/surplus trends
- Trade partner connections
- Risk level classification
- Interactive time series charts

### 4. Trade Clusters 🔗
- Automatic detection of economically linked regions
- Cluster-level risk assessment
- Identify vulnerable regional groups
- Community detection algorithms

### 5. Historical Playback ⏳ **NEW!**
- **Time Travel**: Watch network evolution from 1960-2025
- **Animated Timeline**: Play through decades of fiscal data
- **Adjustable Speed**: Control playback speed (0.5x to 3x)
- **Trend Analysis**: See how average risk changed over time
- **Year Snapshots**: Jump to any specific year
- Visualize how crises emerged and spread historically

## 🎨 Design Philosophy

- **Dark theme** with neon accents for modern, professional look
- **Interactive elements** - click, hover, simulate
- **Real-time calculations** - instant feedback
- **Network thinking** - shows systems, not just individual countries

## 🏆 Why This Wins

1. **Unique Angle**: Nobody else will use network graphs for fiscal data
2. **Visual Impact**: 3D network visualizations are stunning and memorable
3. **Sophisticated Analysis**: Shows systems thinking and interdependence
4. **Interactive**: Judges can play with the contagion simulator
5. **Actionable**: Policymakers can identify vulnerable connections
6. **Animated**: Real-time contagion spread and historical playback
7. **Immersive**: Sound effects and smooth animations
8. **Professional**: Downloadable reports for stakeholders
9. **Time Dimension**: Historical evolution shows long-term patterns
10. **Wow Factor**: 3D networks + animations = unforgettable

## 📈 Technical Stack

- **Streamlit**: Interactive web app framework
- **Plotly**: Beautiful, interactive visualizations
- **NetworkX**: Graph theory and network analysis
- **Pandas/NumPy**: Data processing

## 🎓 Key Insights

- **South Africa** is the most connected hub (affects Botswana, Angola, Tanzania)
- **Nigeria-Ghana** corridor is a critical trade link
- **East African cluster** (Kenya-Tanzania-Rwanda-Ethiopia) is tightly connected
- **West African cluster** (Ghana-Ivory Coast-Togo-Senegal) shows regional interdependence

## ✅ Implemented Features

- ✅ 3D network visualization
- ✅ Animated contagion spread
- ✅ Sound effects for crisis simulation
- ✅ Downloadable PDF-style reports
- ✅ Historical timeline playback
- ✅ Wave-by-wave tracking
- ✅ Interactive controls

## 🔮 Future Enhancements

- Real trade data integration (World Bank API)
- Currency correlation analysis
- Machine learning for crisis prediction
- VR/AR network exploration
- Multi-indicator composite scoring

## 📝 Data Source

10Alytics Hackathon - Fiscal Data (23,784 records, 14 countries, 1960-2025)

---

**Built for 10Alytics Hackathon** | Made with ❤️ and lots of ☕
