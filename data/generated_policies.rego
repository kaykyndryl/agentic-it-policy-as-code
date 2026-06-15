package policy.change_control

# Auto-generated from uploaded policy documentation
# Source document: Company System Information Security and Change Control Policy.pdf
# Rule count: 50
# Domain labels: IT: 30, Manufacturing: 10, Government: 10

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
# 10. Protect CUI, CDI, export-controlled data, and other confidential manufacturing and contract information from unauthorized access, use, disclosure, alteration, destruction, or loss.
# 11. Reduce operational disruption, quality issues, and contract performance risk caused by poorly governed changes.
# 12. Create a repeatable and risk-based change process that scales across enterprise IT, engineering systems, and OT environments.

# [IT] IT-001
deny[msg] {
  input.change.author == input.change.approver
  msg := "Change cannot be approved by its author"
}

# [IT] IT-002
deny[msg] {
  input.change.risk_level == "high"
  not input.change.cab_approved
  msg := "High-risk change requires CAB approval"
}

# [IT] IT-003
deny[msg] {
  input.change.environment == "production"
  not input.change.rollback_plan
  msg := "Production changes require rollback plan"
}

# [IT] IT-004
deny[msg] {
  input.change.type == "emergency"
  not input.change.post_implementation_review
  msg := "Emergency change must include post-implementation review"
}

# [IT] IT-005
deny[msg] {
  input.change.developer == input.change.deployer
  msg := "Segregation of duties required for deployment"
}

# [IT] IT-006
deny[msg] {
  not input.change.window_start
  msg := "Change window must be defined"
}

# [IT] IT-007
deny[msg] {
  not input.change.window_end
  msg := "Change window end time must be defined"
}

# [IT] IT-008
deny[msg] {
  input.change.impacts_security
  not input.change.security_reviewed
  msg := "Security-impacting changes require security review"
}

# [IT] IT-009
deny[msg] {
  input.change.includes_db_schema
  not input.change.dba_approved
  msg := "Database schema changes require DBA approval"
}

# [IT] IT-010
deny[msg] {
  input.change.includes_infrastructure
  not input.change.architecture_approved
  msg := "Infrastructure changes require architecture review"
}

# [IT] IT-011
deny[msg] {
  input.change.environment == "production"
  count(input.change.test_evidence) == 0
  msg := "Production changes require test evidence"
}

# [IT] IT-012
deny[msg] {
  input.change.type == "standard"
  not input.change.template_id
  msg := "Standard changes must use approved template"
}

# [IT] IT-013
deny[msg] {
  input.change.type == "emergency"
  not input.change.emergency_reason
  msg := "Emergency change reason must be documented"
}

# [IT] IT-014
deny[msg] {
  not input.change.rollback_owner
  msg := "Backout contact must be assigned"
}

# [IT] IT-015
deny[msg] {
  count(input.change.implementers) == 0
  msg := "Change implementation team must be listed"
}

# [IT] IT-016
deny[msg] {
  input.change.environment == "production"
  not input.change.monitoring_plan
  msg := "Monitoring plan is required after production change"
}

# [IT] IT-017
deny[msg] {
  input.change.customer_impact
  not input.change.communication_plan
  msg := "Customer communication required for service-impacting change"
}

# [IT] IT-018
deny[msg] {
  input.change.requires_outage
  not input.change.estimated_downtime_minutes
  msg := "Planned outage must include downtime estimate"
}

# [IT] IT-019
deny[msg] {
  input.change.risk_level == "high"
  not input.change.peer_reviewed
  msg := "High-risk change requires peer review"
}

# [IT] IT-020
deny[msg] {
  input.change.includes_code
  not input.change.ticket_id
  msg := "Source code changes must reference approved ticket"
}

# [IT] IT-021
deny[msg] {
  input.change.includes_access_change
  not input.change.iam_approved
  msg := "Production access changes require IAM approval"
}

# [IT] IT-022
deny[msg] {
  input.change.privileged_access_change
  count(input.change.approvals) < 2
  msg := "Privileged access changes require dual authorization"
}

# [IT] IT-023
deny[msg] {
  input.change.type == "patch"
  not input.change.cve_reference
  msg := "Patch deployment must include CVE reference"
}

# [IT] IT-024
deny[msg] {
  input.change.includes_firewall_update
  not input.change.security_arch_approved
  msg := "Firewall changes require security architecture sign-off"
}

# [IT] IT-025
deny[msg] {
  count(input.change.affected_assets) == 0
  msg := "Change records must include affected assets"
}

# [IT] IT-026
deny[msg] {
  input.change.includes_data_migration
  not input.change.reconciliation_plan
  msg := "Data migration changes require reconciliation plan"
}

# [IT] IT-027
deny[msg] {
  input.change.major_change
  not input.change.backup_verified
  msg := "Backup verification is required before major change"
}

# [IT] IT-028
deny[msg] {
  input.change.affects_critical_service
  not input.change.executive_notified
  msg := "Critical service changes require executive notification"
}

# [IT] IT-029
deny[msg] {
  input.change.environment == "production"
  input.change.in_freeze_window
  msg := "Production change cannot be scheduled during freeze window"
}

# [IT] IT-030
deny[msg] {
  input.change.status == "closed"
  not input.change.validation_evidence
  msg := "Change closure requires validation evidence"
}

# [Manufacturing] MFG-001
deny[msg] {
  input.change.affects_ot_system
  not input.change.safety_assessment_completed
  msg := "OT system changes require operational safety assessment"
}

# [Manufacturing] MFG-002
deny[msg] {
  input.change.affects_production_line
  not input.change.manufacturing_engineer_approved
  msg := "Production line changes require manufacturing engineer approval"
}

# [Manufacturing] MFG-003
deny[msg] {
  input.change.affects_critical_equipment
  not input.change.equipment_specialist_approved
  msg := "Critical equipment modification requires equipment specialist sign-off"
}

# [Manufacturing] MFG-004
deny[msg] {
  input.change.affects_supply_chain_system
  not input.change.vendor_verified
  msg := "Supply chain integration changes require vendor verification"
}

# [Manufacturing] MFG-005
deny[msg] {
  input.change.affects_inventory_system
  not input.change.reconciliation_audit_completed
  msg := "Inventory management changes require reconciliation audit"
}

# [Manufacturing] MFG-006
deny[msg] {
  input.change.affects_maintenance_system
  not input.change.maintenance_lead_approved
  msg := "Maintenance system changes require maintenance team approval"
}

# [Manufacturing] MFG-007
deny[msg] {
  input.change.affects_quality_control
  not input.change.qa_director_approved
  msg := "Quality control system changes require QA director sign-off"
}

# [Manufacturing] MFG-008
deny[msg] {
  input.change.affects_safety_system
  not input.change.facility_manager_approved
  msg := "Plant safety system changes require facility manager authorization"
}

# [Manufacturing] MFG-009
deny[msg] {
  input.change.affects_ot_network
  not input.change.ics_security_reviewed
  msg := "OT network changes require industrial control system security review"
}

# [Manufacturing] MFG-010
deny[msg] {
  input.change.affects_process_parameters
  not input.change.process_owner_approved
  msg := "Manufacturing process parameter changes require process owner approval"
}

# [Government] GOV-001
deny[msg] {
  input.change.includes_itar_code
  not input.change.export_control_reviewed
  msg := "ITAR-controlled code changes require export compliance review"
}

# [Government] GOV-002
deny[msg] {
  input.change.affects_classified_system
  not input.change.clearance_verified
  msg := "Classified system changes require security clearance verification"
}

# [Government] GOV-003
deny[msg] {
  input.change.grants_foreign_national_access
  not input.change.ciso_legal_approved
  msg := "Foreign national access changes require CISO and legal approval"
}

# [Government] GOV-004
deny[msg] {
  input.change.involves_ear_technology
  not input.change.ear_compliance_certified
  msg := "EAR technology transfer changes require compliance certification"
}

# [Government] GOV-005
deny[msg] {
  input.change.contract_milestone_impact
  not input.change.customer_notified
  msg := "Contract milestone deadline changes require customer notification"
}

# [Government] GOV-006
deny[msg] {
  input.change.interfaces_with_gov_system
  not input.change.fisma_compliance_audit
  msg := "Government system interface changes require FISMA compliance audit"
}

# [Government] GOV-007
deny[msg] {
  input.change.affects_dod_incident_plan
  not input.change.dod_approved
  msg := "Cybersecurity incident response plan changes require DoD approval"
}

# [Government] GOV-008
deny[msg] {
  input.change.affects_exfiltration_controls
  not input.change.secops_reviewed
  msg := "Data exfiltration controls changes require security operations review"
}

# [Government] GOV-009
deny[msg] {
  input.change.affects_cui_handling
  not input.change.cui_compliance_validated
  msg := "Controlled unclassified information (CUI) handling changes require compliance validation"
}

# [Government] GOV-010
deny[msg] {
  input.change.affects_facility_access
  not input.change.govt_site_approved
  msg := "Facility access control changes requiring government site visit approval"
}
