"""Helpers for extracting policy text and generating OPA Rego policies."""

from __future__ import annotations

import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

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
    PolicyRule("MFG-001", "OT system changes require operational safety assessment", ["input.change.affects_ot_system", "not input.change.safety_assessment_completed"], "manufacturing"),
    PolicyRule("MFG-002", "Production line changes require manufacturing engineer approval", ["input.change.affects_production_line", "not input.change.manufacturing_engineer_approved"], "manufacturing"),
    PolicyRule("MFG-003", "Critical equipment modification requires equipment specialist sign-off", ["input.change.affects_critical_equipment", "not input.change.equipment_specialist_approved"], "manufacturing"),
    PolicyRule("MFG-004", "Supply chain integration changes require vendor verification", ["input.change.affects_supply_chain_system", "not input.change.vendor_verified"], "manufacturing"),
    PolicyRule("MFG-005", "Inventory management changes require reconciliation audit", ["input.change.affects_inventory_system", "not input.change.reconciliation_audit_completed"], "manufacturing"),
    PolicyRule("MFG-006", "Maintenance system changes require maintenance team approval", ["input.change.affects_maintenance_system", "not input.change.maintenance_lead_approved"], "manufacturing"),
    PolicyRule("MFG-007", "Quality control system changes require QA director sign-off", ["input.change.affects_quality_control", "not input.change.qa_director_approved"], "manufacturing"),
    PolicyRule("MFG-008", "Plant safety system changes require facility manager authorization", ["input.change.affects_safety_system", "not input.change.facility_manager_approved"], "manufacturing"),
    PolicyRule("MFG-009", "OT network changes require industrial control system security review", ["input.change.affects_ot_network", "not input.change.ics_security_reviewed"], "manufacturing"),
    PolicyRule("MFG-010", "Manufacturing process parameter changes require process owner approval", ["input.change.affects_process_parameters", "not input.change.process_owner_approved"], "manufacturing"),
    PolicyRule("GOV-001", "ITAR-controlled code changes require export compliance review", ["input.change.includes_itar_code", "not input.change.export_control_reviewed"], "government"),
    PolicyRule("GOV-002", "Classified system changes require security clearance verification", ["input.change.affects_classified_system", "not input.change.clearance_verified"], "government"),
    PolicyRule("GOV-003", "Foreign national access changes require CISO and legal approval", ["input.change.grants_foreign_national_access", "not input.change.ciso_legal_approved"], "government"),
    PolicyRule("GOV-004", "EAR technology transfer changes require compliance certification", ["input.change.involves_ear_technology", "not input.change.ear_compliance_certified"], "government"),
    PolicyRule("GOV-005", "Contract milestone deadline changes require customer notification", ["input.change.contract_milestone_impact", "not input.change.customer_notified"], "government"),
    PolicyRule("GOV-006", "Government system interface changes require FISMA compliance audit", ["input.change.interfaces_with_gov_system", "not input.change.fisma_compliance_audit"], "government"),
    PolicyRule("GOV-007", "Cybersecurity incident response plan changes require DoD approval", ["input.change.affects_dod_incident_plan", "not input.change.dod_approved"], "government"),
    PolicyRule("GOV-008", "Data exfiltration controls changes require security operations review", ["input.change.affects_exfiltration_controls", "not input.change.secops_reviewed"], "government"),
    PolicyRule("GOV-009", "Controlled unclassified information (CUI) handling changes require compliance validation", ["input.change.affects_cui_handling", "not input.change.cui_compliance_validated"], "government"),
    PolicyRule("GOV-010", "Facility access control changes requiring government site visit approval", ["input.change.affects_facility_access", "not input.change.govt_site_approved"], "government"),
]

DOMAIN_DISPLAY_ORDER = {
    "it": 0,
    "manufacturing": 1,
    "government": 2,
}

DOMAIN_LABELS = {
    "it": "IT",
    "manufacturing": "Manufacturing",
    "government": "Government",
}

DOMAIN_KEYWORDS = {
    "it": (
        "it",
        "change",
        "deployment",
        "security",
        "database",
        "infrastructure",
        "cab",
        "iam",
        "firewall",
    ),
    "manufacturing": (
        "manufacturing",
        "ot",
        "production line",
        "plant",
        "industrial",
        "equipment",
        "quality control",
        "maintenance",
        "ics",
    ),
    "government": (
        "government",
        "contract",
        "itar",
        "ear",
        "fisma",
        "dod",
        "cui",
        "classified",
        "export control",
        "clearance",
    ),
}


def _domain_label(domain: str) -> str:
    return DOMAIN_LABELS.get(domain, domain.upper())


def _sorted_rules(rules: List[PolicyRule]) -> List[PolicyRule]:
    return sorted(
        rules,
        key=lambda rule: (
            DOMAIN_DISPLAY_ORDER.get(rule.domain, 99),
            _domain_label(rule.domain),
            rule.rule_id,
        ),
    )


def _domain_is_relevant(source_text: str, domain: str) -> bool:
    lowered = source_text.lower()
    return any(keyword in lowered for keyword in DOMAIN_KEYWORDS.get(domain, ()))


def select_policy_rules(document_text: str) -> List[PolicyRule]:
    """Select policies relevant to uploaded content, then return them label-sorted."""
    text = re.sub(r"\s+", " ", document_text or "").strip()
    if not text:
        return _sorted_rules(POLICY_RULES)

    selected_domains = {
        domain for domain in DOMAIN_KEYWORDS if _domain_is_relevant(text, domain)
    }

    # Keep baseline IT controls in all generated policies; add other domains when relevant.
    selected_domains.add("it")

    selected_rules = [
        rule for rule in POLICY_RULES if rule.domain in selected_domains
    ]

    return _sorted_rules(selected_rules)


def count_rules_by_domain(rules: List[PolicyRule]) -> Dict[str, int]:
    """Return per-domain counts using display labels as keys."""
    counts: Dict[str, int] = {}
    for rule in rules:
        label = _domain_label(rule.domain)
        counts[label] = counts.get(label, 0) + 1
    return counts


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
        "security",
        "audit",
        "itar",
        "export",
        "compliance",
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


def build_rego_policy(document_name: str, extracted_candidates: List[str], selected_rules: List[PolicyRule]) -> str:
    """Generate deterministic OPA policy file with label-grouped deny rules."""
    lines: List[str] = []
    lines.append("package policy.change_control")
    lines.append("")
    lines.append("# Auto-generated from uploaded policy documentation")
    lines.append(f"# Source document: {document_name}")
    lines.append(f"# Rule count: {len(selected_rules)}")

    domain_counts = count_rules_by_domain(selected_rules)
    if domain_counts:
        domain_summary = ", ".join(
            f"{label}: {count}" for label, count in domain_counts.items()
        )
        lines.append(f"# Domain labels: {domain_summary}")
    lines.append("")
    lines.append("# Extracted policy statements from the uploaded document")
    if extracted_candidates:
        for idx, candidate in enumerate(extracted_candidates, start=1):
            sanitized = candidate.replace("\n", " ").replace("\r", " ").strip()
            lines.append(f"# {idx:02d}. {sanitized}")
    else:
        lines.append("# No policy-like statements were confidently extracted; using baseline policy library.")
    lines.append("")

    for rule in selected_rules:
        lines.append(f"# [{_domain_label(rule.domain)}] {rule.rule_id}")
        lines.append("deny[msg] {")
        for condition in rule.conditions:
            lines.append(f"  {condition}")
        lines.append(f"  msg := \"{rule.message}\"")
        lines.append("}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"