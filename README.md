# 🛒 ThreadFlip: Data Product Management Portfolio

Welcome to my Data Product Management portfolio. This repository contains a comprehensive, end-to-end product strategy and technical implementation for **ThreadFlip**, a simulated C2C fashion marketplace (modeled after apps like Vinted and Depop). 

- **The Product Challenge:** Marketplace liquidity was stagnating due to high cart abandonment caused by individual shipping fees. 
- **The Solution:** A "Smart Bundle & Liquidity" Machine Learning Engine that dynamically incentivizes multi-item purchases from the same seller.

This project demonstrates my ability to bridge the gap between business strategy, data engineering, and user experience.

---

## 🛠️ The Tech Stack
* **Product Strategy:** Notion (PRDs, User Personas, Roadmapping)
* **Data Warehousing & SQL:** Google BigQuery (Public Dataset: `thelook_ecommerce`)
* **Experimentation & Analytics:** Python (Polars, Plotly, SciPy)
* **Prototyping & ROI Modeling:** Streamlit, FPDF2

---

## 📂 Project Architecture

This project is broken down into 6 distinct Data PM phases. You can navigate through the repository using the links below:

### [Phase 1: Product Requirement Document (PRD)](https://www.notion.so/Product-Requirement-Document-365d64d8b6e38096b7befaad1b204217?source=copy_link)
* **What it is:** The foundational strategy document outlining the problem, user personas, and target KPIs (Marketplace Liquidity Rate, AOV).
* **PM Skill Demonstrated:** Stakeholder alignment, defining business outcomes over technical outputs, and establishing North Star metrics.

### [Phase 2: Quantitative Product Diagnostics](./Product-Queries)
* **What it is:** 8 advanced SQL queries diagnosing marketplace health, identifying "Power Sellers," cohort retention mapping, and funnel abandonment analysis.
* **PM Skill Demonstrated:** Advanced data retrieval (CTEs, Window Functions, JOINs) to validate product hypotheses without relying on engineering bandwidth.

### [Phase 3: A/B Testing & Statistical Validation](./Product_Metrics_ThreadFlip.ipynb)
* **What it is:** A Google Colab notebook simulating a 10,000-user A/B test for the new Smart Bundle UI, evaluated using Polars for aggregation and Chi-Square testing for statistical significance.
* **PM Skill Demonstrated:** Experimentation design, defining minimum detectable effects, and translating $p$-values into actionable product launch decisions.

### [Phase 4: Live ROI & Feature Validation Dashboard](https://threadflip-j5gxcyxmg2uxnd2xad8dag.streamlit.app/)
* **What it is:** A deployed Streamlit application featuring live unit economics modeling (ARPU & CLV), qualitative user feedback analysis via Word Clouds, and automated PDF strategy generation.
* **PM Skill Demonstrated:** Connecting technical features directly to top-line revenue impact, and building self-serve tooling for business stakeholders. *(Source code available in `app.py`)*.

### Phase 5: Data Contracts & ML Feedback Loops (See below)
* **What it is:** The JSON schema defining front-end telemetry, the ML objective function maximizing Cart Value (constrained by size matching), and the "Cold Start" mitigation strategy.
* **PM Skill Demonstrated:** Translating business requirements into strict technical data contracts for front-end and machine learning engineering teams.

### Phase 6: Launch Strategy & Data Operations (See below)
* **What it is:** A phased rollout plan (Dark Launch → Dogfooding → Canary → GA), Data SLAs defining acceptable latency/freshness, and GDPR compliance parameters for model training.
* **PM Skill Demonstrated:** Risk mitigation, operational excellence, and protecting company revenue during algorithm deployment.

---

## 🔍 Deep Dive: Phase 5 & 6 Highlights

### The Telemetry Data Contract (JSON)
To ensure clean data ingestion for the ML model, the front-end must adhere to this exact schema upon feature interaction:

```json
{
  "event_name": "bundle_recommendation_rendered",
  "timestamp": "2026-05-20T10:34:45Z",
  "user_id": "u_847593",
  "context": {
    "anchor_product_id": "p_1001",
    "seller_id": "s_5542"
  },
  "recommendations_shown": [
    {
      "product_id": "p_8832",
      "algorithm_version": "v1.2_collaborative",
      "size_match_score": 0.95
    }
  ]
}
```

### 📊 Defined Data Service Level Agreements (SLAs)

To ensure a seamless user experience and reliable experimentation, the engineering and data teams are held to the following SLAs for the Smart Bundle Engine:

| SLA Metric | Definition | Target Threshold | Breach Protocol |
| :--- | :--- | :--- | :--- |
| **API Latency** | Time taken for the ML algorithm to return bundle recommendations to the front-end. | < 200 milliseconds | **Critical.** UI lag causes cart abandonment. Front-end automatically falls back to standard UI. |
| **Completeness** | Percentage of checkout events successfully logging the `is_bundle` boolean flag. | 99.9% | **High.** Corrupts A/B test tracking. Automated Slack alert triggered to Data Engineering on-call. |
| **Freshness** | Maximum delay between a seller listing a new item and it being available in the recommendation pool. | < 5 minutes | **Medium.** Recommendation pool is slightly stale. Monitored during weekly sprint review. |
| **Availability** | Overall uptime of the recommendation API service during peak traffic hours. | 99.95% | **Critical.** Automated failover to the Phase 1 "Cold Start" content-based filtering model. |

