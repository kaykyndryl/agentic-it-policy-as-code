package policy.change_control

# Auto-generated from uploaded policy documentation
# Source document: Compay Information Security System and Change Control Policy2.pdf
# Rule count: 50 (30 IT change control + 20 healthcare)

# Extracted policy statements from the uploaded document
# 01. Company System Information Security and Change Control Policy Document Owner: Chief Information Security Officer (CISO) / Privacy Officer Approved By: [Executive Approver / Governance Committee] Versi
# 02. Purpose The purpose of this policy is to establish a clear, practical, and enforceable framework for protecting electronic protected health information (ePHI), supporting safe and reliable patient car
# 03. This policy is written to support the confidentiality, integrity, and availability of ePHI; to ensure that changes to production systems are planned, reviewed, approved, tested, and documented; and to
# 04. Scope This policy applies to all workforce members, medical staff, temporary staff, contractors, students, volunteers, vendors, managed service providers, and business associates who access, administe
# 05. Policy Statement [Organization Name] will maintain written, implemented, and periodically updated security and change control policies and procedures that are reasonable and appropriate for the size,
# 06. All systems containing or supporting ePHI shall be protected through administrative, physical, and technical safeguards.
# 07. Production changes shall not be introduced without documented planning, appropriate authorization, adequate testing, traceability, and post-implementation accountability, except under formally governe
# 08. No workforce member or vendor may bypass this policy, disable required safeguards, or introduce unapproved changes to production systems that could materially affect patient safety, care continuity, p
# 09. Protect ePHI and other confidential healthcare information from unauthorized access, use, disclosure, alteration, destruction, or loss.
# 10. Reduce operational and patient-care disruption caused by poorly governed changes.
# 11. Create a repeatable and risk-based change process that scales across clinical and enterprise environments.
# 12. Ensure accountability through documentation, approvals, audit trails, and evidence retention.

# IT-001 [it]
deny[msg] {
  input.change.author == input.change.approver
  msg := "Change cannot be approved by its author"
}

# IT-002 [it]
deny[msg] {
  input.change.risk_level == "high"
  not input.change.cab_approved
  msg := "High-risk change requires CAB approval"
}

# IT-003 [it]
deny[msg] {
  input.change.environment == "production"
  not input.change.rollback_plan
  msg := "Production changes require rollback plan"
}

# IT-004 [it]
deny[msg] {
  input.change.type == "emergency"
  not input.change.post_implementation_review
  msg := "Emergency change must include post-implementation review"
}

# IT-005 [it]
deny[msg] {
  input.change.developer == input.change.deployer
  msg := "Segregation of duties required for deployment"
}

# IT-006 [it]
deny[msg] {
  not input.change.window_start
  msg := "Change window must be defined"
}

# IT-007 [it]
deny[msg] {
  not input.change.window_end
  msg := "Change window end time must be defined"
}

# IT-008 [it]
deny[msg] {
  input.change.impacts_security
  not input.change.security_reviewed
  msg := "Security-impacting changes require security review"
}

# IT-009 [it]
deny[msg] {
  input.change.includes_db_schema
  not input.change.dba_approved
  msg := "Database schema changes require DBA approval"
}

# IT-010 [it]
deny[msg] {
  input.change.includes_infrastructure
  not input.change.architecture_approved
  msg := "Infrastructure changes require architecture review"
}

# IT-011 [it]
deny[msg] {
  input.change.environment == "production"
  count(input.change.test_evidence) == 0
  msg := "Production changes require test evidence"
}

# IT-012 [it]
deny[msg] {
  input.change.type == "standard"
  not input.change.template_id
  msg := "Standard changes must use approved template"
}

# IT-013 [it]
deny[msg] {
  input.change.type == "emergency"
  not input.change.emergency_reason
  msg := "Emergency change reason must be documented"
}

# IT-014 [it]
deny[msg] {
  not input.change.rollback_owner
  msg := "Backout contact must be assigned"
}

# IT-015 [it]
deny[msg] {
  count(input.change.implementers) == 0
  msg := "Change implementation team must be listed"
}

# IT-016 [it]
deny[msg] {
  input.change.environment == "production"
  not input.change.monitoring_plan
  msg := "Monitoring plan is required after production change"
}

# IT-017 [it]
deny[msg] {
  input.change.customer_impact
  not input.change.communication_plan
  msg := "Customer communication required for service-impacting change"
}

# IT-018 [it]
deny[msg] {
  input.change.requires_outage
  not input.change.estimated_downtime_minutes
  msg := "Planned outage must include downtime estimate"
}

# IT-019 [it]
deny[msg] {
  input.change.risk_level == "high"
  not input.change.peer_reviewed
  msg := "High-risk change requires peer review"
}

# IT-020 [it]
deny[msg] {
  input.change.includes_code
  not input.change.ticket_id
  msg := "Source code changes must reference approved ticket"
}

# IT-021 [it]
deny[msg] {
  input.change.includes_access_change
  not input.change.iam_approved
  msg := "Production access changes require IAM approval"
}

# IT-022 [it]
deny[msg] {
  input.change.privileged_access_change
  count(input.change.approvals) < 2
  msg := "Privileged access changes require dual authorization"
}

# IT-023 [it]
deny[msg] {
  input.change.type == "patch"
  not input.change.cve_reference
  msg := "Patch deployment must include CVE reference"
}

# IT-024 [it]
deny[msg] {
  input.change.includes_firewall_update
  not input.change.security_arch_approved
  msg := "Firewall changes require security architecture sign-off"
}

# IT-025 [it]
deny[msg] {
  count(input.change.affected_assets) == 0
  msg := "Change records must include affected assets"
}

# IT-026 [it]
deny[msg] {
  input.change.includes_data_migration
  not input.change.reconciliation_plan
  msg := "Data migration changes require reconciliation plan"
}

# IT-027 [it]
deny[msg] {
  input.change.major_change
  not input.change.backup_verified
  msg := "Backup verification is required before major change"
}

# IT-028 [it]
deny[msg] {
  input.change.affects_critical_service
  not input.change.executive_notified
  msg := "Critical service changes require executive notification"
}

# IT-029 [it]
deny[msg] {
  input.change.environment == "production"
  input.change.in_freeze_window
  msg := "Production change cannot be scheduled during freeze window"
}

# IT-030 [it]
deny[msg] {
  input.change.status == "closed"
  not input.change.validation_evidence
  msg := "Change closure requires validation evidence"
}

# HC-001 [healthcare]
deny[msg] {
  input.change.affects_phi
  not input.change.privacy_officer_approved
  msg := "PHI access change requires privacy approval"
}

# HC-002 [healthcare]
deny[msg] {
  input.change.affects_phi
  not input.change.hipaa_risk_assessment
  msg := "PHI system change requires HIPAA risk assessment"
}

# HC-003 [healthcare]
deny[msg] {
  input.change.affects_clinical_system
  input.change.requires_outage
  not input.change.patient_safety_plan
  msg := "Clinical system downtime requires patient safety plan"
}

# HC-004 [healthcare]
deny[msg] {
  input.change.affects_ehr
  not input.change.cmio_approved
  msg := "EHR configuration change requires CMIO review"
}

# HC-005 [healthcare]
deny[msg] {
  input.change.affects_medication_workflow
  not input.change.pharmacy_approved
  msg := "Medication workflow changes require pharmacy sign-off"
}

# HC-006 [healthcare]
deny[msg] {
  input.change.affects_lab_interface
  not input.change.interface_validation_report
  msg := "Lab interface changes require validation results"
}

# HC-007 [healthcare]
deny[msg] {
  input.change.affects_radiology
  not input.change.dicom_compatibility_verified
  msg := "Radiology integration changes require DICOM compatibility check"
}

# HC-008 [healthcare]
deny[msg] {
  input.change.affects_telehealth
  not input.change.security_test_completed
  msg := "Telehealth platform changes require security testing"
}

# HC-009 [healthcare]
deny[msg] {
  input.change.phi_export_enabled
  not input.change.audit_logging_verified
  msg := "Changes impacting PHI exports require audit log verification"
}

# HC-010 [healthcare]
deny[msg] {
  input.change.affects_patient_portal
  not input.change.accessibility_reviewed
  msg := "Patient portal changes require accessibility review"
}

# HC-011 [healthcare]
deny[msg] {
  input.change.affects_patient_identity_matching
  not input.change.data_quality_approved
  msg := "Identity matching changes require data quality approval"
}

# HC-012 [healthcare]
deny[msg] {
  input.change.affects_clinical_decision_support
  not input.change.physician_approved
  msg := "Clinical decision support changes require physician sign-off"
}

# HC-013 [healthcare]
deny[msg] {
  input.change.affects_phi_retention
  not input.change.legal_approved
  msg := "PHI retention rule changes require legal approval"
}

# HC-014 [healthcare]
deny[msg] {
  input.change.third_party_healthcare_vendor
  not input.change.baa_confirmed
  msg := "Third-party healthcare integration requires BAA confirmation"
}

# HC-015 [healthcare]
deny[msg] {
  input.change.affects_nursing_workflow
  not input.change.nursing_leadership_approved
  msg := "Nursing workflow changes require nursing leadership sign-off"
}

# HC-016 [healthcare]
deny[msg] {
  input.change.affects_clinical_alert_thresholds
  not input.change.clinical_governance_approved
  msg := "Clinical alert threshold changes require governance approval"
}

# HC-017 [healthcare]
deny[msg] {
  input.change.affects_consent_workflow
  not input.change.compliance_validated
  msg := "Patient consent workflow changes require compliance validation"
}

# HC-018 [healthcare]
deny[msg] {
  input.change.affects_eprescribing
  not input.change.controlled_substance_checks_complete
  msg := "Changes to ePrescribing require controlled-substance checks"
}

# HC-019 [healthcare]
deny[msg] {
  input.change.affects_medical_device_integration
  not input.change.biomedical_approved
  msg := "Medical device integration changes require biomedical review"
}

# HC-020 [healthcare]
deny[msg] {
  input.change.affects_phi
  input.change.go_live
  not input.change.incident_response_updated
  msg := "PHI-related incident response procedures must be updated before go-live"
}
