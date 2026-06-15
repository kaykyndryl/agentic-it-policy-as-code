package policy.change_control

# Auto-generated from uploaded policy documentation
# Source document: Company System Information Security and Change Control Policy.docx
# Rule count: 50 (30 IT change control + 10 manufacturing + 10 government)

# Extracted policy statements from the uploaded document
# 01. Manufacturing and Government Contract Information Security and Change Control Policy Document Owner: Chief Information Security Officer (CISO) / Director of Compliance Approved By: Executive Approver
# 02. Purpose The purpose of this policy is to establish a clear, practical, and enforceable framework for protecting controlled unclassified information (CUI), covered defense information (CDI), export-con
# 03. This policy translates contractual, regulatory, and security obligations into day-to-day expectations for employees, contractors, subcontractors, suppliers, and service providers.
# 04. This policy is written to support the confidentiality, integrity, and availability of sensitive contract, engineering, production, and operational data; to ensure that changes to production IT and OT
# 05. Scope This policy applies to all employees, temporary staff, contractors, subcontractors, consultants, suppliers, vendors, managed service providers, and third parties who access, administer, support,
# 06. Policy Statement [Organization Name] will maintain written, implemented, and periodically updated security and change control policies and procedures that are reasonable and appropriate for the size,
# 07. All systems containing or supporting CUI, CDI, export-controlled data, and other sensitive contract or manufacturing information shall be protected through administrative, physical, and technical safe
# 08. Production changes shall not be introduced without documented planning, appropriate authorization, adequate testing, traceability, and post-implementation accountability, except under formally governe
# 09. No employee, contractor, supplier, or vendor may bypass this policy, disable required safeguards, or introduce unapproved changes to production systems that could materially affect contractual complia
# 10. Objectives The objectives of this policy are to: Protect CUI, CDI, export-controlled data, and other confidential manufacturing and contract information from unauthorized access, use, disclosure, alte
# 11. Reduce operational disruption, quality issues, and contract performance risk caused by poorly governed changes.
# 12. Create a repeatable and risk-based change process that scales across enterprise IT, engineering systems, and OT environments.

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

# MFG-001 [manufacturing]
deny[msg] {
  input.change.affects_ot_system
  not input.change.safety_assessment_completed
  msg := "OT system changes require operational safety assessment"
}

# MFG-002 [manufacturing]
deny[msg] {
  input.change.affects_production_line
  not input.change.manufacturing_engineer_approved
  msg := "Production line changes require manufacturing engineer approval"
}

# MFG-003 [manufacturing]
deny[msg] {
  input.change.affects_critical_equipment
  not input.change.equipment_specialist_approved
  msg := "Critical equipment modification requires equipment specialist sign-off"
}

# MFG-004 [manufacturing]
deny[msg] {
  input.change.affects_supply_chain_system
  not input.change.vendor_verified
  msg := "Supply chain integration changes require vendor verification"
}

# MFG-005 [manufacturing]
deny[msg] {
  input.change.affects_inventory_system
  not input.change.reconciliation_audit_completed
  msg := "Inventory management changes require reconciliation audit"
}

# MFG-006 [manufacturing]
deny[msg] {
  input.change.affects_maintenance_system
  not input.change.maintenance_lead_approved
  msg := "Maintenance system changes require maintenance team approval"
}

# MFG-007 [manufacturing]
deny[msg] {
  input.change.affects_quality_control
  not input.change.qa_director_approved
  msg := "Quality control system changes require QA director sign-off"
}

# MFG-008 [manufacturing]
deny[msg] {
  input.change.affects_safety_system
  not input.change.facility_manager_approved
  msg := "Plant safety system changes require facility manager authorization"
}

# MFG-009 [manufacturing]
deny[msg] {
  input.change.affects_ot_network
  not input.change.ics_security_reviewed
  msg := "OT network changes require industrial control system security review"
}

# MFG-010 [manufacturing]
deny[msg] {
  input.change.affects_process_parameters
  not input.change.process_owner_approved
  msg := "Manufacturing process parameter changes require process owner approval"
}

# GOV-001 [government]
deny[msg] {
  input.change.includes_itar_code
  not input.change.export_control_reviewed
  msg := "ITAR-controlled code changes require export compliance review"
}

# GOV-002 [government]
deny[msg] {
  input.change.affects_classified_system
  not input.change.clearance_verified
  msg := "Classified system changes require security clearance verification"
}

# GOV-003 [government]
deny[msg] {
  input.change.grants_foreign_national_access
  not input.change.ciso_legal_approved
  msg := "Foreign national access changes require CISO and legal approval"
}

# GOV-004 [government]
deny[msg] {
  input.change.involves_ear_technology
  not input.change.ear_compliance_certified
  msg := "EAR technology transfer changes require compliance certification"
}

# GOV-005 [government]
deny[msg] {
  input.change.contract_milestone_impact
  not input.change.customer_notified
  msg := "Contract milestone deadline changes require customer notification"
}

# GOV-006 [government]
deny[msg] {
  input.change.interfaces_with_gov_system
  not input.change.fisma_compliance_audit
  msg := "Government system interface changes require FISMA compliance audit"
}

# GOV-007 [government]
deny[msg] {
  input.change.affects_dod_incident_plan
  not input.change.dod_approved
  msg := "Cybersecurity incident response plan changes require DoD approval"
}

# GOV-008 [government]
deny[msg] {
  input.change.affects_exfiltration_controls
  not input.change.secops_reviewed
  msg := "Data exfiltration controls changes require security operations review"
}

# GOV-009 [government]
deny[msg] {
  input.change.affects_cui_handling
  not input.change.cui_compliance_validated
  msg := "Controlled unclassified information (CUI) handling changes require compliance validation"
}

# GOV-010 [government]
deny[msg] {
  input.change.affects_facility_access
  not input.change.govt_site_approved
  msg := "Facility access control changes requiring government site visit approval"
}
