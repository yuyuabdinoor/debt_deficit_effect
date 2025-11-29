@echo off
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║     DEFICIT DOMINO EFFECT - SETUP SCRIPT                ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

echo 🔧 Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo 🧪 Running tests...
python test_dashboard.py

echo.
echo 🚀 To start the dashboard, run:
echo    streamlit run app.py
echo.
pause
