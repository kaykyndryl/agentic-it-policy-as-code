package data.policies

# Rego-backed policy catalog used by IT Ticket Management and OPA workflows.
# This replaces the legacy JSON data file.
policies := [
  {
    "id": "POL-001",
    "category": "password_management",
    "title": "Password Security Policy",
    "description": "Establishes minimum password requirements and reset procedures",
    "key_requirements": [
      "Minimum 12 characters",
      "Must contain uppercase, lowercase, numbers, and special characters",
      "Password reset required every 90 days",
      "Cannot reuse last 5 passwords"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Active Directory"
  },
  {
    "id": "POL-002",
    "category": "multi_factor_authentication",
    "title": "Multi-Factor Authentication (MFA) Policy",
    "description": "Requires MFA for all remote access and sensitive systems",
    "key_requirements": [
      "MFA required for VPN access",
      "MFA required for cloud application access",
      "MFA required for administrative accounts",
      "Supported methods: TOTP, hardware tokens, Windows Hello"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Identity Provider"
  },
  {
    "id": "POL-003",
    "category": "data_classification",
    "title": "Data Classification and Handling Policy",
    "description": "Defines how sensitive data must be classified, stored, and transmitted",
    "key_requirements": [
      "Data classified as Public, Internal, Confidential, or Restricted",
      "Restricted data requires encryption at rest and in transit",
      "Regular data classification audits required",
      "Unauthorized data sharing is grounds for termination"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Data Loss Prevention (DLP)"
  },
  {
    "id": "POL-004",
    "category": "patch_management",
    "title": "Software Patch Management Policy",
    "description": "Defines patch deployment and security update schedules",
    "key_requirements": [
      "Critical/Security patches: deployed within 5 days",
      "Important patches: deployed within 30 days",
      "Standard patches: deployed within 60 days",
      "Production servers: change management review required"
    ],
    "compliance_level": "mandatory",
    "enforcement": "SCCM/Intune"
  },
  {
    "id": "POL-005",
    "category": "access_control",
    "title": "Access Control Policy",
    "description": "Defines user access provisioning and deprovisioning procedures",
    "key_requirements": [
      "All access requires business justification",
      "Managers must approve access requests",
      "Quarterly access reviews required",
      "Account deprovisioning within 24 hours of termination"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Identity Governance"
  },
  {
    "id": "POL-006",
    "category": "device_management",
    "title": "Device Management and Mobile Device Policy",
    "description": "Controls device provisioning, security baselines, and mobile device usage",
    "key_requirements": [
      "All devices must be enrolled in MDM",
      "Security baseline must be applied",
      "Antivirus software must be installed and updated",
      "Device encryption required for company data access"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Intune/MDM"
  },
  {
    "id": "POL-007",
    "category": "incident_response",
    "title": "Incident Response Policy",
    "description": "Defines procedures for responding to security incidents",
    "key_requirements": [
      "Security incidents must be reported to Security team within 1 hour",
      "Initial assessment must be completed within 4 hours",
      "Forensic evidence preservation is mandatory",
      "Management notification for critical incidents"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Security Operations Center (SOC)"
  },
  {
    "id": "POL-008",
    "category": "acceptable_use",
    "title": "Acceptable Use Policy",
    "description": "Defines appropriate use of company IT resources",
    "key_requirements": [
      "Company IT resources are for business purposes",
      "Personal use must be minimal and incidental",
      "Prohibited: torrenting, streaming, gambling, illegal content",
      "Violation may result in disciplinary action"
    ],
    "compliance_level": "mandatory",
    "enforcement": "Network Monitoring"
  }
]
