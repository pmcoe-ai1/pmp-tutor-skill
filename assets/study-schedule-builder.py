#!/usr/bin/env python3
"""Study schedule builder for the PMCOE PMP Tutor skill.

Generates a week-by-week PMP study schedule tailored to the student's
available weeks, hours per week, and self-identified strengths / weaknesses.

Usage:
    python3 study-schedule-builder.py --weeks 8 --hours-per-week 12
    python3 study-schedule-builder.py --weeks 6 --hours-per-week 15 \\
        --strengths people --weaknesses process,business

Domain weights from the 2021 PMI Exam Content Outline:
    People 42%, Process 50%, Business Environment 8%.

Time allocation is biased toward the student's stated weaknesses and away
from their stated strengths, while keeping the relative balance close to
the exam mix.
"""

from __future__ import annotations

import argparse
import sys

ECO_WEIGHTS = {
    "people": 0.42,
    "process": 0.50,
    "business": 0.08,
}

DOMAIN_PRETTY = {
    "people": "People",
    "process": "Process",
    "business": "Business Environment",
}


def parse_csv(s: str | None) -> set[str]:
    if not s:
        return set()
    parts = {p.strip().lower() for p in s.split(",") if p.strip()}
    invalid = parts - set(ECO_WEIGHTS)
    if invalid:
        raise ValueError(f"Unknown domain(s): {', '.join(invalid)}. Valid: people, process, business.")
    return parts


def adjusted_weights(strengths: set[str], weaknesses: set[str]) -> dict[str, float]:
    """Down-weight strengths and up-weight weaknesses while preserving total."""
    weights = dict(ECO_WEIGHTS)
    for d in strengths:
        weights[d] *= 0.7  # 30% less study time on strengths
    for d in weaknesses:
        weights[d] *= 1.4  # 40% more study time on weaknesses
    total = sum(weights.values())
    return {d: w / total for d, w in weights.items()}


def build_week_plan(week_num: int, total_weeks: int, hours: float, weights: dict[str, float]) -> dict[str, object]:
    """Return a dict describing one week's plan."""
    # Phase: weeks 1-2 foundations, weeks 3 to N-3 deep work, weeks N-2 to N-1 simulation, last week light review.
    if week_num == 1:
        phase = "Foundation — orientation"
        focus = "Read PMI Exam Content Outline (full). Skim PMP Handbook. Watch one agile-overview video."
    elif week_num == 2:
        phase = "Foundation — start the People domain"
        focus = "People domain: conflict, stakeholder engagement, leadership basics."
    elif week_num <= total_weeks - 3:
        phase = "Deep work"
        # Rotate emphasis: even weeks process, odd weeks people, plus occasional business.
        if (week_num % 4) == 3:
            focus = "Business Environment + business case mechanics + Process domain — agile half"
        elif (week_num % 2) == 0:
            focus = "Process domain — predictive (Earned Value, schedule, scope, risk)"
        else:
            focus = "People domain — deep (team formation, conflict modes, engagement)"
    elif week_num == total_weeks - 2:
        phase = "Simulation"
        focus = "One full 180-question timed practice exam. Identify weak topics."
    elif week_num == total_weeks - 1:
        phase = "Simulation"
        focus = "Second full 180-question timed practice exam. Drill flagged questions."
    else:  # last week
        phase = "Light review"
        focus = "40-question daily quiz. No new content. Sleep, hydrate, set up exam environment."

    # Domain allocation in hours
    allocation = {d: round(weights[d] * hours, 1) for d in weights}

    return {
        "week": week_num,
        "phase": phase,
        "focus": focus,
        "hours_total": hours,
        "hours_by_domain": allocation,
    }


def format_markdown(plan: list[dict[str, object]]) -> str:
    out = ["# Custom PMP Study Schedule", ""]
    out.append(f"Total weeks: {len(plan)}")
    total_hours = sum(int(w["hours_total"]) for w in plan)  # type: ignore[arg-type]
    out.append(f"Total study hours: ~{total_hours}")
    out.append("")
    out.append("## Schedule")
    out.append("")
    out.append("| Week | Phase | Focus | Hours | People | Process | Business |")
    out.append("|---|---|---|---|---|---|---|")
    for w in plan:
        hbd = w["hours_by_domain"]
        out.append(
            f"| {w['week']} | {w['phase']} | {w['focus']} | "
            f"{w['hours_total']} | "
            f"{hbd['people']} | {hbd['process']} | {hbd['business']} |"  # type: ignore[index]
        )
    out.append("")
    out.append("## Notes")
    out.append("")
    out.append("- Hours are guidelines, not contracts. Adjust based on retention.")
    out.append("- Domain hours are the relative split within each week's total — your weakest domain gets more weight per week.")
    out.append("- If a week is consistently under-running, you're either ahead or under-engaging; ask the tutor for diagnostic questions.")
    out.append("- The last week is intentionally lighter than the previous two. Don't cram.")
    out.append("")
    out.append("## Disclaimer")
    out.append("- This plan is a typical pattern for dedicated learners. Your actual study time may vary substantially based on existing PM experience and available focus time.")
    out.append("- The PMP exam can be sat at any time; this plan assumes the exam date is at the end of the final week.")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--weeks", type=int, default=8, help="Total weeks (default 8)")
    parser.add_argument("--hours-per-week", type=float, default=12.0, help="Hours per week (default 12)")
    parser.add_argument(
        "--strengths",
        default="",
        help="Comma-separated strong domains (people,process,business)",
    )
    parser.add_argument(
        "--weaknesses",
        default="",
        help="Comma-separated weak domains (people,process,business)",
    )
    args = parser.parse_args(argv)

    if args.weeks < 4 or args.weeks > 24:
        print("--weeks must be between 4 and 24.", file=sys.stderr)
        return 1
    if args.hours_per_week < 4 or args.hours_per_week > 40:
        print("--hours-per-week must be between 4 and 40.", file=sys.stderr)
        return 1

    try:
        strengths = parse_csv(args.strengths)
        weaknesses = parse_csv(args.weaknesses)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        return 1

    overlap = strengths & weaknesses
    if overlap:
        print(
            f"Domain(s) {', '.join(overlap)} listed as both strength and weakness — drop from one.",
            file=sys.stderr,
        )
        return 1

    weights = adjusted_weights(strengths, weaknesses)
    plan = [
        build_week_plan(i + 1, args.weeks, args.hours_per_week, weights)
        for i in range(args.weeks)
    ]
    print(format_markdown(plan))
    return 0


if __name__ == "__main__":
    sys.exit(main())
