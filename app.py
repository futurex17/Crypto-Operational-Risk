import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Crypto Operational Risk', layout='wide')
st.title('Crypto Exchange | Operational Risk Management')
st.caption('Demonstration using synthetic scenarios; not a production risk assessment.')
base = Path(__file__).parent
risks = pd.read_csv(base / 'risk_register.csv')
kris = pd.read_csv(base / 'kri_observations.csv')

st.sidebar.header('Filters')
process = st.sidebar.multiselect('Process', sorted(risks.process.unique()), default=sorted(risks.process.unique()))
view = risks[risks.process.isin(process)].copy()
view['inherent_score'] = view.likelihood * view.impact
view['residual_score'] = view.residual_likelihood * view.residual_impact
kris['status'] = kris.apply(lambda x: 'RED' if x.observed_value >= x.red_threshold else ('AMBER' if x.observed_value > x.amber_threshold else 'GREEN'), axis=1)
c1, c2, c3, c4 = st.columns(4)
c1.metric('Registered risks', len(view))
c2.metric('High / critical residual risks', int((view.residual_score >= 15).sum()))
c3.metric('Open actions', int((view.action_status != 'Closed').sum()))
c4.metric('KRIs in breach', int((kris.loc[kris["kri_id"].isin(view["kri_id"]), "status"] == "RED").sum()))

st.subheader('Risk register & RCSA')
st.dataframe(view, use_container_width=True, hide_index=True)
st.caption('Illustrative 5×5 scoring: 1–4 Low, 5–9 Moderate, 10–14 High, 15–25 Critical. Scores are scenario assumptions, not empirical estimates.')

st.subheader('Key Risk Indicators')

st.dataframe(kris, use_container_width=True, hide_index=True)

st.subheader('Risk heatmap (residual)')
heat = pd.crosstab(view.residual_impact, view.residual_likelihood).reindex(index=range(5, 0, -1), columns=range(1, 6), fill_value=0)
st.dataframe(heat.style.background_gradient(cmap='YlOrRd', axis=None), use_container_width=True)
st.caption('Rows: impact 5→1; columns: likelihood 1→5; values: number of risks.')

st.subheader('Control assurance notes')
st.info('Residual assessments are provisional. Before accepting control effectiveness, collect design evidence, operating test results, exceptions and remediation records. A KRI breach triggers review; it does not automatically prove a loss event.')
# CONTROL EFFECTIVENESS ASSESSMENT

st.divider()
st.subheader("Control Effectiveness Assessment")

control_tests = pd.read_csv(base / "control_tests.csv")

control_assessment = view.merge(control_tests, on="control_id", how="left", validate="many_to_one")

def assess_control(row):
    if row["design_effectiveness"] == "Ineffective" or row["operating_effectiveness"] == "Ineffective":
        return "CONTROL FAILURE"

    if (row["design_effectiveness"] == "Effective" and row["operating_effectiveness"] == "Effective" and row["evidence_status"] == "Available"):
        return "ASSURED"

    return "ASSESSMENT PENDING"


control_assessment["assurance_status"] = control_assessment.apply(assess_control, axis=1)

a1, a2, a3 = st.columns(3)

a1.metric("Assured Controls", int((control_assessment.assurance_status == "ASSURED").sum()))
a2.metric("Control Failures", int((control_assessment.assurance_status == "CONTROL FAILURE").sum()))
a3.metric("Assessment Pending", int((control_assessment.assurance_status == "ASSESSMENT PENDING").sum()))

columns = ["risk_id", "risk_event", "control_id", "control_description", "design_effectiveness", "operating_effectiveness", "evidence_status", "assurance_status", "residual_score"]

st.dataframe(control_assessment[columns], width="stretch", hide_index=True)

st.warning("Residual risk scores are provisional until control design and operating effectiveness are supported by sufficient testing evidence.")
# INTERACTIVE CONTROL TESTING

st.divider()
st.subheader("Control Testing Workspace")

selected_control = st.selectbox("Select Control", control_tests["control_id"].tolist())

selected_row = control_tests[control_tests["control_id"] == selected_control].iloc[0]

design_options = ["Effective", "Ineffective", "Not assessed"]
operating_options = ["Effective", "Ineffective", "Not tested"]
evidence_options = ["Available", "Missing", "Insufficient"]

with st.form("control_test_form"):
    design = st.selectbox("Design Effectiveness", design_options, index=design_options.index(selected_row["design_effectiveness"]))
    operating = st.selectbox("Operating Effectiveness", operating_options, index=operating_options.index(selected_row["operating_effectiveness"]))
    evidence = st.selectbox("Evidence Status", evidence_options, index=evidence_options.index(selected_row["evidence_status"]))
    findings = st.text_area("Test Findings", value=str(selected_row["findings"]))
    submitted = st.form_submit_button("Save Assessment")

if submitted:
    control_tests.loc[control_tests["control_id"] == selected_control, "design_effectiveness"] = design
    control_tests.loc[control_tests["control_id"] == selected_control, "operating_effectiveness"] = operating
    control_tests.loc[control_tests["control_id"] == selected_control, "evidence_status"] = evidence
    control_tests.loc[control_tests["control_id"] == selected_control, "findings"] = findings
    control_tests.loc[control_tests["control_id"] == selected_control, "test_date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

    control_tests.to_csv(base / "control_tests.csv", index=False)
    st.success(f"Assessment saved for {selected_control}")
    st.rerun()
    
    # CONTROL FAILURE & RISK IMPACT ANALYSIS

st.divider()
st.subheader("Control Failure & Risk Impact Analysis")

latest_tests = pd.read_csv(base / "control_tests.csv")
risk_impact = view.merge(latest_tests, on="control_id", how="left", validate="many_to_one")

def risk_review_status(row):
    if row["operating_effectiveness"] == "Ineffective" or row["design_effectiveness"] == "Ineffective":
        return "REASSESSMENT REQUIRED"
    if row["design_effectiveness"] == "Effective" and row["operating_effectiveness"] == "Effective" and row["evidence_status"] == "Available":
        return "CONTROL ASSURED"
    return "ASSURANCE PENDING"

risk_impact["review_status"] = risk_impact.apply(risk_review_status, axis=1)

b1, b2, b3 = st.columns(3)
b1.metric("Risks Requiring Review", int((risk_impact.review_status == "REASSESSMENT REQUIRED").sum()))
b2.metric("Control Assured Risks", int((risk_impact.review_status == "CONTROL ASSURED").sum()))
b3.metric("Assurance Pending Risks", int((risk_impact.review_status == "ASSURANCE PENDING").sum()))

impact_columns = ["risk_id", "risk_event", "control_id", "inherent_score", "residual_score", "operating_effectiveness", "review_status", "action", "action_status"]

st.dataframe(risk_impact[impact_columns], width="stretch", hide_index=True)

failed_risks = risk_impact[risk_impact.review_status == "REASSESSMENT REQUIRED"]

if not failed_risks.empty:
    st.error(f"{len(failed_risks)} risk(s) require reassessment due to control effectiveness failures.")
else:
    st.info("No confirmed control failures in the current assessment data.")
    
 # KRI-RISK MAPPING & EARLY WARNING SYSTEM

st.divider()
st.subheader("KRI-Risk Mapping & Early Warning System")

kri_mapping = risk_impact.merge(kris[["kri_id", "indicator", "observed_value", "amber_threshold", "red_threshold", "status"]], on="kri_id", how="left", validate="many_to_one")

def early_warning(row):
    if pd.isna(row["status"]):
        return "DATA MISSING"
    if row["review_status"] == "REASSESSMENT REQUIRED" and row["status"] == "RED":
        return "CRITICAL ALERT"
    if row["review_status"] == "REASSESSMENT REQUIRED" or row["status"] == "RED":
        return "HIGH ALERT"
    if row["status"] == "AMBER":
        return "WARNING"
    if row["review_status"] == "ASSURANCE PENDING":
        return "MONITOR - UNVERIFIED"
    return "NORMAL"

kri_mapping["early_warning"] = kri_mapping.apply(early_warning, axis=1)

e1, e2, e3 = st.columns(3)
e1.metric("Critical Alerts", int((kri_mapping.early_warning == "CRITICAL ALERT").sum()))
e2.metric("High Alerts", int((kri_mapping.early_warning == "HIGH ALERT").sum()))
e3.metric("Warnings", int((kri_mapping.early_warning == "WARNING").sum()))

warning_columns = ["risk_id", "risk_event", "kri_id", "indicator", "observed_value", "amber_threshold", "red_threshold", "status", "review_status", "early_warning"]

st.dataframe(kri_mapping[warning_columns], width="stretch", hide_index=True)

critical_alerts = kri_mapping[kri_mapping.early_warning == "CRITICAL ALERT"]

if not critical_alerts.empty:
    st.error(f"{len(critical_alerts)} critical alert(s): Control failures coincide with RED KRI breaches.")
else:
     st.info("No combined critical alerts detected.")   
    
# INCIDENT & LOSS MANAGEMENT

st.divider()
st.subheader("Incident & Loss Management")

incidents = pd.read_csv(base / "incidents.csv")
incidents["incident_date"] = pd.to_datetime(incidents["incident_date"], errors="coerce")
incidents["gross_loss_usd"] = pd.to_numeric(incidents["gross_loss_usd"], errors="coerce").fillna(0)
incidents["recovery_usd"] = pd.to_numeric(incidents["recovery_usd"], errors="coerce").fillna(0)
incidents["net_loss_usd"] = incidents["gross_loss_usd"] - incidents["recovery_usd"]

incident_risks = incidents.merge(risks[["risk_id", "risk_event", "process"]], on="risk_id", how="left", validate="many_to_one")
# INCIDENT SUMMARY METRICS

i1, i2, i3, i4 = st.columns(4)

i1.metric("Total Incidents", len(incident_risks))
i2.metric("Gross Loss (USD)", f"${incident_risks['gross_loss_usd'].sum():,.0f}")
i3.metric("Recoveries (USD)", f"${incident_risks['recovery_usd'].sum():,.0f}")
i4.metric("Net Loss (USD)", f"${incident_risks['net_loss_usd'].sum():,.0f}")

# INCIDENT REGISTER

st.subheader("Incident Register")

incident_columns = ["incident_id", "incident_date", "risk_id", "risk_event", "incident_type", "severity", "gross_loss_usd", "recovery_usd", "net_loss_usd", "status", "owner", "corrective_action"]

st.dataframe(incident_risks[incident_columns], width="stretch", hide_index=True)

# LOSS DISTRIBUTION

st.subheader("Loss Distribution by Risk Process")

loss_by_process = incident_risks.groupby("process", dropna=False)["net_loss_usd"].sum().sort_values(ascending=False)

st.bar_chart(loss_by_process)

st.caption("All incidents and financial losses are synthetic demonstration data.")
# EXECUTIVE RISK DASHBOARD

st.divider()
st.header("Executive Risk Dashboard")
st.caption("Management overview | Synthetic operational risk scenarios")

total_risks = len(view)
critical_risks = int((view["residual_score"] >= 15).sum())

filtered_risk_ids = view["risk_id"].unique()
filtered_kris = kris[kris["kri_id"].isin(view["kri_id"])].copy()
filtered_risk_impact = risk_impact[risk_impact["risk_id"].isin(filtered_risk_ids)].copy()
filtered_incidents = incident_risks[incident_risks["risk_id"].isin(filtered_risk_ids)].copy()

red_kris = int((filtered_kris["status"] == "RED").sum())
failed_controls = int((filtered_risk_impact["review_status"] == "REASSESSMENT REQUIRED").sum())
open_incidents = int(filtered_incidents["status"].isin(["Open", "Under Investigation"]).sum())
net_loss = filtered_incidents["net_loss_usd"].sum()

st.subheader("Executive Risk Indicators")

m1, m2, m3 = st.columns(3)
m1.metric("Registered Risks", total_risks)
m2.metric("Critical Residual Risks", critical_risks)
m3.metric("RED KRIs", red_kris)

m4, m5, m6 = st.columns(3)
m4.metric("Failed Controls", failed_controls)
m5.metric("Open Incidents", open_incidents)
m6.metric("Net Operational Loss", f"${net_loss:,.0f}")

st.subheader("Risk Exposure by Process")

process_risk = view.groupby("process")["residual_score"].mean().sort_values(ascending=False)
st.bar_chart(process_risk)

st.subheader("Management Attention Required")

priority_risks = kri_mapping[kri_mapping["risk_id"].isin(filtered_risk_ids) & kri_mapping["early_warning"].isin(["CRITICAL ALERT", "HIGH ALERT"])].copy()
priority_columns = ["risk_id", "risk_event", "early_warning", "review_status", "status", "risk_owner", "action", "action_status"]

st.dataframe(priority_risks[priority_columns], width="stretch", hide_index=True)

st.subheader("Executive Summary")

st.write(f"Total registered risks: {total_risks}")
st.write(f"Critical residual risks: {critical_risks}")
st.write(f"RED KRI indicators: {red_kris}")
st.write(f"Controls requiring reassessment: {failed_controls}")
st.write(f"Open operational incidents: {open_incidents}")
st.write(f"Total net operational loss: ${net_loss:,.0f}")

st.warning("All risk scores, control assessments, incidents and financial losses are synthetic demonstration data. This dashboard is not a production risk assessment.")