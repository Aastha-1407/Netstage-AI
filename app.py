import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
from datetime import datetime

from core.rule_checker import DeterministicRuleChecker
from core.ai_diagnostician import AIDiagnostician

# Set App Configuration
st.set_page_config(page_title="NetSage AI - Network Troubleshooter", layout="wide", page_icon="🌐", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    :root { --ink: #e7f0ed; --muted: #82938e; --line: #223531; --paper: #07110f; --panel: #0d1a17; --teal: #71e1c1; --teal-dark: #103c35; --amber: #f5bd43; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] { background: #0b1714; border-right: 1px solid var(--line); }
    [data-testid="stSidebar"] * { color: #dceae5 !important; }
    [data-testid="stSidebar"] .stCaption { color: #82938e !important; }
    [data-testid="stSidebar"] hr { border-color: var(--line); }
    h1, h2, h3, h4, p, label, .stMarkdown { font-family: 'DM Sans', sans-serif; }
    h1 { letter-spacing: 0; font-weight: 700; color: var(--ink); }
    h2, h3 { color: var(--ink); }
    code, .stCode, [data-testid="stMetricValue"] { font-family: 'Space Mono', monospace; }
    [data-testid="stMetric"] { background: var(--panel); border: 1px solid var(--line); border-radius: 2px; padding: 0.8rem 1rem; }
    [data-testid="stMetricLabel"] { color: var(--muted); }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line); border-radius: 8px; }
    .page-kicker { color: var(--teal); font: 700 0.75rem 'Space Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: -0.45rem; }
    .page-subtitle { color: var(--muted); font-size: 1rem; margin-top: -0.6rem; margin-bottom: 1.5rem; }
    .status-chip { display: inline-block; background: #12362f; color: var(--teal) !important; border: 1px solid #245b4e; border-radius: 999px; padding: 0.3rem 0.7rem; font: 700 0.72rem 'Space Mono', monospace; }
    .command-header { display: flex; align-items: center; gap: 14px; border-bottom: 1px solid var(--line); padding: 0.4rem 0 1.2rem; margin-bottom: 1.1rem; }
    .brand-mark { background: var(--teal); color: #09211b; border-radius: 10px; font-size: 1.5rem; padding: 0.45rem 0.65rem; }
    .brand-name { font: 700 1.1rem 'Space Mono', monospace; letter-spacing: 0.06em; color: var(--ink); }
    .brand-meta { color: var(--muted); font: 0.68rem 'Space Mono', monospace; letter-spacing: 0.08em; margin-top: 0.2rem; }
    .dashboard-panel { background: var(--panel); border: 1px solid var(--line); padding: 1.25rem; min-height: 310px; }
    .panel-kicker { color: var(--teal); font: 700 0.75rem 'Space Mono', monospace; letter-spacing: 0.08em; text-transform: uppercase; }
    .panel-title { color: var(--ink); font-size: 1.35rem; font-weight: 700; margin: 0.45rem 0 1.4rem; }
    .domain-row { display: grid; grid-template-columns: 100px 1fr 30px; align-items: center; gap: 0.8rem; margin: 1rem 0; color: #c9d8d3; font-weight: 600; }
    .domain-track { height: 7px; background: #20352f; }
    .domain-fill { height: 100%; background: var(--teal); }
    .domain-count { color: var(--muted); text-align: right; font: 0.8rem 'Space Mono', monospace; }
    .queue-item { display: grid; grid-template-columns: 38px 1fr auto 18px; gap: 0.8rem; align-items: center; border-top: 1px solid var(--line); padding: 1rem 0; }
    .queue-icon { border: 1px solid #275048; color: var(--teal); font-size: 1.1rem; padding: 0.55rem; text-align: center; }
    .queue-meta { color: var(--muted); font: 0.68rem 'Space Mono', monospace; text-transform: uppercase; }
    .queue-title { color: var(--ink); font-weight: 700; margin-top: 0.3rem; }
    .severity { border: 1px solid #825f2b; color: var(--amber); font: 0.68rem 'Space Mono', monospace; padding: 0.45rem 0.6rem; }
    .queue-arrow { color: var(--muted); font-size: 1.25rem; }
    .dashboard-rule { border-top: 1px solid var(--line); margin: 1.6rem 0; }
    [data-testid="stDataFrame"] { border: 1px solid var(--line); border-radius: 8px; }
    .stButton > button[kind="primary"] { background: var(--teal); border-color: var(--teal); }
    .stButton > button[kind="primary"]:hover { background: var(--teal-dark); border-color: var(--teal-dark); }
</style>
""", unsafe_allow_html=True)

DATA_PATH = "data/cases.csv"
LOG_PATH = "data/review_log.csv"

REVIEW_COLUMNS = [
    "timestamp", "case_id", "symptom", "ai_fault", "ai_layer", 
    "human_verdict", "corrected_fault", "reviewer_notes"
]

if not os.path.exists("data"):
    os.makedirs("data")
# By Aryan
def load_reviews():
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        df = pd.DataFrame(columns=REVIEW_COLUMNS)
        df.to_csv(LOG_PATH, index=False)
        return df
    try:
        return pd.read_csv(LOG_PATH)
    except Exception:
        df = pd.DataFrame(columns=REVIEW_COLUMNS)
        df.to_csv(LOG_PATH, index=False)
        return df

def append_review(entry_dict):
    df = load_reviews()
    df = pd.concat([df, pd.DataFrame([entry_dict])], ignore_index=True)
    df.to_csv(LOG_PATH, index=False)

@st.cache_data
def load_cases():
    if os.path.exists(DATA_PATH) and os.path.getsize(DATA_PATH) > 0:
        try:
            return pd.read_csv(DATA_PATH)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()

df_cases = load_cases()

# ------------------- NAVIGATION ---------------------
diagnostician = AIDiagnostician()

st.markdown("""
<div class="command-header">
    <div class="brand-mark">⌘</div>
    <div><div class="brand-name">NETSAGE <span style="color:#71e1c1">AI</span></div><div class="brand-meta">PACKET TRACER&nbsp;&nbsp;/&nbsp;&nbsp; HUMAN-IN-THE-LOOP</div></div>
</div>
""", unsafe_allow_html=True)
mode = st.radio("Navigation", ["Troubleshooting Studio", "Responsible AI & Review Logs", "Case Repository"], horizontal=True, label_visibility="collapsed")

# ----------------- VIEW 1: STUDIO -----------------
if mode == "Troubleshooting Studio":
    df_logs = load_reviews()
    total_reviews = len(df_logs)
    accepted = len(df_logs[df_logs["human_verdict"] == "Accepted"]) if not df_logs.empty else 0
    corrections = len(df_logs[df_logs["human_verdict"].isin(["Edited", "Rejected"])]) if not df_logs.empty else 0
    agreement_rate = (accepted / total_reviews) * 100 if total_reviews else 0
    domain_counts = df_cases["concept_tag"].astype(str).value_counts().head(7) if not df_cases.empty else pd.Series(dtype=int)
    max_domain_count = int(domain_counts.max()) if not domain_counts.empty else 1

    st.markdown("<div class='page-kicker'>COMMAND CENTER / LIVE OVERVIEW</div>", unsafe_allow_html=True)
    st.title("Network operations at a glance")
    st.markdown("<div class='page-subtitle'>Diagnose Packet Tracer faults, monitor review health, and keep every decision accountable.</div>", unsafe_allow_html=True)

    metric_cols = st.columns(4)
    metrics = [
        ("LAB CASES", len(df_cases), "Across fault domains", "#e7f0ed"),
        ("REVIEWED", total_reviews, "Human decisions logged", "#71e1c1"),
        ("AGREEMENT", f"{agreement_rate:.1f}%", "AI / reviewer alignment", "#f5bd43"),
        ("CORRECTIONS", corrections, "Responsible AI records", "#ff8b78"),
    ]
    for column, (label, value, detail, color) in zip(metric_cols, metrics):
        with column:
            st.markdown(f"<div class='dashboard-panel' style='min-height:0'><div class='panel-kicker' style='color:#82938e'>{label}</div><div style='font:700 2.25rem DM Sans;color:{color};margin:0.8rem 0 0.35rem'>{value}</div><div style='color:#82938e;font-weight:600'>{detail}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='dashboard-rule'></div>", unsafe_allow_html=True)
    signal_col, queue_col = st.columns([1, 1.45])
    with signal_col:
        domain_html = "".join(
            f"<div class='domain-row'><span>{domain}</span><span class='domain-track'><span class='domain-fill' style='display:block;width:{max(8, int(count / max_domain_count * 100))}%'></span></span><span class='domain-count'>{count}</span></div>"
            for domain, count in domain_counts.items()
        ) or "<div style='color:#82938e'>No case data available.</div>"
        st.markdown(f"<div class='dashboard-panel'><div class='panel-kicker'>SIGNAL MAP</div><div class='panel-title'>Fault domains</div>{domain_html}</div>", unsafe_allow_html=True)
    with queue_col:
        queue_html = ""
        for _, row in df_cases.head(5).iterrows():
            severity = str(row.get("severity", "Medium")).upper()
            queue_html += f"<div class='queue-item'><div class='queue-icon'>⌁</div><div><div class='queue-meta'>{row['case_id']} &nbsp;·&nbsp; {row.get('concept_tag', 'NETWORK')}</div><div class='queue-title'>{row['symptom']}</div></div><div class='severity'>{severity}</div><div class='queue-arrow'>›</div></div>"
        if not queue_html:
            queue_html = "<div style='color:#82938e;padding:1rem 0'>No cases in the review queue.</div>"
        st.markdown(f"<div class='dashboard-panel'><div style='display:flex;justify-content:space-between'><div><div class='panel-kicker'>QUEUE SNAPSHOT</div><div class='panel-title'>Needs human review</div></div><div style='color:#71e1c1;font-weight:700'>View queue&nbsp; ›</div></div>{queue_html}</div>", unsafe_allow_html=True)

    st.markdown("<div class='dashboard-rule'></div>", unsafe_allow_html=True)
    st.markdown("<div class='page-kicker'>DIAGNOSTIC WORKSPACE</div>", unsafe_allow_html=True)
    st.subheader("Run a case diagnosis")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("01  Case input")
        case_options = ["Custom Lab Scenario"] + (df_cases["case_id"] + " - " + df_cases["symptom"]).tolist() if not df_cases.empty else ["Custom Lab Scenario"]
        selected_case = st.selectbox("Select Preset Lab Case", case_options)

        if selected_case != "Custom Lab Scenario" and not df_cases.empty:
            cid = selected_case.split(" - ")[0]
            row = df_cases[df_cases["case_id"] == cid].iloc[0]
            symptom_in = st.text_input("Symptom", value=str(row["symptom"]))
            topology_in = st.text_input("Topology / Note", value=str(row["topology_note"]))
            show_in = st.text_area("Show Command Outputs", value=str(row["show_outputs"]), height=200)
            expected_fault = str(row.get("expected_fault", "N/A"))
            current_case_id = cid
        else:
            symptom_in = st.text_input("Symptom", placeholder="e.g. PC cannot ping default gateway")
            topology_in = st.text_input("Topology / Note", placeholder="e.g. PC1 -> SW1 Fa0/1 -> R1 Gi0/0")
            show_in = st.text_area("Show Command Outputs", placeholder="Paste CLI output here...", height=200)
            expected_fault = "User Provided"
            current_case_id = f"CUSTOM-{datetime.now().strftime('%M%S')}"

        run_btn = st.button("🚀 Run Diagnosis", type="primary", use_container_width=True)

    with col2:
        st.subheader("02  Engine findings")
        
        if run_btn and symptom_in:
            with st.spinner("Analyzing rules and consulting AI engine..."):
                # Deterministic Rule Engine
                rule_findings = DeterministicRuleChecker.analyze(symptom_in, show_in, topology_in)
                st.session_state["rule_findings"] = rule_findings

                # AI Diagnosis
                ai_res = diagnostician.diagnose(symptom_in, topology_in, show_in)
                st.session_state["ai_result"] = ai_res
                st.session_state["current_case_data"] = {
                    "case_id": current_case_id,
                    "symptom": symptom_in,
                    "expected_fault": expected_fault
                }

        if "ai_result" in st.session_state:
            ai_res = st.session_state["ai_result"]
            findings = st.session_state.get("rule_findings", [])

            # Rule Checker Alerts
            if findings:
                st.warning(f"⚠️ Deterministic Rule Checker found {len(findings)} syntax/state rule violation(s):")
                for f in findings:
                    st.markdown(f"- **{f['rule']}** (Layer {f['osi_layer']}): {f['evidence']}. *Action: {f['recommendation']}*")
            else:
                st.success("✅ Deterministic Rule Checker: No basic syntax/status anomalies detected.")

            # AI Diagnosis Box
            st.markdown("---")
            st.markdown(f"#### AI Root Cause: **{ai_res.get('root_cause')}**")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("OSI Layer", f"Layer {ai_res.get('osi_layer', 3)}")
            m2.metric("Confidence", ai_res.get("confidence", "Medium"))
            m3.metric("Case ID", st.session_state["current_case_data"]["case_id"])

            st.markdown("**Evidence Cited from CLI:**")
            for ev in ai_res.get("evidence", []):
                st.info(f"🔎 `{ev}`")

            st.markdown("**Remediation CLI Commands:**")
            commands = "\n".join(ai_res.get("remediation_steps", []))
            st.code(commands if commands else "No script generated", language="cisco")

            # ----------------- HUMAN REVIEW CARD --------------------------
            st.markdown("---")
            st.subheader("03  Human review")
            with st.form("human_review_form"):
                verdict = st.radio("Decision", ["Accepted", "Edited", "Rejected"], horizontal=True)
                corr_fault = st.text_input("Corrected Fault (if Edited/Rejected)", value=ai_res.get("root_cause") if verdict == "Accepted" else "")
                notes = st.text_area("Reviewer Audit Notes / Reason for Change", placeholder="Explain why AI diagnosis was modified or approved...")
                submit_review = st.form_submit_button("💾 Commit Human Review to Log")

                if submit_review:
                    log_entry = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "case_id": st.session_state["current_case_data"]["case_id"],
                        "symptom": st.session_state["current_case_data"]["symptom"],
                        "ai_fault": ai_res.get("root_cause"),
                        "ai_layer": ai_res.get("osi_layer"),
                        "human_verdict": verdict,
                        "corrected_fault": corr_fault,
                        "reviewer_notes": notes
                    }
                    append_review(log_entry)
                    st.success("Human review logged successfully!")

# ----------------- VIEW 2: RESPONSIBLE AI LOGS -----------------
elif mode == "Responsible AI & Review Logs":
    st.markdown("<div class='page-kicker'>02 / Governance</div>", unsafe_allow_html=True)
    st.title("Review & Agreement")
    st.markdown("<div class='page-subtitle'>A compact audit trail for model decisions, corrections, and reviewer confidence.</div>", unsafe_allow_html=True)

    df_logs = load_reviews()
    if not df_logs.empty and len(df_logs) > 0:
        total_reviews = len(df_logs)
        accepted = len(df_logs[df_logs["human_verdict"] == "Accepted"])
        edited = len(df_logs[df_logs["human_verdict"] == "Edited"])
        rejected = len(df_logs[df_logs["human_verdict"] == "Rejected"])
        agreement_rate = (accepted / total_reviews) * 100 if total_reviews > 0 else 0

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Total Reviewed", total_reviews)
        k2.metric("Accepted As-Is", accepted)
        k3.metric("Intervened (Edit/Reject)", edited + rejected)
        k4.metric("AI-Human Agreement", f"{agreement_rate:.1f}%")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_pie = px.pie(df_logs, names="human_verdict", title="Review Decisions Breakdown", color="human_verdict",
                             color_discrete_map={"Accepted": "#2ecc71", "Edited": "#f39c12", "Rejected": "#e74c3c"})
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_g2:
            fig_bar = px.histogram(df_logs, x="ai_layer", color="human_verdict", title="Verdicts Across OSI Layers",
                                   category_orders={"ai_layer": [1, 2, 3, 4, 5, 6, 7]})
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("Responsible AI Audit Log")
        st.dataframe(df_logs.sort_values(by="timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No reviews recorded yet. Run diagnostics in the Studio and submit reviews to create records.")

# ----------------- VIEW 3: CASE REPOSITORY -----------------
elif mode == "Case Repository":
    st.markdown("<div class='page-kicker'>03 / Reference library</div>", unsafe_allow_html=True)
    st.title("Case Repository")
    st.markdown(f"<div class='page-subtitle'>Browse {len(df_cases)} pre-configured Packet Tracer troubleshooting scenarios.</div>", unsafe_allow_html=True)

    if not df_cases.empty:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            layers = [int(x) for x in df_cases["osi_layer"].dropna().unique()]
            filter_layer = st.multiselect("Filter by OSI Layer", options=sorted(layers))
        with col_f2:
            tags = [str(x) for x in df_cases["concept_tag"].dropna().unique()]
            filter_tag = st.multiselect("Filter by Concept Tag", options=sorted(tags))

        filtered = df_cases.copy()
        if filter_layer:
            filtered = filtered[filtered["osi_layer"].isin(filter_layer)]
        if filter_tag:
            filtered = filtered[filtered["concept_tag"].isin(filter_tag)]

        st.dataframe(filtered, use_container_width=True)

#finished
