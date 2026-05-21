#!/usr/bin/env python3
"""Practice-question generator for the PMCOE PMP Tutor skill.

Returns one PMP exam-style scenario question from the seed bank, with four
choices, the correct answer, and a full rationale.

Usage:
    python3 practice-question-generator.py
    python3 practice-question-generator.py --domain people
    python3 practice-question-generator.py --domain process --difficulty hard
    python3 practice-question-generator.py --seed 42

Seed bank lives in `practice-question-bank.json` next to this script.
PMCOE owns the bank. All scenarios are anonymised composites — no identifying
information from any real student or cohort.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
BANK_PATH = HERE / "practice-question-bank.json"


def load_bank() -> list[dict[str, Any]]:
    if not BANK_PATH.exists():
        # Default seed bank so the script is self-sufficient.
        return DEFAULT_BANK
    with BANK_PATH.open() as f:
        return json.load(f)


DEFAULT_BANK: list[dict[str, Any]] = [
    {
        "id": "people-001",
        "domain": "people",
        "difficulty": "medium",
        "scenario": (
            "A project manager joins a software project mid-execution. Three of the "
            "eight team members are openly hostile to the new PM, regularly missing "
            "stand-ups and pushing back on every decision. The sponsor has asked the "
            "new PM to 'fix this in two weeks.' What is the BEST first action?"
        ),
        "choices": {
            "A": "Schedule one-on-one meetings with each team member to understand their concerns.",
            "B": "Escalate to the sponsor that the team is not functioning.",
            "C": "Reassign the three resisting team members.",
            "D": "Lead a team-building exercise to reset relationships.",
        },
        "correct": "A",
        "rationale": (
            "The PMP exam consistently rewards information-gathering before action, and "
            "individual conversations before escalation or reassignment. Option A "
            "addresses the root cause (unknown concerns); B abdicates leadership; C is "
            "premature and damages team morale; D is a tactic, not a diagnosis. Per "
            "PMI's framework, the PM understands stakeholder needs before applying any "
            "intervention."
        ),
    },
    {
        "id": "people-002",
        "domain": "people",
        "difficulty": "easy",
        "scenario": (
            "Two team members are in conflict over technical direction. Both are subject "
            "matter experts; both have strong opinions. The conflict is delaying delivery. "
            "What conflict-resolution mode is MOST appropriate?"
        ),
        "choices": {
            "A": "Avoiding — let them work it out.",
            "B": "Smoothing — emphasise areas of agreement.",
            "C": "Compromising — find a middle ground.",
            "D": "Collaborating — work toward a solution both accept.",
        },
        "correct": "D",
        "rationale": (
            "Collaborating (win-win) is the PMI-preferred mode when both parties have "
            "valid expertise and stake. Avoiding and Smoothing defer the issue; "
            "Compromising leaves both partially unsatisfied (lose-lose-light). "
            "Collaborating takes longest but produces the most durable resolution. "
            "Per Thomas-Kilmann Conflict Mode Instrument as adopted by PMI."
        ),
    },
    {
        "id": "process-001",
        "domain": "process",
        "difficulty": "hard",
        "scenario": (
            "A project has Earned Value (EV) of $80,000, Actual Cost (AC) of $100,000, "
            "and Planned Value (PV) of $90,000. The Cost Performance Index (CPI) is "
            "stable at this value through the project. The Budget at Completion (BAC) "
            "is $500,000. What is the Estimate at Completion (EAC) using the standard "
            "CPI-based formula?"
        ),
        "choices": {
            "A": "$400,000",
            "B": "$500,000",
            "C": "$555,555",
            "D": "$625,000",
        },
        "correct": "D",
        "rationale": (
            "CPI = EV / AC = 80,000 / 100,000 = 0.80. The EAC formula assuming current "
            "CPI continues: EAC = BAC / CPI = 500,000 / 0.80 = $625,000. Option A is "
            "BAC × CPI (wrong direction). B is BAC itself. C uses a different formula "
            "(BAC × something else). The PMP exam expects fluency with this formula and "
            "the inverse-direction trap — when CPI is below 1.0, EAC is greater than BAC."
        ),
    },
    {
        "id": "process-002",
        "domain": "process",
        "difficulty": "medium",
        "scenario": (
            "During sprint planning, the team commits to 40 story points. By the end of "
            "the sprint, they have completed 28 points and identify three stories that "
            "will not finish. The Product Owner asks the Scrum Master to add three more "
            "stories to the sprint to compensate. What should the Scrum Master do?"
        ),
        "choices": {
            "A": "Add the three stories as requested — the team has the capacity.",
            "B": "Refuse and remind the Product Owner that the sprint scope is fixed.",
            "C": "Facilitate a discussion between the Product Owner and the Development Team.",
            "D": "Move the unfinished stories to the next sprint without discussion.",
        },
        "correct": "C",
        "rationale": (
            "The Scrum Master facilitates; only the Development Team can change sprint "
            "scope, and they do so collaboratively with the Product Owner. Option A "
            "lets the Product Owner unilaterally change scope — wrong. B is rigid and "
            "skips conversation. D pre-empts the team's input. C is the servant-leader "
            "approach the PMP exam tests on agile-domain questions."
        ),
    },
    {
        "id": "business-001",
        "domain": "business",
        "difficulty": "medium",
        "scenario": (
            "Mid-project, the organisation's strategic priorities shift. The CEO "
            "announces a new direction that makes the current project's deliverables "
            "less valuable than originally planned. What is the BEST first step for "
            "the project manager?"
        ),
        "choices": {
            "A": "Continue execution until told otherwise — strategic shifts are above PM pay grade.",
            "B": "Halt the project immediately and await direction.",
            "C": "Re-validate the business case with the sponsor.",
            "D": "Begin reassigning resources to other initiatives.",
        },
        "correct": "C",
        "rationale": (
            "The Business Environment domain emphasises ongoing business-case validation, "
            "especially when strategic context changes. A is passive; B is rash; D is "
            "premature. The PM works with the sponsor to re-confirm whether the project "
            "still produces value under the new direction, and if not, formally proposes "
            "scope change or termination through the change-control process."
        ),
    },
]


def filter_bank(
    bank: list[dict[str, Any]],
    domain: str | None,
    difficulty: str | None,
) -> list[dict[str, Any]]:
    pool = bank
    if domain:
        pool = [q for q in pool if q["domain"] == domain]
    if difficulty:
        pool = [q for q in pool if q["difficulty"] == difficulty]
    return pool


def format_question(q: dict[str, Any]) -> str:
    out = [f"## Practice Question ({q['id']}, domain={q['domain']}, difficulty={q['difficulty']})"]
    out.append("")
    out.append(q["scenario"])
    out.append("")
    for letter, text in q["choices"].items():
        out.append(f"{letter}. {text}")
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"**Correct: {q['correct']}**")
    out.append("")
    out.append(q["rationale"])
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=["people", "process", "business"])
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"])
    parser.add_argument("--seed", type=int, help="Reproducible selection")
    args = parser.parse_args(argv)

    bank = load_bank()
    pool = filter_bank(bank, args.domain, args.difficulty)

    if not pool:
        print(
            f"No scenarios match domain={args.domain} difficulty={args.difficulty}.",
            file=sys.stderr,
        )
        return 1

    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    q = rng.choice(pool)
    print(format_question(q))
    return 0


if __name__ == "__main__":
    sys.exit(main())
