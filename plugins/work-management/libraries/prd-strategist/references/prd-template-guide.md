# PRD Template Guide

Use this reference for full PRDs, executive-ready specs, or any request that needs a more formal document shape.

## Core Principles

- Open with the shortest clear description of the product or feature.
- Establish the problem and evidence before expanding into scope.
- Write for mixed audiences: leadership, design, engineering, QA, and operations.
- Keep every section tied to a decision, an action, or a measurable outcome.
- Recommend a path instead of listing options without judgment.

## Recommended Section Order

1. Title block
2. Executive summary
3. Audience definition
4. Positioning statement
5. Goals, non-goals, and success metrics
6. Scope and constraints
7. MVP feature list
8. North-star or post-MVP opportunities
9. User stories, FRs, NFRs, and ACs
10. Data, privacy, security, and observability notes
11. Phase roadmap and slices
12. Rollout and risk management
13. Stakeholders and RACI
14. Assumptions, open questions, and decision log

Add or remove sections based on the job. Do not force a heavyweight PRD when a lighter artifact would work.

## Title Block

For a formal document, include:

- product or feature name
- one-line tagline
- version
- date
- author or owner
- status such as Draft, Review, Approved, In Development, or Released

## Executive Summary

Aim for 2-4 short paragraphs:

- what this is and who it serves
- what the first release accomplishes
- why this matters now
- what future expansion could unlock

## Audience Definition

Define the main audiences in terms of:

- who they are
- what they need to see
- what builds trust
- what action they should take

Include accessibility or localization considerations when they materially affect scope.

## Positioning Statement

Use a short differentiator statement:

`This product is for [audience] who need [outcome]. Unlike [current alternative], it delivers [difference].`

## Scope Framing

Always make these explicit:

- in scope
- out of scope
- constraints
- dependencies
- non-goals

This section prevents quiet scope creep later.

## Requirements Guidance

### Functional requirements

Each FR should have:

- ID
- title
- description
- priority
- linked story
- linked AC

### Non-functional requirements

Use NFRs for:

- performance
- reliability
- privacy
- security
- observability
- maintainability
- scalability
- accessibility when it must be enforced as a quality bar

### Acceptance criteria

Prefer Gherkin. Keep each criterion observable.

## Delivery and Roadmap Guidance

Use phases to show maturity over time. Use slices to show user outcomes.

Recommended default:

- `Phase 1: MVP`
- `Phase 2: Expand`
- `Phase 3: Scale`

Each phase should answer:

- what ships
- who benefits
- what KPI or gate must be met before the next phase

## Rollout and Risk Guidance

For higher-risk work, include:

- rollout rings
- flag strategy
- rollback plan
- kill switch owner
- top risks and mitigations

## Editorial Tone

- outcome-first
- user-centered
- concrete
- decisive
- honest about tradeoffs

Avoid:

- generic business filler
- long lists without prioritization
- undefined PM jargon
- requirements with no owner or no validation path

## Formal Deliverables

If the user asks for a `.docx`, use this guide to shape the content, then hand off to `$doc` for document creation, formatting, and visual QA.
