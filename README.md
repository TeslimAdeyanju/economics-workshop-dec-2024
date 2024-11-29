# Economic Data Dashboard
**🚀 Try the live dashboard: [Economics Dashboard on Streamlit Cloud](https://economics-workshop-dec-2024.streamlit.app/)**

<p align="center">
  <img src="static/images/dashboard_preview.png" alt="Economic Data Dashboard Preview" width="900"/>
  <br>
  <em>Economic Indicators Dashboard showing unemployment rate trends and analysis</em>
</p>

A comprehensive economic data dashboard that combines data from multiple sources (Yahoo Finance, FRED) into a Streamlit application with automated data collection and visualization.

## Introduction

Hi, I'm **Ivan Brigida**, an Analyst at Google with a background in **Economics** and **Data Analysis**. Before joining Google, I worked in the banking sector, and 3 years ago, I started investing in **U.S. markets** while living in **Ireland**. My work and investing experience focus on using **economic data** to understand the economy, make financial decisions, and develop market strategies. You can read more about my approach in my [blog post about macro indicators affecting the stock market](https://pythoninvest.com/long-read/macro-indicators-affecting-stock-market).

Last year, I ran the **[Stock Markets Analysis Zoomcamp](https://pythoninvest.com/course)**, which attracted **1,800+ registrations**. I'll be running it again in **2025**, you can express your interest here:

<p align="center">
  <a href="https://pythoninvest.com/course"><img src="https://user-images.githubusercontent.com/875246/185755203-17945fd1-6b64-46f2-8377-1011dcb1a444.png" height="50" /></a>
</p>

---

### My Skills and Motivation

I'm skilled in:
- Writing **SQL code** for analysis and workflows.
- Building **graphs** and conducting data-driven analysis.
- Creating **basic trading strategies**, though they can get complex.

However, I want to avoid the overhead of tasks like:
- Managing **data pipelines** and **databases**.
- Ensuring **data integrity**.
- Coding **dashboards**, debugging **JavaScript**, or dealing with **CSS styles**.
- Handling **containerization** and deployment.

AI tools have helped me bridge these gaps, saving time and energy (at <$20/month). I'm focusing on what I do best while letting technology handle the rest.

---

### The Grand Idea 💡

This repository is a step toward a **generic Data Science project template** with solid foundational layers:
1. **Data storage** and **automated updates** for reliable, scalable data handling.
2. **Dashboards** for visualization and monitoring.
3. **Containers** for streamlined deployment.

With these pieces in place, the real focus can shift to **predictions**, **machine learning**, and advanced strategy development—what really matters for understanding markets and making decisions.

## Features
- Real-time cryptocurrency data collection
- Daily economic indicators updates
- Interactive visualizations
- Professional dark theme UI
- Containerized deployment
- Automated data collection via cron jobs
- SQLite database for data storage
- Health monitoring and logging

## Project Structure
```
.
├── app.py                      # Streamlit application
├── utils.py                    # Shared utilities (DB, data loading, chart styling)
├── data/                       # Data directory
│   └── economics_data.db       # SQLite database
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── btc_minute_data.py     # Cryptocurrency data collection
│   ├── daily_job.sh           # Daily collection script
│   ├── fred_data_retrieval.py # Economic data collection
│   └── minute_job.sh          # Minute collection script
├── pages/                      # Dashboard pages
│   ├── economic_indicators.py  # Economic indicators page
│   ├── stock_market.py        # Stock market analysis
│   ├── interest_rates.py      # Interest rates page
│   ├── currency_markets.py    # Currency markets page
│   └── crypto_markets.py      # Cryptocurrency markets page
├── static/
│   └── css/
│       └── style.css          # Application styling
└── README.md                  # Project documentation
```

## Project Reproduction
For detailed instructions on how to reproduce this project from scratch using AI-assisted development, see [REPRODUCTION.md](REPRODUCTION.md).

## Quick Start

### Docker Deployment (Recommended)

#### Option 1: With Persistent Data (Volume Mounting)
Use this option to persist data between container restarts:
```bash
# Run this before, if you want to rebuild the container that is currently running:
docker stop finance_test && docker rm finance_test

# Then run the container:
docker build -t data_app .
docker run -d --name finance_test -p 8501:8501 -v $(pwd)/data:/app/data data_app
```
This will use existing data if available, or create new data if the directory is empty.

#### Option 2: Without Volume Mounting
Use this option for a fresh start or testing (e.g., when developing a new version):
```bash
# Run this before, if you want to rebuild the container that is currently running:
docker stop finance_test && docker rm finance_test

# Then run the container:
docker build -t data_app .
docker run -d --name finance_test -p 8501:8501 data_app
```
This will automatically run initial data collection on startup since no existing data is mounted.

### Verifying Initial Data Collection
After running the container for the first time, you can verify data collection:

1. Check data collection logs:
```bash
docker exec finance_test tail -f /var/log/cron.log
```
This will show the progress of initial data collection for both daily and minute data.

2. Verify collected data:
```bash
# Check BTC minute data
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT datetime, close, volume FROM btc_minute ORDER BY datetime DESC LIMIT 5;"

# Check daily economic data (e.g., SP500)
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT date, sp500, sp500_returns_daily FROM sp500 ORDER BY date DESC LIMIT 5;"
```

### Accessing the Dashboard
Access the dashboard at http://localhost:8501

### Managing Data Collection

1. To manually trigger data collection jobs:
```bash
# Run daily job
docker exec finance_test /app/scripts/daily_job.sh

# Run minute job
docker exec finance_test /app/scripts/minute_job.sh
```

2. Monitor logs:
```bash
# View cron job logs
docker exec finance_test tail -f /var/log/cron.log

# View container logs
docker logs finance_test

# Check data collection status
docker exec finance_test sqlite3 /app/data/economics_data.db "SELECT COUNT(*) FROM btc_minute;"
```

### Local Development (Advanced)
Note: The scripts are designed to run within the Docker container. For local development:

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

3. For data collection, it's recommended to use the Docker container as it handles all the necessary environment setup and scheduling.



## Cloud Deployment Options

### 1. Streamlit Community Cloud (Current Demo, easiest)
This option is perfect for demos and simple deployments. The data will be static but it's free and easy to set up.

> [!NOTE]
> The [live demo](https://economics-workshop-dec-2024.streamlit.app/) runs on Streamlit Community Cloud.


### Steps:
1. Fork this repository to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your forked repository
6. Set main branch and app path to `app.py`
7. Click "Deploy"

Your app will be available at `https://[your-app-name].streamlit.app`

Note: The Community Cloud version will have static data. For dynamic updates, consider:
- Setting up GitHub Actions for periodic data collection
- Using external databases instead of local SQLite
- Implementing API-based data fetching



### 2. Cloud Platform Deployment (Full Control)

### Digital Ocean (Recommended for Beginners)

Digital Ocean offers a good balance of simplicity and control.

1. Create account at [digitalocean.com](https://m.do.co/c/bb21d245e296). (This is a referral link by Ivan: you will have $200 in credit over 60 days)
2. Install Docker on your machine
3. Build and push container:
```bash
docker build -t data_app .
docker tag data_app registry.digitalocean.com/your-registry/data_app
docker push registry.digitalocean.com/your-registry/data_app
```
4. Deploy via App Platform or Droplet
5. Set up volumes for data persistence

Cost: Starting at ~$5/month

### 3. AWS/GCP/Azure (Enterprise)
For full control and scalability, use major cloud providers.

Example using AWS:
1. Create AWS account
2. Install AWS CLI
3. Push to ECR:
```bash
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
docker tag data_app aws_account_id.dkr.ecr.region.amazonaws.com/data_app
docker push aws_account_id.dkr.ecr.region.amazonaws.com/data_app
```
4. Deploy using ECS or EKS
5. Set up EFS for data persistence

Cost: Starting at ~$20/month

## Cloud Deployment Comparison

### Streamlit Community Cloud
✅ Free
✅ Easy setup
✅ Good for demos
❌ Static data only
❌ Limited control

### Digital Ocean
✅ Simple pricing
✅ Good documentation
✅ Moderate control
✅ Data persistence
❌ Basic monitoring

### AWS/GCP/Azure
✅ Full control
✅ Enterprise features
✅ Advanced monitoring
✅ Auto-scaling
❌ Complex setup
❌ Higher cost

Choose based on your needs:
- Demo/Portfolio: Use Streamlit Cloud
- Small Project: Use Digital Ocean
- Enterprise/Production: Use AWS/GCP/Azure
