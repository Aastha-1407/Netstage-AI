# Netstage-ai
🛰️ NetSage AI
Evidence-First AI Network Troubleshooting & Diagnosis Platform

NetSage AI is an intelligent network troubleshooting platform built for Cisco networking labs, Packet Tracer environments, CCNA learners, and junior network engineers.

The platform combines deterministic networking rules, Generative AI, Cisco CLI evidence, and human-in-the-loop validation to transform raw network symptoms into structured, explainable troubleshooting recommendations.

Instead of simply asking an AI model “What is wrong with my network?”, NetSage AI follows a controlled diagnostic pipeline:

┌──────────────────────────────────────────────────────────────┐
│                    NETSAGE AI PLATFORM                       │
└──────────────────────────────────────────────────────────────┘

        Network Symptom / Topology / CLI Evidence
                         │
                         ▼
              ┌─────────────────────┐
              │ Evidence Collection │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Deterministic Rule  │
              │      Engine         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   AI Diagnostic     │
              │      Engine         │
              │      Gemini         │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Structured Diagnosis│
              │ Root Cause / Layer  │
              │ Evidence / Severity │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Human Review      │
              │ Accept / Edit /     │
              │ Reject              │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Verification &      │
              │ Review Logging      │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Analytics & Insights│
              └─────────────────────┘
🎯 Problem Statement

Network troubleshooting often requires engineers to interpret multiple sources of information simultaneously:

User-reported symptoms
Network topology
Cisco IOS configuration
Routing tables
Interface states
VLAN configuration
ACLs
NAT translations
DHCP information
DNS configuration
Routing protocols

For beginners and junior engineers, the difficult part is not memorizing commands. The difficult part is connecting evidence to the correct root cause.

NetSage AI addresses this gap by providing a structured troubleshooting workflow that combines traditional rule-based analysis with AI-assisted reasoning.

🧠 Core Philosophy

NetSage AI follows three principles:

1. Evidence First

The system should reason from the evidence supplied by the user.

It should never invent Cisco CLI output or unseen configuration.

2. AI Assisted, Not AI Autonomous

The AI provides a diagnosis and recommendations, but it does not directly modify network devices.

3. Human in the Loop

Every diagnosis passes through a review stage:

AI Diagnosis
     ↓
Human Review
     ├── Accept
     ├── Edit
     └── Reject

This makes the system more suitable for educational environments and responsible AI workflows.

🏗️ System Architecture

NetSage AI is divided into several logical layers.

                    ┌───────────────────┐
                    │   Streamlit UI    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Application Layer │
                    └─────────┬─────────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
     ┌──────────────────┐           ┌──────────────────┐
     │ Rule Engine      │           │ AI Diagnostic    │
     │                  │           │ Engine           │
     │ Deterministic    │           │ Gemini           │
     │ Network Checks   │           │ Structured JSON  │
     └────────┬─────────┘           └────────┬─────────┘
              │                              │
              └──────────────┬───────────────┘
                             ▼
                    ┌───────────────────┐
                    │ Diagnosis Schema  │
                    │ Pydantic          │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Human Review      │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Persistence Layer │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Analytics Layer  │
                    └───────────────────┘
🔬 Diagnostic Pipeline

A troubleshooting session follows this pipeline:

Step 1 — Evidence Collection

The user provides:

Symptom
Topology
Cisco IOS show output

For example:

PC can reach its gateway but cannot reach a server
in another VLAN.
Step 2 — Deterministic Analysis

The rule engine evaluates known networking patterns.

Examples:

Interface administratively down
Duplicate IP
Wrong subnet mask
Gateway mismatch
Missing VLAN
Missing route
Trunk VLAN mismatch
DHCP failure
NAT configuration issue
ACL denial

This layer provides predictable, explainable checks independent of the LLM.

Step 3 — AI Diagnosis

Gemini receives the supplied evidence together with the deterministic findings.

The AI produces a structured diagnosis containing:

Root Cause
OSI Layer
Issue Type
Severity
Confidence
Evidence
Next Commands
Remediation
Verification
Reviewer Note
Step 4 — Validation

The AI response is validated against a structured schema.

This prevents malformed AI output from silently entering the application.

Step 5 — Human Review

The reviewer can:

Accept

if the diagnosis is correct.

Edit

if the diagnosis needs correction.

Reject

if the diagnosis is unsupported.

The original AI response and human decision are retained.

Step 6 — Verification

The system provides commands and checks that can be used to verify whether the issue was actually resolved.

Step 7 — Analytics

Review data feeds the analytics layer.

This allows the project to measure:

AI agreement
Correction rate
Rejection rate
Common network problems
Severity distribution
OSI-layer distribution
Most frequent root causes
📁 Project Architecture
netsage-ai/
│
├── app.py
│
├── core/
│   ├── __init__.py
│   ├── rule_checker.py
│   ├── ai_diagnostician.py
│   ├── fallback_diagnostician.py
│   └── schemas.py
│
├── data/
│   ├── cases.csv
│   └── review_log.csv
│
├── utils/
│   ├── __init__.py
│   ├── storage.py
│   └── validators.py
│
├── assets/
│
├── diagnose_prompt.md
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
🧩 Major Components
🎨 Streamlit Interface

Provides the interactive application experience.

Main modules:

Dashboard
Troubleshooting Studio
Case Library
Rule Checker
Human Review
Analytics
Settings
⚙️ Rule Engine

The deterministic layer identifies known network problems without depending on an LLM.

This improves:

Explainability
Reliability
Repeatability
Debuggability
🤖 AI Diagnostic Engine

Gemini provides contextual reasoning over the supplied evidence.

The AI is not responsible for basic deterministic checks alone. Instead, it works alongside the rule engine.

Rules = deterministic evidence
AI = contextual reasoning
Human = final decision
🧾 Schema Validation

Pydantic validates AI responses before they reach the UI.

This creates a controlled interface between the LLM and application.

Gemini
   ↓
JSON
   ↓
Pydantic Validation
   ↓
Diagnosis Object
   ↓
Streamlit UI
👨‍⚖️ Human Review System

The review layer is one of the most important parts of the project.

It records:

AI Diagnosis
     +
Human Decision
     +
Human Correction
     +
Reviewer Notes

This creates a feedback dataset that can later be used to evaluate and improve the diagnostic system.

📊 Analytics

The analytics dashboard provides visibility into the system's behavior.

Example metrics:

Total Cases
Diagnostics Run
Human Reviews
AI Agreement
Corrections
Rejections
Critical Issues

Visualizations include:

Issue categories
Severity
OSI layers
Review outcomes
AI/human agreement
Common root causes
📚 Dataset

The project contains 30+ realistic network troubleshooting scenarios covering areas such as:

VLAN
Routing
DHCP
DNS
NAT
ACL
Wireless
Trunking
OSPF
RIP
SSH
IP addressing
Gateway configuration
Interface failures

Each case contains structured troubleshooting information rather than just a question/answer pair.

🛡️ Responsible AI Architecture

NetSage AI intentionally avoids fully autonomous network modification.

The system follows:

          ┌─────────────┐
          │   Evidence  │
          └──────┬──────┘
                 ↓
          ┌─────────────┐
          │ Rule Engine │
          └──────┬──────┘
                 ↓
          ┌─────────────┐
          │     AI      │
          └──────┬──────┘
                 ↓
          ┌─────────────┐
          │ Diagnosis   │
          └──────┬──────┘
                 ↓
          ┌─────────────┐
          │   Human     │
          │   Review    │
          └──────┬──────┘
                 ↓
          ┌─────────────┐
          │ Verification│
          └─────────────┘

AI-generated Cisco commands are recommendations only.

The application never automatically executes configuration changes on network devices.

🚀 Technology Stack
Layer	Technology
UI	Streamlit
Language	Python
AI	Google Gemini
AI SDK	Google GenAI
Validation	Pydantic
Data Processing	Pandas
Visualization	Plotly
Network Concepts	Cisco IOS / Packet Tracer
Storage	CSV / JSON
Deployment	Streamlit Community Cloud
🔐 Security

NetSage AI follows basic security practices:

API keys stored through environment variables/secrets
No hard-coded credentials
No automatic network configuration execution
Structured AI output validation
Human approval before remediation
Graceful handling of missing AI credentials
💡 Example Workflow
User:
"PC can reach gateway but cannot reach server."

                ↓

Cisco Evidence:
show ip route

                ↓

Rule Engine:
Possible missing route detected

                ↓

Gemini:
Likely root cause:
Missing route to remote VLAN

Confidence:
High

OSI:
Layer 3

                ↓

Recommended Command:
show ip route

                ↓

Human Review:
✓ Accepted

                ↓

Verification:
Ping server
Check routing table
Confirm connectivity
🎓 Intended Use

NetSage AI is designed for:

CCNA students
Networking students
Cisco Packet Tracer labs
Network troubleshooting practice
Junior network engineers
Networking instructors
AI-assisted technical education
Responsible AI demonstrations
🚀 Future Roadmap

Potential future enhancements include:

Real Cisco device integration
SSH-based read-only diagnostics
Packet Tracer integration
Network topology visualization
Automated configuration diff
RAG-based Cisco documentation retrieval
More advanced network telemetry
PostgreSQL backend
Authentication and role-based access
Team collaboration
Reviewer feedback-driven model evaluation
Historical incident similarity search
📌 Project Vision

NetSage AI aims to bridge the gap between networking knowledge and practical troubleshooting reasoning.

Instead of giving engineers another chatbot, the platform provides a structured diagnostic workflow:

Observe → Analyze → Explain → Review → Verify

The result is an AI-assisted network troubleshooting environment that emphasizes evidence, explainability, human judgment, and practical Cisco networking skills.
