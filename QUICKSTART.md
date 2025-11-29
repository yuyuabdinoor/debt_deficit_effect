# 🚀 Quick Start Guide - Deficit Domino Effect

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the dashboard
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 🎮 How to Use

### Tab 1: Network Map 🕸️

**What it shows**: Visual representation of how African countries are fiscally connected

**How to use**:
1. Toggle between **2D** and **3D** views
2. In 3D mode: Click and drag to rotate, scroll to zoom
3. Hover over nodes to see country details
4. Red nodes = High risk, Green = Low risk
5. Thicker lines = Stronger trade relationships

**Pro tip**: Use 3D mode for presentations - it's visually stunning!

---

### Tab 2: Contagion Simulator 💥

**What it shows**: Simulates how a fiscal crisis spreads across Africa

**How to use**:
1. Select a country as "Crisis Epicenter" (try Nigeria or South Africa)
2. Adjust "Contagion Threshold" (lower = more spread)
3. Check "Animate Spread" for wave-by-wave visualization
4. Click **🚨 SIMULATE CRISIS**
5. Watch the domino effect in action!
6. Download the report for detailed analysis

**Pro tip**: Try different epicenters to see which countries are most dangerous

---

### Tab 3: Risk Analysis 📊

**What it shows**: Deep dive into individual country fiscal health

**How to use**:
1. Select a country from dropdown
2. View risk score (0-100)
3. See historical deficit trends
4. Check trade partner connections

**Pro tip**: Compare high-risk vs low-risk countries to spot patterns

---

### Tab 4: Trade Clusters 🔗

**What it shows**: Countries grouped by economic interdependence

**How to use**:
1. View automatically detected clusters
2. Check average risk per cluster
3. Identify regional vulnerabilities

**Pro tip**: Clusters show which countries will fall together like dominoes

---

### Tab 5: Historical Playback ⏳

**What it shows**: Time-lapse of network evolution from 1960-2025

**How to use**:
1. Select time period (e.g., 2000-2024)
2. Choose playback speed (1x recommended)
3. Click **▶️ Play Timeline**
4. Watch 60+ years of fiscal history unfold
5. See trend analysis at the end

**Pro tip**: Look for sudden changes during major events (2008 crisis, COVID)

---

## 🎯 Demo Scenarios for Judges

### Scenario 1: "The Nigeria Effect"
1. Go to Contagion Simulator
2. Select Nigeria as epicenter
3. Set threshold to 30%
4. Simulate and show how West Africa is affected
5. Download report to show professionalism

### Scenario 2: "Time Travel"
1. Go to Historical Playback
2. Set range 2000-2024
3. Play at 2x speed
4. Point out 2008 crisis and COVID impact
5. Show trend chart

### Scenario 3: "3D Wow Factor"
1. Go to Network Map
2. Switch to 3D view
3. Rotate the network while explaining connections
4. Zoom in on specific clusters
5. This is your "drop the mic" moment

---

## 🎨 Customization Tips

### Change Colors
Edit `app.py` line 20-30 to modify color scheme

### Add More Countries
Edit `create_trade_network()` function to add trade links

### Adjust Risk Algorithm
Modify `calculate_country_risk()` function

---

## 🐛 Troubleshooting

**Dashboard won't start?**
```bash
pip install --upgrade streamlit plotly networkx
```

**Animations laggy?**
- Reduce playback speed
- Use 2D instead of 3D
- Close other browser tabs

**Data not loading?**
- Ensure CSV file is in same directory
- Check file name matches exactly

---

## 📱 Presentation Tips

1. **Start with 3D network** - Immediate wow factor
2. **Run Nigeria simulation** - Shows real-world impact
3. **Play historical timeline** - Shows depth of analysis
4. **Download a report** - Shows professionalism
5. **End with clusters** - Shows systems thinking

**Time allocation** (5 min presentation):
- 1 min: Intro + 3D network
- 2 min: Contagion simulation
- 1 min: Historical playback
- 1 min: Key insights + Q&A

---

## 🏆 Winning Strategy

**What makes this unique:**
- Nobody else will have 3D networks
- Contagion simulation is interactive and memorable
- Historical playback shows long-term thinking
- Professional reports show real-world applicability
- "Domino effect" metaphor is powerful and clear

**Key talking points:**
1. "This isn't just data visualization - it's a crisis prediction tool"
2. "Watch how one country's problems cascade across the continent"
3. "We can see 60 years of fiscal history in 60 seconds"
4. "Policymakers can download actionable reports"
5. "This shows systems thinking - not just individual countries"

---

## 🎓 Technical Highlights to Mention

- Network graph theory (NetworkX)
- 3D visualization (Plotly 3D)
- Community detection algorithms
- Wave-based contagion modeling
- Time-series analysis
- Interactive web framework (Streamlit)

---

**Good luck! You've got this! 🚀**
