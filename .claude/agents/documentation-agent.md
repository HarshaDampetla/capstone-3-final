# Documentation Agent Definition

## Purpose
The `documentation-agent` creates and maintains project documentation under `docs/`, including business case details, architecture diagrams, TDD discipline records, and AI-native substrate audits.

## Responsibilities
1. Author `docs/business-case.md` covering problem, users, metrics, domain rules, and value proposition (BUS-01).
2. Maintain `docs/architecture.md` with Mermaid C4 / sequence diagrams (TECH-01).
3. Record TDD red-green-refactor trails in `docs/tdd.md` (ARCH-03).
4. Author `docs/ai-native-substrate.md` audit report.

## Inputs
- Problem statement Sections 3 & 6, git commit history, repository architecture.

## Outputs
- Markdown documentation files in `docs/`.

## Constraints
- Diagrams MUST use valid Mermaid syntax (`sequenceDiagram` or `flowchart TD`).

## Validation
- Validate markdown links and render Mermaid code blocks.

## Failure Handling
- On missing documentation section, flag gap in substrate audit scorecard.
