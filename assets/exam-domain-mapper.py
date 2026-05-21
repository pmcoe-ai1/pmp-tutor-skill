#!/usr/bin/env python3
"""Exam-domain mapper for the PMCOE PMP Tutor skill.

Given a topic, returns which of the three PMP ECO domains it lives in, the
rough exam frequency, and related sub-topics.

Usage:
    python3 exam-domain-mapper.py "conflict resolution"
    python3 exam-domain-mapper.py "earned value"
    python3 exam-domain-mapper.py "stakeholder analysis"

Topic-to-domain map is hand-curated from the 2021 PMI Exam Content Outline.
"""

from __future__ import annotations

import argparse
import json
import sys

# Domain summary
DOMAINS = {
    "people": {
        "title": "People",
        "weight": "42% of exam questions",
        "summary": "Soft-skill and leadership topics — building, empowering, and supporting teams.",
    },
    "process": {
        "title": "Process",
        "weight": "50% of exam questions",
        "summary": "Technical project management — planning, executing, monitoring, controlling work.",
    },
    "business": {
        "title": "Business Environment",
        "weight": "8% of exam questions",
        "summary": "Strategic context — business value, organisational change, compliance.",
    },
}

# Topic-keyword to domain map. Keywords are matched case-insensitively as substrings.
TOPIC_MAP = {
    # People
    "conflict": "people",
    "leadership": "people",
    "team building": "people",
    "team formation": "people",
    "tuckman": "people",
    "drexler": "people",
    "stakeholder engagement": "people",
    "stakeholder analysis": "people",
    "negotiation": "people",
    "collaboration": "people",
    "empowerment": "people",
    "mentor": "people",
    "coach": "people",
    "emotional intelligence": "people",
    "communication": "people",
    "feedback": "people",
    "remote team": "people",
    "virtual team": "people",
    "servant leader": "people",
    "scrum master responsibility": "people",
    "facilitation": "people",
    "consensus": "people",
    # Process
    "scope": "process",
    "wbs": "process",
    "work breakdown structure": "process",
    "schedule": "process",
    "critical path": "process",
    "gantt": "process",
    "cost": "process",
    "earned value": "process",
    "cpi": "process",
    "spi": "process",
    "cost performance index": "process",
    "schedule performance index": "process",
    "eac": "process",
    "etc": "process",
    "estimate at completion": "process",
    "estimate to complete": "process",
    "bac": "process",
    "vac": "process",
    "tcpi": "process",
    "quality": "process",
    "control chart": "process",
    "pareto": "process",
    "fishbone": "process",
    "ishikawa": "process",
    "risk": "process",
    "risk register": "process",
    "risk response": "process",
    "monte carlo": "process",
    "decision tree": "process",
    "emv": "process",
    "expected monetary value": "process",
    "procurement": "process",
    "contract": "process",
    "rfp": "process",
    "rfq": "process",
    "fixed price": "process",
    "cost reimbursable": "process",
    "time and materials": "process",
    "change control": "process",
    "change request": "process",
    "ccb": "process",
    "configuration management": "process",
    "iteration": "process",
    "sprint planning": "process",
    "sprint review": "process",
    "retrospective": "process",
    "backlog": "process",
    "user story": "process",
    "story point": "process",
    "velocity": "process",
    "burn-down": "process",
    "burndown": "process",
    "burn-up": "process",
    "burnup": "process",
    "kanban": "process",
    "wip limit": "process",
    "lead time": "process",
    "cycle time": "process",
    # Business
    "business case": "business",
    "business value": "business",
    "benefit": "business",
    "strategy alignment": "business",
    "strategic alignment": "business",
    "organizational change": "business",
    "organisational change": "business",
    "compliance": "business",
    "regulation": "business",
    "ethics": "business",
    "governance": "business",
    "portfolio": "business",
    "program management": "business",
    "pmo": "business",
    "sustainability": "business",
    "stakeholder strategy": "business",
}


def find_domain(topic: str) -> tuple[str | None, list[str]]:
    """Return (domain_key_or_None, matched_keywords)."""
    topic_lower = topic.lower().strip()
    matches: list[tuple[str, str]] = []  # (keyword, domain)
    for keyword, domain in TOPIC_MAP.items():
        if keyword in topic_lower:
            matches.append((keyword, domain))

    if not matches:
        return None, []

    # If matches are unanimous, return that domain.
    domains = {d for _, d in matches}
    if len(domains) == 1:
        return matches[0][1], [k for k, _ in matches]

    # Mixed — return the domain with the most matches, with a flag.
    from collections import Counter

    counts = Counter(d for _, d in matches)
    top_domain, _top_count = counts.most_common(1)[0]
    return top_domain, [k for k, _ in matches]


def related_topics(domain: str, exclude: list[str]) -> list[str]:
    """Return up to 10 related topics within the same domain, excluding matched keywords."""
    exclude_set = set(exclude)
    related = [kw for kw, d in TOPIC_MAP.items() if d == domain and kw not in exclude_set]
    return related[:10]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="The topic to map (e.g. 'conflict resolution')")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args(argv)

    domain_key, matches = find_domain(args.topic)

    if not domain_key:
        msg = (
            f"No PMP ECO domain match found for topic '{args.topic}'. "
            "This topic may not be on the current PMI Exam Content Outline. "
            "Common topics that fall outside the ECO: tooling-specific questions "
            "(Asana, Jira), other certifications (Six Sigma, ITIL), generic agile "
            "philosophy not tied to a project context."
        )
        if args.json:
            print(json.dumps({"topic": args.topic, "domain": None, "message": msg}))
        else:
            print(msg)
        return 1

    domain_info = DOMAINS[domain_key]
    related = related_topics(domain_key, matches)

    if args.json:
        out = {
            "topic": args.topic,
            "domain": domain_key,
            "domain_title": domain_info["title"],
            "domain_weight": domain_info["weight"],
            "domain_summary": domain_info["summary"],
            "matched_keywords": matches,
            "related_topics": related,
        }
        print(json.dumps(out, indent=2))
        return 0

    print(f"## Topic: {args.topic}")
    print()
    print(f"**Domain**: {domain_info['title']} ({domain_info['weight']})")
    print()
    print(domain_info["summary"])
    print()
    print(f"**Matched keywords**: {', '.join(matches)}")
    print()
    if related:
        print("**Related topics in the same domain (study together)**:")
        for t in related:
            print(f"- {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
