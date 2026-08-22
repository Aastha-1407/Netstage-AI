import re
import ipaddress
from typing import List, Dict, Any

class DeterministicRuleChecker:
    @staticmethod
    def analyze(symptom: str, show_outputs: str, topology_note: str = "") -> List[Dict[str, Any]]:
        findings = []
        text = f"{symptom}\n{show_outputs}\n{topology_note}"

        # Rule 1: Interface Administratively Down / Down
        down_matches = re.findall(r"(\S+)\s+(?:is\s+)?(administratively down|down|disabled)", show_outputs, re.IGNORECASE)
        for intf, status in down_matches:
            if "protocol" not in intf.lower():
                findings.append({
                    "rule": "Interface State Down",
                    "severity": "High",
                    "osi_layer": 1,
                    "evidence": f"Interface {intf} is {status}",
                    "recommendation": f"Execute 'no shutdown' on interface {intf} or inspect physical link."
                })

        # Rule 2: Missing 802.1Q Encapsulation on Sub-interface
        if re.search(r"interface\s+\S+\.\d+", show_outputs, re.IGNORECASE):
            if not re.search(r"encapsulation\s+dot1q\s+\d+", show_outputs, re.IGNORECASE):
                findings.append({
                    "rule": "Missing 802.1Q Encapsulation",
                    "severity": "High",
                    "osi_layer": 2,
                    "evidence": "Sub-interface configured without 'encapsulation dot1Q <vlan-id>'",
                    "recommendation": "Configure 'encapsulation dot1Q <vlan-id>' under the sub-interface before applying IP."
                })

        # Rule 3: OSPF MTU Mismatch
        mtus = re.findall(r"MTU\s+(\d+)", show_outputs, re.IGNORECASE)
        if len(set(mtus)) > 1:
            findings.append({
                "rule": "OSPF MTU Mismatch",
                "severity": "High",
                "osi_layer": 3,
                "evidence": f"Found conflicting MTU sizes: {', '.join(set(mtus))}",
                "recommendation": "Align interface MTU sizes or apply 'ip ospf mtu-ignore' under interface."
            })

        # Rule 4: Native VLAN Mismatch
        native_vlans = re.findall(r"Native VLAN:?\s*(\d+)", show_outputs, re.IGNORECASE)
        if len(set(native_vlans)) > 1:
            findings.append({
                "rule": "Native VLAN Mismatch",
                "severity": "Medium",
                "osi_layer": 2,
                "evidence": f"Trunk ports report differing native VLANs: {', '.join(set(native_vlans))}",
                "recommendation": "Configure matching native VLAN on both sides: 'switchport trunk native vlan <id>'."
            })

        # Rule 5: Missing IP Helper Address
        if "dhcp" in symptom.lower() or "apipa" in symptom.lower() or "169.254" in symptom:
            if "encapsulation dot1q" in show_outputs.lower() and "ip helper-address" not in show_outputs.lower():
                findings.append({
                    "rule": "Missing DHCP Helper Address",
                    "severity": "High",
                    "osi_layer": 3,
                    "evidence": "VLAN router sub-interface lacks 'ip helper-address <dhcp-server-ip>'",
                    "recommendation": "Add 'ip helper-address <DHCP-Server-IP>' under the routing interface/sub-interface."
                })

        # Rule 6: NAT Inside/Outside Interface Directive Missing
        if "ip nat inside source" in show_outputs.lower():
            has_inside = bool(re.search(r"ip\s+nat\s+inside", show_outputs, re.IGNORECASE))
            has_outside = bool(re.search(r"ip\s+nat\s+outside", show_outputs, re.IGNORECASE))
            if not has_inside or not has_outside:
                findings.append({
                    "rule": "Incomplete NAT Configuration",
                    "severity": "High",
                    "osi_layer": 3,
                    "evidence": f"NAT status - inside configured: {has_inside}, outside configured: {has_outside}",
                    "recommendation": "Ensure 'ip nat inside' is applied to LAN interface and 'ip nat outside' to WAN interface."
                })

        return findings