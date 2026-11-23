# Crypto Exchange | Operational Risk Management System

**A Python-based operational risk management and monitoring application for a simulated cryptocurrency exchange.**

This self-directed project demonstrates the design and implementation of an integrated operational risk framework covering risk identification, assessment, control testing, key risk indicators, incident management, early warning signals and executive risk reporting.

Built with Python, Pandas and Streamlit.

> **Disclaimer:** All scenarios, financial losses, thresholds and control assessments are synthetic. This application is a portfolio demonstration, not a production risk management system or evidence of regulatory compliance.

## Core Features

### 1. Risk Register & RCSA
- 15 crypto-specific operational risk scenarios
- Inherent and residual risk scoring using a 5×5 likelihood-impact matrix
- Coverage of wallet custody, withdrawals, trading infrastructure, cybersecurity, reconciliation, third-party dependencies, financial crime operations and business continuity
- Risk ownership and remediation actions

### 2. Control Effectiveness Assessment
- Control design effectiveness assessment
- Operating effectiveness testing
- Evidence availability tracking
- Identification of failed controls and assessments awaiting assurance
- Identification of risks requiring reassessment following control failures

### 3. Control Testing Workspace
- Interactive selection and assessment of individual controls
- Updating control effectiveness, evidence status and test findings
- Saving assessments and recalculating dashboard indicators
- Demonstration of the control assurance workflow

### 4. Key Risk Indicators (KRIs)
- Monitoring of operational risk indicators
- Configurable amber and red thresholds through the input dataset
- Automated GREEN, AMBER and RED classification
- Risk-specific indicator mapping

### 5. Early Warning System
- Integration of KRI breaches and control assessment results
- Identification of critical alerts, high alerts and warnings
- Escalation signals for management attention
- Prioritization of risks requiring intervention

### 6. Incident & Loss Management
- Incident register with severity and status
- Operational loss-event monitoring
- Gross loss, recovery and net loss calculations
- Loss analysis by operational risk process

### 7. Executive Risk Dashboard
- Registered risks and critical residual exposures
- RED KRIs and failed controls
- Open incidents and operational losses
- Risk exposure analysis by process
- Management attention and remediation priorities

## Risk Assessment Methodology

Likelihood and impact are assessed on illustrative ordinal scales from 1 to 5.

**Risk Score = Likelihood × Impact**

| Score | Classification |
|---|---|
| 1–4 | Low |
| 5–9 | Moderate |
| 10–14 | High |
| 15–25 | Critical |

Residual likelihood and impact are illustrative expert assumptions. They are not mechanically derived from control effectiveness.

Control failures and insufficient testing evidence are flagged for reassessment rather than treated as validated reductions in risk.

KRI thresholds use greater-than-or-equal-to comparisons (`>=`). These thresholds are illustrative and would require calibration against actual operating data and approved risk appetite.

## Technology Stack

- Python
- Pandas
- Streamlit
- Matplotlib
- CSV-based synthetic datasets

## Installation

Clone the repository and install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Project Data

The application uses synthetic CSV datasets:

- `risk_register.csv`
- `kri_observations.csv`
- `control_tests.csv`
- `incidents.csv`

No live exchange data, customer records or confidential information are required.

## Limitations & Future Development

This application is an illustrative prototype. It does not implement a complete production-grade governance or operational risk infrastructure.

Potential future enhancements include:

1. Historical KRI time-series analysis and trend monitoring
2. Formal approval workflows and immutable audit trails
3. Risk appetite limits and escalation policies
4. Extended incident lifecycle and root-cause analysis
5. Regulatory and industry framework mapping
6. Database integration and role-based access controls

## Portfolio Context

This project was independently developed to demonstrate practical operational risk management concepts and Python-based risk analytics within a cryptocurrency exchange environment.

It combines quantitative risk analysis with operational risk governance concepts, including RCSA, control assurance, KRI monitoring, incident management and management reporting.

**Project type:** Independent portfolio simulation  
**Industry focus:** Cryptocurrency exchanges / Digital assets  
**Primary domain:** Operational Risk Management

## Live Demo

**[Launch the Operational Risk Management Dashboard](https://crypto-operational-risk.streamlit.app/)**

The application demonstrates an integrated operational risk framework for a fictional cryptocurrency exchange.

Features include RCSA, control effectiveness testing, KRI monitoring, early warning indicators, incident and loss management, and executive risk reporting.

All data and scenarios are synthetic. The public demo is read-only; control assessment changes are disabled.
