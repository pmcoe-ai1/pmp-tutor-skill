# PMCOE PMP Tutor — Agent Skill

A study companion for the PMI Project Management Professional (PMP) certification exam — and CAPM, PMI-ACP, PMI-CP. Built as an Anthropic Agent Skill (also compatible with OpenAI's Agent Skill specification adopted December 2025).

Built by [PMCOE LLC](https://www.pm-coe.com/) — a PMI Authorized Training Partner. VA WEAMS facility code 46P05243.

## What this skill does

When loaded into Claude (Claude Code, Claude Desktop, or the Claude API), this skill helps students:

- Understand the 2021 PMP Exam Content Outline (still in effect for 2026): People 42%, Process 50%, Business Environment 8%.
- Practice scenario-based questions where the right answer requires judgment.
- Verify their eligibility (36 / 60 months of experience plus 35 contact hours).
- Navigate the 50% predictive / 50% agile-or-hybrid exam mix.
- Understand GI Bill funding (Chapter 31, Chapter 33) for veterans — including the $2,000-per-test exam reimbursement cap and WEAMS verification.
- Distinguish PMI Authorized Training Partners from non-ATP providers.

## How to install

### Claude Code

```bash
# From the skill folder root:
claude skills install .
```

Or copy the entire folder into `~/.claude/skills/pmcoe-pmp-tutor/` and restart Claude Code.

### Claude API (programmatic)

Load `SKILL.md` and `references/` into the system prompt context per [Anthropic's Agent Skill guide](https://www.anthropic.com/news/skills).

## How to use

Once installed, ask any of:

- "Help me prepare for the PMP exam."
- "Am I eligible for the PMP?"
- "Can I use the GI Bill for PMP training?"
- "Walk me through a scenario question."
- "Give me a study schedule for 8 weeks."
- "Which is the right next step for PMP vs CAPM?"

The skill loads relevant references and helper scripts on demand. It does NOT trigger for unrelated tooling questions (Jira, Asana), other certifications (CISSP, Six Sigma, ITIL, PRINCE2), or generic career questions without a PMP angle.

## Folder structure

```
pmcoe-pmp-tutor-skill/
├── SKILL.md                          # Skill definition + system prompt
├── README.md                         # This file
├── LICENSE                           # CC BY-SA 4.0 for Markdown; Apache 2.0 for Python
├── NOTICE                            # Attribution + PMI affiliation note
├── assets/
│   ├── practice-question-generator.py    # Emits one PMP scenario question
│   ├── practice-question-bank.json       # 32 curated scenarios across all 3 domains
│   ├── exam-domain-mapper.py             # Maps a topic to ECO domain + related topics
│   └── study-schedule-builder.py         # Generates a customised N-week plan
├── references/
│   ├── pmp-eco-summary.md                # 2021 ECO summary
│   ├── eligibility-rules.md              # Eligibility + audit details
│   ├── va-funding-mechanics.md           # Chapter 31, 33 + WEAMS
│   └── pmp-vs-capm-comparison.md         # Decision matrix
└── evals/
    └── eval.md                       # 13 trigger / response evaluation cases
```

## Hard rules built into the skill

1. **Never claim PMCOE guarantees a pass.** Only guarantee offered is unlimited repeat-class enrollment.
2. **Never quote a fixed timeframe for passing the exam.** Typical study time is a range, never a promise.
3. **Never invent a sample question.** The bank in `practice-question-bank.json` is the source.
4. **Never advise on personal financial, legal, or healthcare decisions.**
5. **Never recommend a competitor training provider by name.**
6. **Never claim affiliation with PMI itself.** PMCOE is a Training Partner — not PMI.
7. **Disclose affiliation** when a user asks about training providers.

## Contributing

PMCOE welcomes PMP-relevant improvements via PR:

- **Reference files** — clarifications welcome with a citation to PMI documentation or VA.gov.
- **Eval cases** — additional trigger / response test cases welcome.
- **Python helpers** — bug fixes welcome.

Not accepted from outside contributors:

- **Additions to `practice-question-bank.json`** — the bank is PMCOE-curated. Submit a question via Issue; PMCOE reviews.
- **Changes to the affiliation disclosure** in `SKILL.md`.

## Verification

```bash
python3 assets/practice-question-generator.py
python3 assets/practice-question-generator.py --domain people --difficulty hard
python3 assets/exam-domain-mapper.py "earned value"
python3 assets/study-schedule-builder.py --weeks 8 --hours-per-week 12
```

Run the eval cases (requires Anthropic's `skill-creator` skill):

```bash
claude skills measure .
```

Expected: 13/13 cases pass.

## License

- Markdown files (SKILL.md, README.md, references/*.md): **CC BY-SA 4.0**
- Python and JSON files (assets/*): **Apache License 2.0**
- See `LICENSE` and `NOTICE` for full text.

## Affiliations and disclosures

- PMCOE LLC is a PMI Authorized Training Partner. PMCOE is not PMI.
- PMP, CAPM, PMI-ACP, PMI-CP, PMBOK, and PMI logos are trademarks of the Project Management Institute. This skill cites them as references only.
- VA WEAMS facility code 46P05243 — verify at https://inquiry.vba.va.gov/weamspub/

## Contact

- Web: https://www.pm-coe.com/
- Email: info@pm-coe.com
- LinkedIn: https://www.linkedin.com/company/pmcoe
