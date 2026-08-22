import json
import os
from typing import Dict, Any
from pydantic import BaseModel, Field

class DiagnosisResponse(BaseModel):
    root_cause: str = Field(description="Clear explanation of the diagnosed network failure")
    osi_layer: int = Field(description="OSI Layer number from 1 to 7")
    confidence: str = Field(description="High, Medium, or Low")
    evidence: list[str] = Field(description="Exact lines or parameters from show command output")
    next_commands: list[str] = Field(description="Commands recommended to isolate or verify")
    remediation_steps: list[str] = Field(description="Exact Cisco IOS commands to fix the issue")

class AIDiagnostician:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.client = None
        if self.api_key:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)

    def diagnose(self, symptom: str, topology_note: str, show_outputs: str) -> Dict[str, Any]:
        prompt = f"""You are NetSage AI, a specialized Cisco CCNA / Network Troubleshooting Assistant.
Analyze the following network scenario and return ONLY a valid JSON object matching the schema.

Scenario:
- Symptom: {symptom}
- Topology Note: {topology_note}
- Show Command Outputs:
{show_outputs}

Rules:
1. Ground your diagnosis strictly on the provided show outputs.
2. Quote exact command lines in the 'evidence' list.
3. Provide executable Cisco IOS CLI commands in 'remediation_steps'.
4. Do not wrap JSON in markdown ticks if possible, return raw json.
"""
        if self.client:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config={
                        'response_mime_type': 'application/json',
                        'response_schema': DiagnosisResponse,
                        'temperature': 0.1,
                    },
                )
                return json.loads(response.text)
            except Exception as e:
                return self._fallback_simulated(symptom, show_outputs, error_note=str(e))
        else:
            return self._fallback_simulated(symptom, show_outputs)

    def _fallback_simulated(self, symptom: str, show_outputs: str, error_note: str = None) -> Dict[str, Any]:
        return {
            "root_cause": "Deterministic Fallback: Possible Layer 2/3 interface misconfiguration or missing route/helper-address.",
            "osi_layer": 3,
            "confidence": "Medium",
            "evidence": [line.strip() for line in show_outputs.splitlines() if line.strip()][:2],
            "next_commands": ["show ip interface brief", "show running-config", "show ip route"],
            "remediation_steps": ["Verify interface IP addressing", "Check VLAN database and trunk encapsulation"],
            "_note": "Generated via offline engine" if not error_note else f"API Fallback: {error_note}"
        }