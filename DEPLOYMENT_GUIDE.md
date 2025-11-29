# 🚀 Deployment Guide - The Deficit Domino Effect

## Quick Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Deficit Domino Effect Dashboard"

# Create repository on GitHub (github.com/new)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/deficit-domino-effect.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to **https://share.streamlit.io/**
2. Click **"New app"**
3. Connect your GitHub account
4. Select your repository: `deficit-domino-effect`
5. Set:
   - **Main file path:** `app.py`
   - **Python version:** 3.11
6. Click **"Deploy"**

**That's it!** Your dashboard will be live in 2-3 minutes.

---

## Alternative: Deploy to Heroku

### Prerequisites
```bash
# Install Heroku CLI
brew install heroku/brew/heroku  # Mac
# or download from heroku.com
```

### Files Needed

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Deploy
```bash
heroku login
heroku create deficit-domino-effect
git push heroku main
heroku open
```

---

## Alternative: Deploy to Render

1. Go to **https://render.com/**
2. Click **"New +"** → **"Web Service"**
3. Connect GitHub repository
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Click **"Create Web Service"**

---

## Environment Variables (if needed)

If you add any API keys or secrets later:

**Streamlit Cloud:**
- Go to app settings → Secrets
- Add in TOML format

**Heroku:**
```bash
heroku config:set API_KEY=your_key_here
```

**Render:**
- Go to Environment → Add Environment Variable

---

## Testing Before Deployment

```bash
# Test locally first
streamlit run app.py

# Check for errors
python -m py_compile app.py

# Run test suite
python test_dashboard.py
```

---

## Post-Deployment Checklist

- [ ] Dashboard loads without errors
- [ ] All 6 tabs work correctly
- [ ] Network visualization displays
- [ ] Contagion simulator runs
- [ ] Historical playback works
- [ ] Data loads properly
- [ ] Charts render correctly
- [ ] Mobile responsive (check on phone)

---

## Troubleshooting

### Issue: "Module not found"
**Solution:** Make sure `requirements.txt` is complete and pushed to GitHub

### Issue: "Port already in use"
**Solution:** Streamlit Cloud handles this automatically. For local, kill the process:
```bash
lsof -ti:8501 | xargs kill -9
```

### Issue: "Data file not found"
**Solution:** Make sure CSV file is in the repository and path is correct

### Issue: Slow loading
**Solution:** This is normal for first load. Subsequent loads are cached and fast.

---

## Custom Domain (Optional)

### Streamlit Cloud:
- Upgrade to paid plan
- Add custom domain in settings

### Heroku:
```bash
heroku domains:add www.your-domain.com
```

### Render:
- Go to Settings → Custom Domain
- Add your domain

---

## Monitoring & Analytics

### Streamlit Cloud:
- Built-in analytics in dashboard
- View usage, errors, performance

### Add Google Analytics (Optional):
Add to `app.py`:
```python
# Google Analytics
st.markdown("""
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
""", unsafe_allow_html=True)
```

---

## Sharing Your Dashboard

Once deployed, share the URL:
- **Streamlit Cloud:** `https://your-app-name.streamlit.app`
- **Heroku:** `https://deficit-domino-effect.herokuapp.com`
- **Render:** `https://deficit-domino-effect.onrender.com`

---

## For the Hackathon

**Recommended:** Use **Streamlit Cloud** (fastest, easiest, free)

**Steps:**
1. Push to GitHub (5 min)
2. Deploy to Streamlit Cloud (2 min)
3. Test the live URL (3 min)
4. Share URL with judges

**Total time:** 10 minutes! 🚀

---

## Quick Commands Reference

```bash
# Git commands
git status
git add .
git commit -m "Update dashboard"
git push

# Local testing
streamlit run app.py
python test_dashboard.py

# Kill local server
lsof -ti:8501 | xargs kill -9
```

---

## Support

If deployment fails:
1. Check GitHub Actions/logs
2. Verify requirements.txt
3. Test locally first
4. Check Streamlit Cloud logs

---

**You're ready to deploy! Good luck with the hackathon! 🏆**
