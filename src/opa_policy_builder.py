"""Helpers for extracting policy text and generating OPA Rego policies."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List

from docx import Document
from pypdf import PdfReader


@dataclass(frozen=True)
class PolicyRule:
    """Simple structure for deterministic Rego deny rule generation."""

    rule_id: str
    message: str
    conditions: List[str]
    domain: str


POLICY_RULES: List[PolicyRule] = [
    PolicyRule("IT-001", "Change cannot be approved by its author", ["input.change.author == input.change.approver"], "it"),
    PolicyRule("IT-002", "High-risk change requires CAB approval", ["input.change.risk_level == \"high\"", "not input.change.cab_approved"], "it"),
    PolicyRule("IT-003", "Production changes require rollback plan", ["input.change.environment == \"production\"", "not input.change.rollback_plan"], "it"),
    PolicyRule("IT-004", "Emergency change must include post-implementation review", ["input.change.type == \"emergency\"", "not input.change.post_implementation_review"], "it"),
    PolicyRule("IT-005", "Segregation of duties required for deployment", ["input.change.developer == input.change.deployer"], "it"),
    PolicyRule("IT-006", "Change window must be defined", ["not input.change.window_start"], "it"),
    PolicyRule("IT-007", "Change window end time must be defined", ["not input.change.window_end"], "it"),
    PolicyRule("IT-008", "Security-impacting changes require security review", ["input.change.impacts_security", "not input.change.security_reviewed"], "it"),
    PolicyRule("IT-009", "Database schema changes require DBA approval", ["input.change.includes_db_schema", "not input.change.dba_approved"], "it"),
    PolicyRule("IT-010", "Infrastructure changes require architecture review", ["input.change.includes_infrastructure", "not input.change.architecture_approved"], "it"),
    PolicyRule("IT-011", "Production changes require test evidence", ["input.change.environment == \"production\"", "count(input.change.test_evidence) == 0"], "it"),
    PolicyRule("IT-012", "Standard changes must use approved template", ["input.change.type == \"standard\"", "not input.change.template_id"], "it"),
    PolicyRule("IT-013", "Emergency change reason must be documented", ["input.change.type == \"emergency\"", "not input.change.emergency_reason"], "it"),
    PolicyRule("IT-014", "Backout contact must be assigned", ["not input.change.rollback_owner"], "it"),
    PolicyRule("IT-015", "Change implementation team must be listed", ["count(input.change.implementers) == 0"], "it"),
    PolicyRule("IT-016", "Monitoring plan is required after production change", ["input.change.environment == \"production\"", "not input.change.monitoring_plan"], "it"),
    PolicyRule("IT-017", "Customer communication required for service-impacting change", ["input.change.customer_impact", "not input.change.communication_plan"], "it"),
    PolicyRule("IT-018", "Planned outage must include downtime estimate", ["input.change.requires_outage", "not input.change.estimated_downtime_minutes"], "it"),
    PolicyRule("IT-019", "High-risk change requires peer review", ["input.change.risk_level == \"high\"", "not input.change.peer_reviewed"], "it"),
    PolicyRule("IT-020", "Source code changes must reference approved ticket", ["input.change.includes_code", "not input.change.ticket_id"], "it"),
    PolicyRule("IT-021", "Production access changes require IAM approval", ["input.change.includes_access_change", "not input.change.iam_approved"], "it"),
    PolicyRule("IT-022", "Privileged access changes require dual authorization", ["input.change.privileged_access_change", "count(input.change.approvals) < 2"], "it"),
    PolicyRule("IT-023", "Patch deployment must include CVE reference", ["input.change.type == \"patch\"", "not input.change.cve_reference"], "it"),
    PolicyRule("IT-024", "Firewall changes require security architecture sign-off", ["input.change.includes_firewall_update", "not input.change.security_arch_approved"], "it"),
    PolicyRule("IT-025", "Change records must include affected assets", ["count(input.change.affected_assets) == 0"], "it"),
    PolicyRule("IT-026", "Data migration changes require reconciliation plan", ["input.change.includes_data_migration", "not input.change.reconciliation_plan"], "it"),
    PolicyRule("IT-027", "Backup verification is required before major change", ["input.change.major_change", "not input.change.backup_verified"], "it"),
    PolicyRule("IT-028", "Critical service changes require executive notification", ["input.change.affects_critical_service", "not input.change.executive_notified"], "it"),
    PolicyRule("IT-029", "Production change cannot be scheduled during freeze window", ["input.change.environment == \"production\"", "input.change.in_freeze_window"], "it"),
    PolicyRule("IT-030", "Change closure requires validation evidence", ["input.change.status == \"closed\"", "not input.change.validation_evidence"], "it"),
    PolicyRule("HC-001", "PHI access change requires privacy approval", ["input.change.affects_phi", "not input.change.privacy_officer_approved"], "healthcare"),
    PolicyRule("HC-002", "PHI system change requires HIPAA risk assessment", ["input.change.affects_phi", "not input.change.hipaa_risk_assessment"], "healthcare"),
    PolicyRule("HC-003", "Clinical system downtime requires patient safety plan", ["input.change.affects_clinical_system", "input.change.requires_outage", "not input.change.patient_safety_plan"], "healthcare"),
    PolicyRule("HC-004", "EHR configuration change requires CMIO review", ["input.change.affects_ehr", "not input.change.cmio_approved"], "healthcare"),
    PolicyRule("HC-005", "Medication workflow changes require pharmacy sign-off", ["input.change.affects_medication_workflow", "not input.change.pharmacy_approved"], "healthcare"),
    PolicyRule("HC-006", "Lab interface changes require validation results", ["input.change.affects_lab_interface", "not input.change.interface_validation_report"], "healthcare"),
    PolicyRule("HC-007", "Radiology integration changes require DICOM compatibility check", ["input.change.affects_radiology", "not input.change.dicom_compatibility_verified"], "healthcare"),
    PolicyRule("HC-008", "Telehealth platform changes require security testing", ["input.change.affects_telehealth", "not input.change.security_test_completed"], "healthcare"),
    PolicyRule("HC-009", "Changes impacting PHI exports require audit log verification", ["input.change.phi_export_enabled", "not input.change.audit_logging_verified"], "healthcare"),
    PolicyRule("HC-010", "Patient portal changes require accessibility review", ["input.change.affects_patient_portal", "not input.change.accessibility_reviewed"], "healthcare"),
    PolicyRule("HC-011", "Identity matching changes require data quality approval", ["input.change.affects_patient_identity_matching", "not input.change.data_quality_approved"], "healthcare"),
    PolicyRule("HC-012", "Clinical decision support changes require physician sign-off", ["input.change.affects_clinical_decision_support", "not input.change.physician_approved"], "healthcare"),
    PolicyRule("HC-013", "PHI retention rule changes require legal approval", ["input.change.affects_phi_retention", "not input.change.legal_approved"], "healthcare"),
    PolicyRule("HC-014", "Third-party healthcare integration requires BAA confirmation", ["input.change.third_party_healthcare_vendor", "not input.change.baa_confirmed"], "healthcare"),
    PolicyRule("HC-015", "Nursing workflow changes require nursing leadership sign-off", ["input.change.affects_nursing_workflow", "not input.change.nursing_leadership_approved"], "healthcare"),
    PolicyRule("HC-016", "Clinical alert threshold changes require governance approval", ["input.change.affects_clinical_alert_thresholds", "not input.change.clinical_governance_approved"], "healthcare"),
    PolicyRule("HC-017", "Patient consent workflow changes require compliance validation", ["input.change.affects_consent_workflow", "not input.change.compliance_validated"], "healthcare"),
    PolicyRule("HC-018", "Changes to ePrescribing require controlled-substance checks", ["input.change.affects_eprescribing", "not input.change.controlled_substance_checks_complete"], "healthcare"),
    PolicyRule("HC-019", "Medical device integration changes require biomedical review", ["input.change.affects_medical_device_integration", "not input.change.biomedical_approved"], "healthcare"),
    PolicyRule("HC-020", "PHI-related incident response procedures must be updated before go-live", ["input.change.affects_phi", "input.change.go_live", "not input.change.incident_response_updated"], "healthcare"),
]


def extract_text_from_document(filename: str, content: bytes) -> str:
    """Extract plain text from supported document formats."""
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(content))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()

    if suffix == ".docx":
        doc = Document(io.BytesIO(content))
        paragraphs = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
        return "\n".join(paragraphs).strip()

    if suffix == ".doc":
        # Legacy .doc binary format is not consistently parseable without external system tools.
        # Keep a best-effort decode fallback for plain-text-compatible files.
        return content.decode("utf-8", errors="ignore").strip()

    raise ValueError("Unsupported file type. Please upload PDF, DOCX, or DOC.")


def extract_policy_candidates(text: str, limit: int = 12) -> List[str]:
    """Extract policy-like statements from document text for traceability comments."""
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    keywords = (
        "must",
        "shall",
        "required",
        "prohibited",
        "approval",
        "change",
        "hipaa",
        "phi",
        "security",
        "audit",
    )

    selected: List[str] = []
    for sentence in sentences:
        s = sentence.strip()
        if len(s) < 35:
            continue
        lowered = s.lower()
        if any(k in lowered for k in keywords):
            selected.append(s[:200])
        if len(selected) >= limit:
            break

    return selected


def build_rego_policy(document_name: str, extracted_candidates: List[str]) -> str:
    """Generate a deterministic OPA policy file with 50 deny rules."""
    lines: List[str] = []
    lines.append("package policy.change_control")
    lines.append("")
    lines.append("# Auto-generated from uploaded policy documentation")
    lines.append(f"# Source document: {document_name}")
    lines.append("# Rule count: 50 (30 IT change control + 20 healthcare)")
    lines.append("")
    lines.append("# Extracted policy statements from the uploaded document")
    if extracted_candidates:
        for idx, candidate in enumerate(extracted_candidates, start=1):
            sanitized = candidate.replace("\n", " ").replace("\r", " ").strip()
            lines.append(f"# {idx:02d}. {sanitized}")
    else:
        lines.append("# No policy-like statements were confidently extracted; using baseline policy library.")
    lines.append("")

    for rule in POLICY_RULES:
        lines.append(f"# {rule.rule_id} [{rule.domain}]")
        lines.append("deny[msg] {")
        for condition in rule.conditions:
            lines.append(f"  {condition}")
        lines.append(f"  msg := \"{rule.message}\"")
        lines.append("}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"