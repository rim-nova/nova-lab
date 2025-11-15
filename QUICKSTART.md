# Quick Start Guide - InfinityInsight

## 🚀 Super Simple Installation (2 Steps!)

### Step 1: Clone the Repository

```bash
git clone https://github.com/rim-nova/nova-lab.git
cd nova-lab
```

### Step 2: Run the Installer

```bash
chmod +x install.sh
./install.sh
```

**That's it!** Choose option 1 (Docker) or 2 (Local) and follow the prompts.

---

## 🎯 Using Docker (Easiest - Recommended)

**Requirements:** Docker & Docker Compose installed

```bash
# Run installer and choose option 1
./install.sh

# Services start automatically at:
# ✓ Backend:  http://localhost:8000
# ✓ Frontend: http://localhost:3000
# ✓ API Docs: http://localhost:8000/docs
```

**Commands:**
```bash
docker-compose logs -f        # View logs
docker-compose down           # Stop
docker-compose up -d          # Start
```

---

## 💻 Local Installation

**Requirements:** Python 3.11+, Node.js 18+ (optional for frontend)

```bash
# Run installer and choose option 2
./install.sh

# After installation, start backend:
source venv/bin/activate
python -m uvicorn backend.app.main:app --reload

# In another terminal, start frontend:
cd frontend
npm run dev
```

---

## 🎓 First Steps

### 1. Create Your Account

Visit `http://localhost:3000` and click "Register"

### 2. Upload Data

- Click "Upload Data" on dashboard
- Supports: CSV, Excel, SPSS, Stata, JSON, Parquet

### 3. Run Analysis

**Via UI:**
- Navigate to "Analyze" section
- Choose your test (t-test, ANOVA, regression, etc.)

**Via API (http://localhost:8000/docs):**
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "your@email.com", "password": "password"}
)
token = response.json()["access_token"]

# Upload dataset
files = {"file": open("data.csv", "rb")}
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/api/v1/datasets/upload",
    files=files,
    headers=headers
)

# Run analysis
dataset_id = response.json()["id"]
response = requests.post(
    "http://localhost:8000/api/v1/statistics/descriptives",
    json={
        "dataset_id": dataset_id,
        "variables": ["age", "income"],
        "include_plots": True
    },
    headers=headers
)
print(response.json())
```

---

## 📊 Available Analyses

### Statistical Tests
- ✅ Descriptive Statistics
- ✅ Frequencies & Crosstabs
- ✅ T-Tests (one-sample, independent, paired)
- ✅ ANOVA (one-way, factorial)
- ✅ Correlation (Pearson, Spearman, Kendall)
- ✅ Linear & Logistic Regression
- ✅ Factor Analysis
- ✅ Cluster Analysis
- ✅ Reliability Analysis
- ✅ Nonparametric Tests

### Machine Learning
- ✅ 10+ Algorithms (Random Forest, XGBoost, etc.)
- ✅ AutoML (automatic model selection)
- ✅ Classification & Regression
- ✅ Feature Importance
- ✅ Cross-validation

---

## ❓ Troubleshooting

### "Docker not found"
Install Docker: https://docs.docker.com/get-docker/

### "Python not found"
Install Python 3.11+: https://www.python.org/downloads/

### "Port already in use"
Change ports in `docker-compose.yml` or `.env` file

### Database errors
Default uses SQLite (no setup needed). For PostgreSQL, update `DATABASE_URL` in `.env`

---

## 🆘 Need Help?

- **Documentation:** [README.md](README.md) | [CLAUDE.md](CLAUDE.md)
- **API Docs:** http://localhost:8000/docs
- **Issues:** https://github.com/rim-nova/nova-lab/issues

---

## 🎉 You're Ready!

Start analyzing your data with the power of AI! 🚀
