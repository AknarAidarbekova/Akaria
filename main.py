import streamlit as st
from pathlib import Path
from typing import Any

from modules.data_loader import (
load_research_data,
load_research_registry
)

from modules.analysis_engine import analyze_research
from modules.psi_collector import search_psi_investigations

base_dir = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Akaria: Space Fire Intelligence",
    page_icon="🚀",
    layout="wide"
)


@st.cache_data
def get_registry() -> list[dict[str, Any]]:
    registry_path = base_dir / "data" / "metadata" / "research_registry.json"
    return load_research_registry(registry_path)

def get_full_research(research_record_source: dict[str, Any]) -> dict[str, Any]:
    relative_path = research_record_source.get("file")

    if not isinstance(relative_path, str):
        raise ValueError("Invalid research file path")

    file_path = base_dir / relative_path
    data = load_research_data(file_path)

    if not isinstance(data, dict):
        raise ValueError("Research data must be a dictionary")

    return load_research_data(file_path)

try:
    investigations = get_registry()
except Exception as error:
    st.error(f"Could not load research registry: {error}")
    st.stop()


st.sidebar.title("Akaria")
st.sidebar.caption("Space Fire Intelligence")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Research Explorer", "NASA Search"]
)


if page == "Dashboard":

    st.title("Space Fire Intelligence")
    st.write(
        "Understanding combustion research "
        "for safer human space exploration."
    )

    available = [
        item for item in investigations
        if item.get("status") == "available"
    ]

    planned = [
        item for item in investigations
        if item.get("status") == "planned"
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Investigations", len(investigations))
    col2.metric("Available", len(available))
    col3.metric("Planned", len(planned))

    st.divider()

    st.subheader("Available research")

    for research_record in available:
        st.markdown(f" {research_record['name']}")
        st.caption(f"Research ID: {research_record['id']}")

    st.info(
        "Akaria transforms scientific research "
        "into structured knowledge for spacecraft fire safety."
    )

elif page == "Research Explorer":

    st.title("Research Explorer")
    st.write("Explore NASA microgravity combustion investigations.")

    if not investigations:
        st.warning("No investigations found.")
        st.stop()

    selected_record = st.selectbox(
        "Select an investigation",
        options=investigations,
        format_func=lambda sel_record: (
            f"{sel_record.get('id', 'UNKNOWN')} — "
            f"{sel_record.get('name', 'Unnamed research')}"
        )
    )

    if selected_record is None:
        st.warning("No investigations selected.")
        st.stop()


    try:
        research = get_full_research(selected_record)
    except Exception as error:
        st.error(f"Could not load investidation: {error}")
        st.stop()

    st.divider()

    st.header(
        research.get(
        "name",
        selected_record.get("name", "Unnamed research")))

    metadata = research.get("metadata", {})

    col1, col2, col3 = st.columns(3)

    col1.metric("Research ID", research.get("id", "N/A"))
    col2.metric("Start Date", metadata.get("start_date", "N/A"))
    col3.metric("End Date", metadata.get("end_date", "N/A"))

    st.subheader("Overview")

    st.write(f"Program: {research.get('program', 'N/A')}")
    st.write(f"Project type: {research.get('project_type', 'N/A')}")
    st.write(f"Research type: {research.get('research_type', 'N/A')}")

    st.subheader("Research objectives")

    for objective in research.get("objectives", []):
        st.markdown(f"- {objective}")

    st.subheader("Experimental setup")

    setup = research.get("experimental_setup", {})

    st.write(f"Location: {setup.get('location', 'N/A')}")

    st.write(f"Hardware:")
    for hardware in setup.get("hardware", []):
        st.markdown(f"- {hardware}")

    st.write(f"Fuel materials:")
    for material in setup.get("fuel_materials", []):
        st.markdown(f"- {material}")

    st.divider()

    st.header(f"Akaria Intelligence Report")

    analysis = analyze_research(research)

    st.subheader("Evidence Status")
    st.info(analysis["evidence_status"])

    st.subheader("Research Statistics")
    stats = analysis["statistics"]

    clo1, clo2, clo3 = st.columns(3)

    col1.metric("Objectives", stats["objectives"])
    col2.metric("Findings", stats["findings"])
    col3.metric("Publications", stats["publications"])

    col4, col5, col6 = st.columns(3)

    col4.metric("Fuel Materials", stats["fuel_materials"])
    col5.metric("Hardware Components", stats["hardware_components"])
    col6.metric("Limitations", stats["limitations"])

    st.subheader("Analytical Insights")

    if analysis["evidence_gaps"]:
        for insight in analysis["insights"]:
            with st.container(border=True):
                st.markdown(f"- {insight["category"]}")
                st.write(insight["observation"])
                st.caption(f"Evidence basis: {insight['basis']}")

    else:
        st.info("No structured insights available.")

    st.subheader("Evidence Gap")

    if analysis["evidence_gaps"]:
        for gap in analysis["evidence_gaps"]:
            st.warning(gap)

    else:
        st.success("No documented evidence gaps detected.")

    st.caption(
        f"Analysis method: {analysis['method']} | "
        f"Version: {analysis['analysis_version']}"
    )


    st.subheader("Research findings")

    findings = research.get("findings", [])

    if findings:
        for finding in findings:
            st.write(f"- {finding}")
    else:
        st.info(
            "Detailed experimental findings "
            "have not yet been extracted."
        )

    st.subheader("Research Limitations")

    for limitation in research.get("limitations", []):
        st.markdown(f"- {limitation}")

    st.subheader("Publications")

    for publication in research.get("publications", []):
        title = publication.get("title", "Untitled")
        doi = publication.get("doi")

        st.markdown(f"{title}")

        if doi:
            st.markdown(f"Doi: {doi}")

elif page == "NASA Search":

    st.title("NASA Research Search")

    st.write(
        "Search NASA Physical Sciences Informatics "
        "for microgravity investigations."
    )

    query = st.text_input(
        "Search scientific research",
        placeholder="e.g. combustion, flame, fire safety"
    )

    limit = st.slider(
        "Maximum results",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )

    if st.button("Search NASA", type="primary"):

        if not query or not query.strip():
            st.warning("Enter a search query.")
        else:
            with st.spinner("Searching NASA PSI..."):

                result = search_psi_investigations(
                    query.strip() if query else "",
                    limit=limit
                )

            if not result["success"]:
                st.error(
                    f"NASA PSI search failed: {result['error']}"
                )

            else:
                records = result["records"]

                st.success(
                    f"Found {result['total']} investigations. "
                    f"Retrieved {len(records)}."
                )

                for record in records:

                    with st.expander(
                        f"{record.get('Accession', 'N/A')} — "
                        f"{record.get('Title', 'Untitled')}"
                    ):

                        st.write(
                            "**Research area:**",
                            record.get("Research Area", "N/A")
                        )

                        st.write(
                            "**Flight platform:**",
                            record.get("Flight Platform", "N/A")
                        )

                        st.write("**Objectives:**")
                        st.write(
                            record.get("Objectives", "Not available")
                        )

                        st.write("**Approach:**")
                        st.write(
                            record.get("Approach", "Not available")
                        )

                        st.write("**Hypothesis:**")
                        st.write(
                            record.get("Hypothesis", "Not available")
                        )