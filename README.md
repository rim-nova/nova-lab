# InfinityInsight (NovaLab) - AI-Powered Analytics Platform

**Transform data into insights with the power of AI**

InfinityInsight is a comprehensive, modern analytics platform that combines the power of traditional statistical analysis (SPSS-equivalent) with cutting-edge machine learning and natural language interfaces. Built with Python (FastAPI) and Vue.js, it provides an intuitive, beautiful interface for data scientists, analysts, and researchers.

## 🌟 Key Features

### Comprehensive Statistical Analysis
- **Descriptive Statistics** - Frequencies, descriptives, explore
- **Bivariate Analysis** - T-tests, ANOVA, correlation, crosstabs
- **Regression** - Linear, logistic, multinomial regression with diagnostics
- **Advanced Methods** - Factor analysis, cluster analysis, reliability analysis
- **Nonparametric Tests** - Mann-Whitney, Wilcoxon, Kruskal-Wallis

### Machine Learning & AutoML
- **Supervised Learning** - Classification and regression with 10+ algorithms
- **AutoML** - Automatic model selection and hyperparameter tuning
- **Model Management** - Save, load, and deploy trained models
- **Explainability** - Feature importance and model diagnostics

### Data Management
- **Multi-Format Support** - CSV, Excel, SPSS (.sav), Stata, JSON, Parquet
- **Data Profiling** - Automatic EDA and data quality reports
- **Transformations** - Missing data handling, scaling, encoding, outlier detection
- **Connections** - Database and cloud storage support

### Natural Language Interface
- **Chat with Data** - Ask questions in plain English
- **Smart Insights** - AI-powered recommendations and interpretations
- **Report Generation** - Automatic analysis reports

### Modern UI/UX
- **Beautiful Dashboard** - Clean, intuitive interface built with Vue.js
- **Interactive Visualizations** - Powered by Chart.js and Plotly
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Mode Support** - Easy on the eyes

## 🚀 Quick Start (One-Click Installation)

### Option 1: Docker (Recommended - Easiest)

```bash
# Clone the repository
git clone https://github.com/rim-nova/nova-lab.git
cd nova-lab

# Run the one-click installation script
chmod +x install.sh
./install.sh
# Choose option 1 for Docker installation

# Services will be available at:
# - Backend API: http://localhost:8000
# - API Documentation: http://localhost:8000/docs
# - Frontend: http://localhost:3000
```

### Option 2: Local Installation

```bash
# Clone and run installation script
git clone https://github.com/rim-nova/nova-lab.git
cd nova-lab
chmod +x install.sh
./install.sh
# Choose option 2 for local installation
```

## 📋 Prerequisites

### For Docker Installation:
- Docker 20.10+
- Docker Compose 2.0+
- That's it! 🎉

### For Local Installation:
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+ (or use SQLite)
- Redis 6+ (optional)

## 🛠️ Manual Installation

### Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start server
python -m uvicorn backend.app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **Development Guide**: See [CLAUDE.md](CLAUDE.md)
- **Architecture**: Clean, modular, class-based design

## 🎯 Usage Examples

### Via Python SDK (coming soon)

```python
from infinityinsight import Client

client = Client(api_key="your-key")

# Upload and analyze
dataset = client.datasets.upload("data.csv")
profile = client.datasets.profile(dataset.id)

# Run t-test
results = client.statistics.ttest(
    dataset_id=dataset.id,
    dependent_var="score",
    test_type="independent"
)
```

### Via Natural Language

```
"Run descriptive statistics on age, income, and education"
"Compare sales between regions using ANOVA"
"Build a churn prediction model"
"Show correlation heatmap"
```

## 🏗️ Architecture

```
nova-lab/
├── backend/              # Python FastAPI backend
│   └── app/
│       ├── api/         # REST API endpoints
│       ├── core/        # Configuration & security
│       ├── models/      # SQLAlchemy models
│       ├── schemas/     # Pydantic schemas
│       └── services/    # Business logic (class-based)
│           ├── data/    # Data loading & profiling
│           ├── statistics/  # Statistical analysis
│           └── ml/      # Machine learning & AutoML
├── frontend/            # Vue.js 3 + Vite frontend
├── docker-compose.yml   # Easy deployment
└── install.sh          # One-click installer
```

## 🔒 Security

- JWT authentication
- Role-based access control
- Encrypted data storage
- HTTPS in production

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- IBM SPSS Statistics (feature reference)
- scikit-learn, statsmodels ecosystem
- Vue.js community

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/rim-nova/nova-lab/issues)
- **Documentation**: [CLAUDE.md](CLAUDE.md)

## 🗺️ Roadmap

- [x] Core statistical analysis (SPSS-equivalent)
- [x] Machine learning & AutoML
- [x] Data profiling & transformations
- [x] Modern Vue.js frontend
- [x] Docker deployment
- [ ] Natural language interface (OpenAI integration)
- [ ] Time series forecasting
- [ ] Survival analysis
- [ ] Real-time collaboration
- [ ] Mobile apps

---

**Made with ❤️ for the data science community**

*Empowering everyone to make data-driven decisions*
