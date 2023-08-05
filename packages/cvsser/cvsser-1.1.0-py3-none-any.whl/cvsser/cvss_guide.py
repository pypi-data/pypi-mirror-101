# -*- coding: utf-8 -*-

cvss_guide = {
  "v2.0": {
    "AV": {
      "name": "Access Vector",
      "values": {
        "L": "Local",
        "A": "Adjacent Network",
        "N": "Network"
      },
      "type": "Base",
      "mandatory": True
    },
    "AC": {
      "name": "Access Complexity",
      "values": {
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Base",
      "mandatory": True
    },
    "Au": {
      "name": "Authentication",
      "values": {
        "M": "Multiple",
        "S": "Single",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "C": {
      "name": "Confidentiality Impact",
      "values": {
        "N": "None",
        "P": "Partial",
        "C": "Complete"
      },
      "type": "Base",
      "mandatory": True
    },
    "I": {
      "name": "Integrity Impact",
      "values": {
        "N": "None",
        "P": "Partial",
        "C": "Complete"
      },
      "type": "Base",
      "mandatory": True
    },
    "A": {
      "name": "Availability Impact",
      "values": {
        "N": "None",
        "P": "Partial",
        "C": "Complete"
      },
      "type": "Base",
      "mandatory": True
    },
    "E": {
      "name": "Exploitability",
      "values": {
        "U": "Unproven",
        "POC": "Proof-of-Concept",
        "F": "Functional",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RL": {
      "name": "Remediation Level",
      "values": {
        "OF": "Official Fix",
        "TF": "Temporary Fix",
        "W": "Workaround",
        "U": "Unavailable",
        "ND": "Not Defined"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RC": {
      "name": "Report Confidence",
      "values": {
        "UC": "Unconfirmed",
        "UR": "Uncorroborated ",
        "C": "Confirmed",
        "ND": "Not Defined"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "CDP": {
      "name": "Collateral Damage Potential",
      "values": {
        "N": "None",
        "L": "Low",
        "LM": "Low-Medium",
        "MH": "Medium-High",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "TD": {
      "name": "Target Distribution",
      "values": {
        "N": "None",
        "L": "Low",
        "M": "Medium",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "CR": {
      "name": "Confidentiality Requirement",
      "values": {
        "L": "Low",
        "M": "Medium",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "IR": {
      "name": "Integrity Requirement",
      "values": {
        "L": "Low",
        "M": "Medium",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "AR": {
      "name": "Availability Requirement",
      "values": {
        "L": "Low",
        "M": "Medium",
        "H": "High",
        "ND": "Not Defined"
      },
      "type": "Environmental",
      "mandatory": False
    }
  },
  "v3.0": {
    "AV": {
      "name": "Attack Vector",
      "values": {
        "N": "Network",
        "A": "Adjacent",
        "L": "Local",
        "P": "Physical"
      },
      "type": "Base",
      "mandatory": True
    },
    "AC": {
      "name": "Attack Complexity",
      "values": {
        "L": "Low",
        "H": "High"
      },
      "type": "Base",
      "mandatory": True
    },
    "PR": {
      "name": "Privileges Required",
      "values": {
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Base",
      "mandatory": True
    },
    "UI": {
      "name": "User Interaction",
      "values": {
        "N": "None",
        "R": "Required"
      },
      "type": "Base",
      "mandatory": True
    },
    "S": {
      "name": "Scope",
      "values": {
        "U": "Unchanged",
        "C": "Changed"
      },
      "type": "Base",
      "mandatory": True
    },
    "C": {
      "name": "Confidentiality Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "I": {
      "name": "Integrity Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "A": {
      "name": "Availability Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "E": {
      "name": "Exploit Code Maturity",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "F": "Functional",
        "P": "Proof-of-Concept",
        "U": "Unproven"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RL": {
      "name": "Remediation Level",
      "values": {
        "X": "Not Defined",
        "U": "Unavailable",
        "W": "Workaround",
        "T": "Temporary Fix",
        "O": "Official Fix"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RC": {
      "name": "Report Confidence",
      "values": {
        "X": "Not Defined",
        "C": "Confirmed",
        "R": "Reasonable",
        "U": "Unknown"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "CR": {
      "name": "Confidentiality Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "IR": {
      "name": "Integrity Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "AR": {
      "name": "Availability Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MAV": {
      "name": "Modified Attack Vector",
      "values": {
        "X": "Not Defined",
        "N": "Network",
        "A": "Adjacent",
        "L": "Local",
        "P": "Physical"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MAC": {
      "name": "Modified Attack Complexity",
      "values": {
        "X": "Not Defined",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MPR": {
      "name": "Modified Privileges Required",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MUI": {
      "name": "Modified User Interaction",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "R": "Required"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MS": {
      "name": "Modified Scope",
      "values": {
        "X": "Not Defined",
        "U": "Unchanged",
        "C": "Changed"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MC": {
      "name": "Modified Confidentiality",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MI": {
      "name": "Modified Integrity",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MA": {
      "name": "Modified Availability",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    }
  },
  "v3.1": {
    "AV": {
      "name": "Attack Vector",
      "values": {
        "N": "Network",
        "A": "Adjacent",
        "L": "Local",
        "P": "Physical"
      },
      "type": "Base",
      "mandatory": True
    },
    "AC": {
      "name": "Attack Complexity",
      "values": {
        "L": "Low",
        "H": "High"
      },
      "type": "Base",
      "mandatory": True
    },
    "PR": {
      "name": "Privileges Required",
      "values": {
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Base",
      "mandatory": True
    },
    "UI": {
      "name": "User Interaction",
      "values": {
        "N": "None",
        "R": "Required"
      },
      "type": "Base",
      "mandatory": True
    },
    "S": {
      "name": "Scope",
      "values": {
        "U": "Unchanged",
        "C": "Changed"
      },
      "type": "Base",
      "mandatory": True
    },
    "C": {
      "name": "Confidentiality Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "I": {
      "name": "Integrity Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "A": {
      "name": "Availability Impact",
      "values": {
        "H": "High",
        "L": "Low",
        "N": "None"
      },
      "type": "Base",
      "mandatory": True
    },
    "E": {
      "name": "Exploit Code Maturity",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "F": "Functional",
        "P": "Proof-of-Concept",
        "U": "Unproven"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RL": {
      "name": "Remediation Level",
      "values": {
        "X": "Not Defined",
        "U": "Unavailable",
        "W": "Workaround",
        "T": "Temporary Fix",
        "O": "Official Fix"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "RC": {
      "name": "Report Confidence",
      "values": {
        "X": "Not Defined",
        "C": "Confirmed",
        "R": "Reasonable",
        "U": "Unknown"
      },
      "type": "Temporal",
      "mandatory": False
    },
    "CR": {
      "name": "Confidentiality Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "IR": {
      "name": "Integrity Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "AR": {
      "name": "Availability Requirement",
      "values": {
        "X": "Not Defined",
        "H": "High",
        "M": "Medium",
        "L": "Low"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MAV": {
      "name": "Modified Attack Vector",
      "values": {
        "X": "Not Defined",
        "N": "Network",
        "A": "Adjacent",
        "L": "Local",
        "P": "Physical"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MAC": {
      "name": "Modified Attack Complexity",
      "values": {
        "X": "Not Defined",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MPR": {
      "name": "Modified Privileges Required",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MUI": {
      "name": "Modified User Interaction",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "R": "Required"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MS": {
      "name": "Modified Scope",
      "values": {
        "X": "Not Defined",
        "U": "Unchanged",
        "C": "Changed"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MC": {
      "name": "Modified Confidentiality",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MI": {
      "name": "Modified Integrity",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    },
    "MA": {
      "name": "Modified Availability",
      "values": {
        "X": "Not Defined",
        "N": "None",
        "L": "Low",
        "H": "High"
      },
      "type": "Environmental",
      "mandatory": False
    }
  }
}