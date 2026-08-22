# 🛰️ NetSage AI

## Evidence-First AI-Powered Network Troubleshooting Platform

> **Diagnose smarter. Validate with evidence. Keep humans in control.**

**[🚀 Try Live Demo](https://netstage-ai-eentie5da9xxb8bphmoxzj.streamlit.app/)**

NetSage AI is an AI-assisted network troubleshooting platform for **Cisco networking labs, Packet Tracer, CCNA learners, and junior engineers**. It combines **deterministic rule-based analysis, Generative AI, CLI evidence evaluation, and human-in-the-loop review** to transform network symptoms into explainable diagnoses.

---

## 🎯 The Problem

Network troubleshooting requires connecting multiple pieces of evidence to identify root causes:

- User-reported symptoms
- Network topology
- Cisco IOS configuration
- Routing tables, VLAN config, ACLs, NAT, DHCP, DNS

**The challenge:** Beginners don't know which commands to run, why they matter, or how to interpret results.

---

## ✨ Our Solution

NetSage AI provides a **structured diagnostic workflow**:

```
Network Evidence → Rule Analysis → AI Diagnosis → Human Review → Remediation → Verification
```

## Key Differentiators

✅ **Evidence-First Diagnosis** — AI uses only supplied evidence, never invents CLI output  
✅ **Hybrid AI + Rules** — Deterministic rule engine validates AI recommendations  
✅ **Human-in-the-Loop** — Every diagnosis can be accepted, edited, or rejected  
✅ **Explainable Output** — Root cause + Evidence + Next steps + Verification  
✅ **No Auto Execution** — AI recommendations only; humans apply changes  
✅ **Educational** — Teaches *why* problems occur, not just solutions  

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│     Streamlit User Interface        │
└────────────────┬────────────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────────┐      ┌──────────────────┐
│ Rule Engine  │      │ AI Diagnostician │
│(Deterministic│      │   (Gemini)       │
│ Networking)  │      └──────────────────┘
└──────────┬───┘              │
           └────────┬─────────┘
                    ▼
         ┌─────────────────────┐
         │ Structured Diagnosis│
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────┐
         │  Human Review       │
         │ Accept/Edit/Reject  │
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────┐
         │ Analytics & History │
         └─────────────────────┘
```

---

## 🧠 How It Works

## 1️⃣ Evidence Collection
User provides:
- Network symptom (what's broken)
- Topology/lab notes
- Cisco CLI evidence (`show ip route`, `show vlan brief`, etc.)

## 2️⃣ Deterministic Analysis
Rule engine detects known problems:
- Interface down / VLAN missing / Route missing
- Duplicate IP / Gateway mismatch / Subnet mask wrong
- DHCP failure / NAT issue / ACL denial

## 3️⃣ AI Diagnosis
Gemini analyzes evidence + rule findings → produces structured diagnosis:
```json
{
  "root_cause": "Missing route to remote VLAN",
  "osi_layer": 3,
  "confidence": "High",
  "severity": "High",
  "evidence": ["Routing table lacks destination network"],
  "next_commands": ["show ip route", "show running-config"],
  "remediation": ["Add static route or configure dynamic routing"],
  "verification": ["Ping remote destination", "Verify routing table"]
}
```

## 4️⃣ Human Review
Reviewer can:
- ✅ **Accept** — Diagnosis is correct
- ✏️ **Edit** — Correct the diagnosis
- ❌ **Reject** — Diagnosis unsupported

System retains both original AI response and human correction.

## 5️⃣ Verification
System provides commands to verify the fix worked.

---

## 📚 What's Included

| Component | Details |
|-----------|---------|
| **Cases** | 30+ realistic network scenarios covering VLAN, Routing, DHCP, DNS, NAT, ACL, OSPF, RIP, Trunking, SSH, IP Addressing |
| **Rule Engine** | 15+ deterministic checks for common network faults |
| **AI Model** | Google Gemini with structured JSON validation |
| **Human Review** | Accept/Edit/Reject workflow with full audit trail |
| **Analytics** | Issue categories, severity, OSI layers, AI/human agreement rates |
| **Demo Mode** | Works offline without API key for testing |

---

## 🚀 Quick Start

## Installation

```bash
# Clone repository
git clone https://github.com/Aastha-1407/Netstage-ai.git
cd Netstage-ai

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

Or use Streamlit Secrets in production.

## Run Application

```bash
streamlit run app.py
```

Application opens at `http://localhost:8501`

---

## 🧰 Technology Stack

| Layer | Technology |
|-------|------------|
| **UI** | Streamlit |
| **Backend** | Python |
| **AI** | Google Gemini + GenAI SDK |
| **Validation** | Pydantic |
| **Data** | Pandas, Plotly |
| **Storage** | CSV, JSON |
| **Deployment** | Streamlit Community Cloud |

---

## 📁 Project Structure

```
netsage-ai/
├── app.py                          # Main Streamlit application
├── core/
│   ├── rule_checker.py             # Deterministic networking rules
│   ├── ai_diagnostician.py         # Gemini integration
│   ├── fallback_diagnostician.py   # Offline/demo mode
│   └── schemas.py                  # Pydantic validation schemas
├── data/
│   ├── cases.csv                   # 30+ troubleshooting cases
│   └── review_log.csv              # Human review history
├── utils/
│   ├── storage.py                  # Data persistence
│   └── validators.py               # Input validation
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🎓 Example Workflow

**Problem:** PC in VLAN 30 can reach gateway but not server in VLAN 20.

**User Input:**
```
Symptom: Cannot reach server in different VLAN
Evidence: show ip route
Evidence: show vlan brief
Evidence: show interfaces trunk
```

**System Process:**
1. Rule engine checks routing table → detects missing route
2. Gemini analyzes: "Layer 3 routing issue"
3. AI recommends: "Add static route to 10.20.0.0/24"
4. Human reviews: ✓ Accepted
5. Verification: User pings server → success

**Result:** User learns *why* the fix worked and *how* to troubleshoot similar issues.

---

## 🛡️ Responsible AI Design

- ✅ Evidence-based reasoning (no fabricated CLI output)
- ✅ Confidence awareness (communicates uncertainty)
- ✅ Human approval required (no autonomous changes)
- ✅ Explainable output (shows evidence + reasoning)
- ✅ No auto-execution (AI suggestions only)
- ✅ Audit trail (retains all diagnoses and reviews)

---

## 🔮 Future Roadmap

- Real Cisco device SSH integration
- Packet Tracer topology visualization
- Configuration comparison and diff
- Cisco documentation retrieval (RAG)
- PostgreSQL backend
- User authentication & role-based access
- Team collaboration
- Automated test case generation

---

## 👥 Team

| Member | Role |
|--------|------|
| **Aastha Sanodiya** | Project Lead, Full-Stack Developer |
| **Deeksha Pandit** | AI & Responsible AI Engineer |
| **Aryan Ravi** | Network Diagnostics & Rule Engine |
| **Aaditya Kumar Mishra** | Data, Testing & Analytics |

---

## 📄 License

MIT License

---

## ⚠️ Disclaimer

NetSage AI is an **educational and decision-support platform**.

- AI recommendations should be reviewed by a qualified human before production deployment
- System does not automatically execute network configuration commands
- Intended for learning, labs, and non-critical environments
- Always verify changes on test networks first

---

## 🚀 [Try Live Demo](https://netstage-ai-eentie5da9xxb8bphmoxzj.streamlit.app/)

---

**Questions?** Open an issue or check the [GitHub repository](https://github.com/Aastha-1407/Netstage-ai).
