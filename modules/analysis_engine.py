
from typing import Any


def analyze_research(research: dict[str, Any]) -> dict[str, Any]:


    objectives = research.get("objectives", [])
    findings = research.get("findings", [])
    limitations = research.get("limitations", [])
    publications = research.get("publications", [])

    setup = research.get("experimental_setup", {})

    if not isinstance(setup, dict):
        setup = {}

    fuel_materials = setup.get("fuel_materials", [])
    hardware = setup.get("hardware", [])

    if not isinstance(objectives, list):
        objectives = []

    if not isinstance(findings, list):
        findings = []

    if not isinstance(limitations, list):
        limitations = []

    if not isinstance(publications, list):
        publications = []

    if not isinstance(fuel_materials, list):
        fuel_materials = []

    if not isinstance(hardware, list):
        hardware = []

    evidence_gaps = []

    if not findings:
        evidence_gaps.append(
            "Experimental findings have not been extracted."
        )

    if not limitations:
        evidence_gaps.append(
            "No research limitations are documented."
        )

    insights = []

    if objectives:
        insights.append({
            "category": "Research scope",
            "observation": (
                f"The investigation contains "
                f"{len(objectives)} documented objectives."
            ),
            "basis": "Research objectives"
        })

    if fuel_materials:
        insights.append({
            "category": "Experimental coverage",
            "observation": (
                f"The investigation documents "
                f"{len(fuel_materials)} fuel materials."
            ),
            "basis": "Experimental setup"
        })

    extinguishing_agent = research.get("extinguishing_agent", {})

    if isinstance(extinguishing_agent, dict):
        agent_type = extinguishing_agent.get("type")
        agent_purpose = extinguishing_agent.get("purpose")

        if agent_type:
            observation = (
                f"{agent_type.capitalize()} is documented as "
                "the gaseous flame suppression agent. "
                "Its effectiveness is not established by the "
                "currently extracted findings."
            )

            if agent_purpose:
                observation += f" Purpose: {agent_purpose}."

            insights.append({
                "category": "Fire suppression",
                "observation": observation,
                "basis": "Research metadata"
            })

    if not findings:
        evidence_status = "Insufficient extracted evidence"
    else:
        evidence_status = "Findings available for review"

    return {
        "research_id": research.get("id", "UNKNOWN"),
        "analysis_version": "1.0",
        "method": "Structured evidence analysis",
        "evidence_status": evidence_status,
        "statistics": {
            "objectives": len(objectives),
            "findings": len(findings),
            "limitations": len(limitations),
            "publications": len(publications),
            "fuel_materials": len(fuel_materials),
            "hardware_components": len(hardware)
        },
        "insights": insights,
        "evidence_gaps": evidence_gaps,
        "documented_limitations": limitations
    }
