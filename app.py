from datetime import date, timedelta
from typing import Any

import streamlit as st


st.set_page_config(
    page_title="ShipReady AI | Submission readiness",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


DEFAULT_REQUIREMENTS = [
    "Project description and problem statement",
    "Working demo or deployment link",
    "Source code repository",
    "Demo video or presentation",
    "Team details and acknowledgements",
]


def initialize_state() -> None:
    if "project_name" not in st.session_state:
        st.session_state.project_name = ""
    if "deadline" not in st.session_state:
        st.session_state.deadline = date.today() + timedelta(days=14)
    if "requirements" not in st.session_state:
        st.session_state.requirements = [
            {
                "id": index,
                "name": name,
                "complete": False,
                "verified": False,
                "evidence": "",
                "notes": "",
            }
            for index, name in enumerate(DEFAULT_REQUIREMENTS)
        ]
    if "next_requirement_id" not in st.session_state:
        st.session_state.next_requirement_id = len(st.session_state.requirements)


def build_report(
    project_name: str,
    deadline: date,
    requirements: list[dict[str, Any]],
    readiness: int,
) -> str:
    completed_count = sum(item["complete"] for item in requirements)
    verified_count = sum(item["verified"] for item in requirements)
    lines = [
        "SHIPREADY AI — HACKATHON SUBMISSION READINESS REPORT",
        "=" * 58,
        f"Project: {project_name.strip() or 'Untitled project'}",
        f"Deadline: {deadline.isoformat()}",
        f"User-reported readiness: {readiness}% ({completed_count}/{len(requirements)} marked complete)",
        f"Independently verified: {verified_count}/{len(requirements)}",
        "",
        "STATUS NOTE",
        "Completion is self-reported by the project team. A verified status is a separate",
        "reviewer attestation; ShipReady AI does not open links or independently validate evidence.",
        "",
        "REQUIREMENTS",
        "-" * 58,
    ]
    for item in requirements:
        lines.extend(
            [
                f"[{'x' if item['complete'] else ' '}] {item['name'] or 'Untitled requirement'}",
                f"    User-reported: {'Complete' if item['complete'] else 'Incomplete'}",
                f"    Independently verified: {'Yes (reviewer-marked)' if item['verified'] else 'No'}",
                f"    Evidence: {item['evidence'].strip() or 'Not provided'}",
                f"    Notes: {item['notes'].strip() or 'None'}",
                "",
            ]
        )
    missing = [
        item["name"] or "Untitled requirement"
        for item in requirements
        if not item["complete"]
    ]
    lines.extend(["MISSING REQUIREMENTS", "-" * 58])
    if missing:
        lines.extend(f"- {name}" for name in missing)
    else:
        lines.append("None — all requirements are marked complete.")
    lines.extend(
        [
            "",
            "This report reflects the information entered by the user and is not an",
            "official confirmation of hackathon submission or evidence validity.",
        ]
    )
    return "\n".join(lines)


initialize_state()

st.markdown(
    """
    <style>
    .stApp { background: #f5f7fb; }
    .block-container { max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem; }
    .hero {
        background: linear-gradient(120deg, #111c3a 0%, #233b71 58%, #3159a6 100%);
        color: white; padding: 2rem 2.2rem; border-radius: 18px; margin-bottom: 1.25rem;
    }
    .hero h1 { color: white; margin: 0 0 .45rem 0; font-size: 2.2rem; }
    .hero p { color: #dce7ff; margin: 0; font-size: 1.05rem; }
    .subtle { color: #5d6880; font-size: .92rem; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e4e9f2; padding: 1rem 1.15rem;
        border-radius: 13px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🚀 ShipReady AI</h1>
      <p>Your clear, calm checklist for a confident hackathon submission.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="subtle">Track what your team says is complete, attach evidence, '
    "and record a separate reviewer verification status.</p>",
    unsafe_allow_html=True,
)

with st.container():
    project_col, deadline_col = st.columns([2, 1])
    with project_col:
        st.text_input(
            "Project name",
            key="project_name",
            placeholder="e.g. GreenRoute",
            help="The project name shown in your downloadable report.",
        )
    with deadline_col:
        st.date_input("Submission deadline", key="deadline")


requirements: list[dict[str, Any]] = st.session_state.requirements

# Synchronize checkbox state before calculating the dashboard.
for item in requirements:
    requirement_id = item["id"]
    item["complete"] = bool(
        st.session_state.get(
            f"requirement_complete_{requirement_id}",
            item["complete"],
        )
    )
    item["verified"] = bool(
        st.session_state.get(
            f"requirement_verified_{requirement_id}",
            item["verified"],
        )
    )

total_requirements = len(requirements)
completed_count = sum(item["complete"] for item in requirements)
verified_count = sum(item["verified"] for item in requirements)
readiness = (
    round(completed_count / total_requirements * 100)
    if total_requirements
    else 0
)
missing_requirements = [
    item for item in requirements if not item["complete"]
]


metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("User-reported readiness", f"{readiness}%")
metric_col2.metric("Marked complete", f"{completed_count} / {total_requirements}")
metric_col3.metric("Independently verified", f"{verified_count} / {total_requirements}")
st.progress(readiness, text=f"{readiness}% of requirements marked complete by your team")

st.markdown("### Submission requirements")
st.markdown(
    '<p class="subtle">“Complete” is your team’s report. “Verified” is a separate '
    "reviewer attestation; links are not automatically opened or validated.</p>",
    unsafe_allow_html=True,
)

removed_ids: list[int] = []
for item in requirements:
    requirement_id = item["id"]
    with st.container(border=True):
        title_col, remove_col = st.columns([8, 1])
        with title_col:
            item["name"] = st.text_input(
                "Requirement",
                value=item["name"],
                key=f"requirement_name_{requirement_id}",
                label_visibility="collapsed",
                placeholder="Name this submission requirement",
            )
        with remove_col:
            if st.button("Remove", key=f"remove_requirement_{requirement_id}"):
                removed_ids.append(requirement_id)

        status_col, verified_col = st.columns(2)
        with status_col:
            item["complete"] = st.checkbox(
                "Marked complete by my team",
                value=bool(item["complete"]),
                key=f"requirement_complete_{requirement_id}",
            )
        with verified_col:
            item["verified"] = st.checkbox(
                "Independently verified by a reviewer",
                value=bool(item["verified"]),
                key=f"requirement_verified_{requirement_id}",
                help="Check only after a reviewer has separately inspected the evidence.",
            )
        evidence_col, notes_col = st.columns(2)
        with evidence_col:
            item["evidence"] = st.text_input(
                "Evidence link",
                value=item["evidence"],
                key=f"requirement_evidence_{requirement_id}",
                placeholder="https://…",
            )
        with notes_col:
            item["notes"] = st.text_input(
                "Notes",
                value=item["notes"],
                key=f"requirement_notes_{requirement_id}",
                placeholder="Owner, follow-up, or context",
            )

if removed_ids:
    st.session_state.requirements = [
        item for item in requirements if item["id"] not in removed_ids
    ]
    st.rerun()

if st.button("＋ Add requirement", type="secondary"):
    requirement_id = st.session_state.next_requirement_id
    st.session_state.next_requirement_id += 1
    st.session_state.requirements.append(
        {
            "id": requirement_id,
            "name": "",
            "complete": False,
            "verified": False,
            "evidence": "",
            "notes": "",
        }
    )
    st.rerun()

st.markdown("### Readiness check")
if not requirements:
    st.info("Add at least one requirement to calculate your submission readiness.")
elif missing_requirements:
    st.warning(
        f"{len(missing_requirements)} requirement"
        f"{'s are' if len(missing_requirements) != 1 else ' is'} still marked incomplete. "
        "Review the items below before submitting."
    )
    for item in missing_requirements:
        st.markdown(f"- {item['name'].strip() or 'Untitled requirement'}")
else:
    st.success("All listed requirements are marked complete by your team.")

completed_without_evidence = [
    item for item in requirements if item["complete"] and not item["evidence"].strip()
]
if completed_without_evidence:
    st.warning(
        f"{len(completed_without_evidence)} completed requirement"
        f"{'s have' if len(completed_without_evidence) != 1 else ' has'} no evidence link yet."
    )

unverified_completed = [
    item for item in requirements if item["complete"] and not item["verified"]
]
if unverified_completed:
    st.info(
        f"{len(unverified_completed)} team-reported completed item"
        f"{'s have' if len(unverified_completed) != 1 else ' has'} not been marked "
        "independently verified. A link alone does not count as verification."
    )

report = build_report(
    st.session_state.project_name,
    st.session_state.deadline,
    requirements,
    readiness,
)
filename = "shipready-report.txt"
st.download_button(
    "⬇ Download readiness report",
    data=report,
    file_name=filename,
    mime="text/plain",
    type="primary",
    use_container_width=True,
)
st.caption(
    "Your project details and checklist are kept in this Streamlit session. "
    "The report distinguishes self-reported completion from reviewer-marked verification."
)