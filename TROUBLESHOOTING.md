# 🔧 Troubleshooting Guide - The Deficit Domino Effect

## 🚨 Common Issues & Solutions

---

## Issue #1: Dashboard Won't Start

### Symptom:
```bash
$ streamlit run app.py
ModuleNotFoundError: No module named 'streamlit'
```

### Solution:
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install streamlit pandas numpy plotly networkx

# Try again
streamlit run app.py
```

### Still not working?
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install
pip install -r requirements.txt
```

---

## Issue #2: Data Won't Load

### Symptom:
```
FileNotFoundError: [Errno 2] No such file or directory: '10Alytics Hackathon- Fiscal Data.xlsx - Data.csv'
```

### Solution:
```bash
# Check if file exists
ls -la "10Alytics Hackathon- Fiscal Data.xlsx - Data.csv"

# Make sure you're in the right directory
pwd

# Run from project root
cd /path/to/project
streamlit run app.py
```

### File name issues?
- Ensure exact spelling (including spaces)
- Check for hidden characters
- Try renaming to simpler name: `fiscal_data.csv`
- Update `app.py` line 42 to match new name

---

## Issue #3: Animations Are Laggy

### Symptom:
- 3D network rotates slowly
- Historical playback stutters
- Browser feels sluggish

### Solution 1: Use 2D Instead
```
1. Go to Network Map tab
2. Select "2D" instead of "3D"
3. Much faster performance
```

### Solution 2: Reduce Playback Speed
```
1. Go to Historical Playback
2. Set speed to 0.5x or 1x
3. Smoother animation
```

### Solution 3: Close Other Apps
```bash
# Close unnecessary browser tabs
# Close other applications
# Restart browser
```

### Solution 4: Use Chrome
```
Chrome generally performs better than Safari/Firefox
for Plotly visualizations
```

---

## Issue #4: Port Already in Use

### Symptom:
```
OSError: [Errno 48] Address already in use
```

### Solution:
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run app.py --server.port 8502
```

---

## Issue #5: Network Graph Not Showing

### Symptom:
- Blank space where network should be
- "Loading..." never finishes

### Solution:
```bash
# Check if NetworkX is installed
python -c "import networkx; print('OK')"

# If error, install it
pip install networkx

# Restart dashboard
streamlit run app.py
```

---

## Issue #6: Download Button Not Working

### Symptom:
- Click "Download Report" but nothing happens
- No file downloads

### Solution:
```
1. Check browser download settings
2. Allow downloads from localhost
3. Check Downloads folder
4. Try different browser
```

### Alternative:
```
Copy report text manually:
1. Run simulation
2. Select report text
3. Copy (Cmd+C / Ctrl+C)
4. Paste into text editor
5. Save manually
```

---

## Issue #7: Sound Effects Not Playing

### Symptom:
- No domino sound during simulation
- Silent animations

### Solution:
```
1. Check browser sound settings
2. Unmute tab
3. Check system volume
4. Try different browser
```

### Note:
Sound effects are optional - dashboard works fine without them!

---

## Issue #8: Historical Playback Crashes

### Symptom:
- Browser freezes during timeline animation
- "Page Unresponsive" error

### Solution:
```
1. Reduce time range (e.g., 2010-2024 instead of 2000-2024)
2. Use slower playback speed (0.5x or 1x)
3. Close other tabs
4. Refresh page and try again
```

---

## Issue #9: Colors Look Wrong

### Symptom:
- Network nodes all same color
- Can't distinguish risk levels

### Solution:
```python
# Check if data has values
# In app.py, add debug print:
print(risk_scores)

# Should show:
# {'Nigeria': 65.2, 'Ghana': 58.3, ...}

# If all same value, check calculate_country_risk()
```

---

## Issue #10: CSV Encoding Error

### Symptom:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte...
```

### Solution:
```python
# In app.py, change line 42 to:
df = pd.read_csv('10Alytics Hackathon- Fiscal Data.xlsx - Data.csv', 
                 encoding='latin-1')

# Or try:
df = pd.read_csv('10Alytics Hackathon- Fiscal Data.xlsx - Data.csv', 
                 encoding='iso-8859-1')
```

---

## Issue #11: Memory Error

### Symptom:
```
MemoryError: Unable to allocate array
```

### Solution:
```python
# Reduce data size
# In app.py, add after loading:
df = df.tail(5000)  # Use only recent 5000 records

# Or sample data:
df = df.sample(frac=0.5)  # Use 50% of data
```

---

## Issue #12: Presentation Computer Issues

### Symptom:
- Works on your laptop
- Doesn't work on presentation computer

### Solution:
```
BEFORE PRESENTATION:
1. Test on presentation computer
2. Install dependencies there
3. Copy entire project folder
4. Have backup screenshots
5. Practice on that computer
```

### Emergency Backup:
```
If tech fails completely:
1. Use screenshots from phone/tablet
2. Explain concept verbally
3. Draw on whiteboard if available
4. Focus on insights, not visuals
5. Stay calm - judges understand
```

---

## Issue #13: Python Version Incompatibility

### Symptom:
```
SyntaxError: invalid syntax
```

### Solution:
```bash
# Check Python version
python --version

# Need Python 3.8 or higher
# If lower, upgrade Python

# Or use specific version:
python3.9 -m pip install -r requirements.txt
python3.9 -m streamlit run app.py
```

---

## Issue #14: Plotly Not Rendering

### Symptom:
- Charts show as blank boxes
- "Loading..." forever

### Solution:
```bash
# Reinstall Plotly
pip uninstall plotly
pip install plotly==5.18.0

# Clear browser cache
# Restart browser
# Try again
```

---

## Issue #15: Streamlit Caching Issues

### Symptom:
- Old data showing
- Changes not reflecting

### Solution:
```bash
# Clear Streamlit cache
streamlit cache clear

# Or restart with:
streamlit run app.py --server.runOnSave true
```

---

## 🆘 Emergency Procedures

### If Dashboard Completely Fails:

#### Plan A: Use Backup Computer
```
1. Have project on USB drive
2. Switch to backup laptop
3. Run from there
```

#### Plan B: Use Screenshots
```
1. Show pre-captured screenshots
2. Explain what would happen
3. Focus on concept
```

#### Plan C: Whiteboard Presentation
```
1. Draw network on whiteboard
2. Explain domino effect
3. Show insights verbally
4. Emphasize innovation
```

#### Plan D: Concept-Only Pitch
```
1. Explain the idea clearly
2. Describe features
3. Show understanding of data
4. Emphasize uniqueness
```

**Remember: Judges care about IDEAS, not just tech!**

---

## 🧪 Pre-Presentation Testing

### Run This Checklist:

```bash
# 1. Test data loading
python -c "import pandas as pd; df = pd.read_csv('10Alytics Hackathon- Fiscal Data.xlsx - Data.csv'); print(f'Loaded {len(df)} records')"

# 2. Test dependencies
python test_dashboard.py

# 3. Test dashboard
streamlit run app.py

# 4. Test each tab
# - Click through all 5 tabs
# - Try 3D network
# - Run simulation
# - Play timeline
# - Download report

# 5. Test on presentation computer
# - Repeat all above tests
# - Check display resolution
# - Test with projector
```

---

## 📞 Quick Fixes Reference

| Problem | Quick Fix |
|---------|-----------|
| Won't start | `pip install -r requirements.txt` |
| Data error | Check file name, try encoding='latin-1' |
| Slow animations | Use 2D, reduce speed |
| Port in use | `pkill -f streamlit` |
| Network blank | `pip install networkx` |
| Download fails | Try different browser |
| No sound | Check volume, try Chrome |
| Crashes | Reduce data size, close tabs |
| Colors wrong | Check risk_scores values |
| Memory error | Use df.tail(5000) |

---

## 💡 Pro Tips

### Before Presentation:
1. ✅ Test on presentation computer
2. ✅ Have backup screenshots
3. ✅ Know how to restart quickly
4. ✅ Practice with tech issues
5. ✅ Stay calm if things break

### During Presentation:
1. ✅ If lag, switch to 2D
2. ✅ If crash, restart calmly
3. ✅ If fail, use screenshots
4. ✅ Keep talking while fixing
5. ✅ Focus on concept, not tech

### After Issue:
1. ✅ Don't apologize excessively
2. ✅ Move on quickly
3. ✅ Emphasize what works
4. ✅ Show confidence
5. ✅ Finish strong

---

## 🎯 Confidence Mantras

When tech fails:
- "The concept is what matters"
- "Judges understand tech issues"
- "My idea is still unique"
- "I can explain it clearly"
- "This won't stop me from winning"

---

## 📱 Contact Info (For Help)

### If You Need Help:

1. **Check this guide first**
2. **Run test_dashboard.py**
3. **Google the error message**
4. **Check Streamlit docs**: docs.streamlit.io
5. **Check Plotly docs**: plotly.com/python

### Common Resources:
- Streamlit Forum: discuss.streamlit.io
- Stack Overflow: stackoverflow.com
- Plotly Community: community.plotly.com

---

## ✅ Final Checklist

Before presenting, verify:
- [ ] Dashboard starts without errors
- [ ] All 5 tabs load correctly
- [ ] 3D network rotates smoothly
- [ ] Simulation runs and animates
- [ ] Historical playback works
- [ ] Download button functions
- [ ] Colors display correctly
- [ ] No console errors
- [ ] Tested on presentation computer
- [ ] Backup screenshots ready

---

## 🏆 Remember

**Technology can fail. Your idea can't.**

Even if the dashboard doesn't work perfectly:
- Your concept is unique
- Your analysis is solid
- Your insights are valuable
- Your presentation is practiced
- You can still win!

**Stay calm. Stay confident. You've got this!** 💪

---

*"The best preparation for tomorrow is doing your best today."*

**GO WIN THAT HACKATHON! 🚀🏆**
