# interviewer.skill

> *"So, thank you for your interest in our company."*

**Reverse-engineer the interviewers you've met. Distill them into an AI Skill that keeps roasting you.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

Feed it whatever materials you have: job descriptions, interview transcripts, and anything you know about the interviewer — their role, background, papers, code, GitHub profile, or just your subjective impression of how they asked questions.
It won't be a perfect replica of a person. But it can get surprisingly close to how they interviewed.

To put it plainly: this isn't generic AI roleplay. This is **interviewer reverse engineering**, built for candidates who are tired of walking into an information asymmetry and losing.

In real life, they've already clocked out. In the cyber realm, we've decided they work here now, year-round.

⚠️ **This project is for interview preparation and review only. Not for impersonating real people, violating privacy, fabricating interview outcomes, or making hiring decisions on behalf of any company.**

[Install](#install) · [Usage](#usage) · [Examples](#examples) · [中文](README.md)

---

## Installation

### Claude Code

```bash
# Install to current project
mkdir -p .claude/skills
git clone https://github.com/Bughouse1024/interviewer-skill.git .claude/skills/create-interviewer

# Or install globally
git clone https://github.com/Bughouse1024/interviewer-skill.git ~/.claude/skills/create-interviewer
```

### Dependencies (optional)

```bash
pip3 install -r requirements.txt
```

---

## Usage

In Claude Code, type:

```text
/create-interviewer
```

This creates a Skill that brings back an interviewer you've met — specifically, the one from that interview you'd rather not think about but definitely need to revisit.

Import whatever you have: interview transcripts, job descriptions, company background, and anything you know about them. The system will piece together a working model — or at least a pretty accurate projection of how they show up in an interview room.

Follow the prompts to enter a codename, basic info, technical background, and a persona sketch. Everything except the codename is optional — a rough verbal description is enough to generate a first draft.

Once done, use `/{slug}` to start the interviewer and put them to work on your laptop, indefinitely, unpaid.

### Management Commands

| Command | Description |
|---------|-------------|
| `/list-interviewers` | List all interviewer Skills |
| `/{slug}` | Launch a full interviewer Skill |
| `/update-interviewer {slug}` | Add new materials and update |
| `/interviewer-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-interviewer {slug}` | Delete |
| `/let-them-rest {slug}` | Gentle alias for delete — send them home |

---

## Features

To make sure the result isn't a standard question-bank reciter, but a cyber interviewer with a distinct background and  personality, this Skill reconstructs three things simultaneously:

their technical background, their assessment logic, and their personality.

### Data Sources

| Source | Format | Notes |
|--------|--------|-------|
| Interview transcripts | txt / md / plain text | Exact questions, follow-up logic, pacing, catchphrases |
| Academic papers | PDF | Research direction, methodology preferences, rigor standards |
| Code materials | .py / .cpp / .java etc. | Coding style, preferred frameworks, problem-solving approach |
| Job-related materials | txt / md / PDF / screenshots | Assessment scope, requirements, written test question types |
| GitHub / LinkedIn screenshots | JPEG / PNG | Public profile, interests, self-expression style |
| Narration / paste | Plain text | Subjective impressions and feelings |

### Generated Skill Structure

Each interviewer Skill is composed of three parts that drive the output together:

| Part | Contents |
|------|----------|
| **Part A — TechMap** | Academic background, tech stack, research direction, projected assessment areas and question patterns |
| **Part B — BehaviorArchive** | Question bank, follow-up chain archive, interview pacing, reactions to different answers |
| **Part C — Persona** | 5-layer structure: hard rules → identity → speaking style → questioning & pressure patterns → interview behavior |

Logic: `receive message → Persona determines how they'd ask → BehaviorArchive reproduces known questions and follow-up chains → TechMap fills in technical context → output in their style`

### Evolution

* **Add materials** → new transcripts, papers, code, screenshots → auto-analyzed and merged into the relevant part
* **In-conversation correction** → say "they wouldn't ask that" → written to the Correction layer, takes effect immediately
* **Version control** → every update is auto-archived, rollback supported

---

## Notes

* **Material quality determines accuracy**: interview transcripts + follow-up logic + job/company description > subjective impressions
* Recommended priority: **technical question bank** > **resume-based questions** > **complete follow-up chains** > **reactions to right/wrong answers** > **opening and closing style**
* The goal isn't a standard question bank — it's an interviewer who will press you, correct you, and not let you get away with a vague answer

---

## Acknowledgments

The architecture of this project is directly inspired by **[colleague.skill](https://github.com/titanwings/colleague-skill)** (by [titanwings](https://github.com/titanwings)), which pioneered the Work Skill + Persona dual-layer architecture for distilling a person — or at least their professional side — into an AI Skill. interviewer.skill takes that foundation and moves the scenario into interview reverse engineering. Full credit to the original author for the idea and for open-sourcing it.

This project follows the [AgentSkills](https://agentskills.io) open standard and is compatible with Claude Code and OpenClaw.

---

