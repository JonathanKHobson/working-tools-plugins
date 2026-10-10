# Source Index: Project Expansion & Organization Skill Packet

_Last researched/compiled: 2026-05-19._

This packet synthesizes current guidance from official documentation and established engineering/documentation practices. The source IDs below are used in the reference docs.

## Codex / agent configuration

- **S01 — OpenAI Codex AGENTS.md guide**  
  https://developers.openai.com/codex/guides/agents-md  
  Key takeaways: Codex reads `AGENTS.md` before work; global and project guidance can be layered; `AGENTS.override.md` can override `AGENTS.md`; project guidance can exist at different directory levels.

- **S02 — OpenAI Codex Agent Skills**  
  https://developers.openai.com/codex/skills  
  Key takeaways: A skill is a directory with required `SKILL.md` plus optional `scripts/`, `references/`, `assets/`, and `agents/`; `SKILL.md` requires `name` and `description`; skill descriptions should be concise and front-load trigger words.

- **S03 — OpenAI Codex best practices**  
  https://developers.openai.com/codex/learn/best-practices  
  Key takeaways: Good prompts include goal, context, constraints, and done criteria; complex tasks benefit from planning first; reusable guidance belongs in `AGENTS.md`; overly large guidance should reference task-specific markdown files.

## Repository management / change management

- **S04 — GitHub Docs: About README files**  
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes  
  Key takeaways: A README explains why a project is useful, what people can do with it, and how to use it.

- **S05 — GitHub Docs: CODEOWNERS**  
  https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners  
  Key takeaways: CODEOWNERS can define owners for files/directories and can be combined with branch protection to require review from owners.

- **S06 — GitHub Docs: Branch protection rules**  
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule  
  Key takeaways: Protected branches can require reviews and passing status checks before merge.

- **S07 — GitHub Docs: Large files / repository limits**  
  https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github  
  https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits  
  Key takeaways: GitHub recommends keeping repositories small, ideally under 1 GB and strongly under 5 GB; individual Git objects are recommended under 1 MB and blocked at 100 MB; use Git LFS for large files.

- **S08 — Google Engineering Practices: Small CLs and code review**  
  https://google.github.io/eng-practices/review/developer/small-cls.html  
  https://google.github.io/eng-practices/review/reviewer/standard.html  
  Key takeaways: Small, self-contained changes are easier to design well, review, test, and maintain; code review should improve overall code health.

- **S09 — The Twelve-Factor App**  
  https://12factor.net/  
  Key takeaways: Use declarative setup automation, explicit dependencies, environment-backed configuration, and clean separation of build/release/run concerns.

## Web/app structure

- **S10 — MDN: Organizing CSS**  
  https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Organizing  
  Key takeaways: Logical sections and consistent organization make styles easier to scan and maintain; organization should be intentional.

- **S11 — Next.js Docs: Project structure**  
  https://nextjs.org/docs/app/getting-started/project-structure  
  Key takeaways: Colocation can be safe within framework rules; private folders can separate UI logic from routing logic, create consistency, and avoid naming conflicts.

- **S12 — React Docs: File structure**  
  https://legacy.reactjs.org/docs/faq-structure.html  
  Key takeaways: Common project structures include grouping by feature/route or grouping by file type; React does not mandate one structure.

- **S13 — Vite Docs: Static asset handling**  
  https://vite.dev/guide/assets  
  Key takeaways: `public/` is for assets that are not referenced in source, must keep exact file names, or should not be imported first; source-referenced assets can live in `src`.

- **S14 — Turborepo: Structuring a repository**  
  https://turborepo.dev/docs/crafting-your-repository/structuring-a-repository  
  Key takeaways: Multi-package workspaces typically separate `apps/` and `packages/`.

- **S15 — pnpm workspaces**  
  https://pnpm.io/workspaces  
  Key takeaways: Workspaces unite multiple projects/packages in one repository via `pnpm-workspace.yaml`.

- **S16 — Nx folder structure**  
  https://nx.dev/docs/concepts/decisions/folder-structure  
  Key takeaways: Monorepo structure should support moving/removing projects as organizations evolve; apps and libraries can be organized intentionally.

## Game project structure

- **S17 — Unity: Best practices for organizing your project**  
  https://unity.com/how-to/organizing-your-project  
  Key takeaways: There is no single correct Unity structure; document naming conventions and folder structure; templates/style guides help teams find files.

- **S18 — Godot Docs: Project organization**  
  https://docs.godotengine.org/en/stable/tutorials/best_practices/project_organization.html  
  Key takeaways: Godot recommends snake_case for folder/file names except C# scripts; PascalCase for node names; directory naming consistency avoids export/case-sensitivity issues.

- **S19 — Unreal Engine Docs: Recommended asset naming conventions**  
  https://dev.epicgames.com/documentation/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects  
  Key takeaways: Large UE projects should establish asset naming conventions early to avoid ambiguity and help teams locate assets.

- **S20 — Unreal Engine Docs: Directory structure**  
  https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-directory-structure  
  Key takeaways: Unreal game projects commonly contain `Config`, `Content`, `Plugins`, `Source`, generated/cache/build directories, etc.; generated and cache directories should be treated differently from source/content.

## Database/data organization

- **S21 — PostgreSQL Docs: Schemas**  
  https://www.postgresql.org/docs/current/ddl-schemas.html  
  Key takeaways: Schemas organize database objects into logical groups, enable multiple users to share a database without interference, and prevent third-party object name collisions.

- **S22 — PostgreSQL Docs: Constraints / foreign keys**  
  https://www.postgresql.org/docs/current/ddl-constraints.html  
  https://www.postgresql.org/docs/current/tutorial-fk.html  
  Key takeaways: Constraints and foreign keys protect relational integrity; many-to-many relationships typically need join tables.

- **S23 — Microsoft: Database normalization description**  
  https://learn.microsoft.com/en-us/troubleshoot/microsoft-365-apps/access/database-normalization-description  
  Key takeaways: Normalization organizes data into tables and relationships to protect data, improve flexibility, and reduce redundancy/inconsistent dependency.

- **S24 — Cookiecutter Data Science**  
  https://cookiecutter-data-science.drivendata.org/  
  Key takeaways: Data-science projects benefit from a logical, flexible, standardized structure with explicit `data/`, `docs/`, `models/`, `notebooks/`, `reports/`, and source directories.

## Documentation, project management, information architecture

- **S25 — PMI: Work Breakdown Structure basics**  
  https://www.pmi.org/learning/library/work-breakdown-structure-basic-principles-4883  
  Key takeaways: WBS is a product/deliverable-oriented hierarchy that organizes and defines total project scope; each descending level adds detail.

- **S26 — NASA Systems Engineering Handbook: Technical Data Management**  
  https://www.nasa.gov/reference/6-6-technical-data-management/  
  Key takeaways: Technical Data Management plans for acquiring, accessing, managing, protecting, and using technical data through the system life cycle.

- **S27 — Diátaxis documentation framework**  
  https://diataxis.fr/  
  Key takeaways: Documentation should serve four distinct needs: tutorials, how-to guides, reference, and explanation.

- **S28 — ThoughtWorks: Lightweight Architecture Decision Records**  
  https://www.thoughtworks.com/en-us/radar/techniques/lightweight-architecture-decision-records  
  Key takeaways: ADRs capture important architectural decisions with context and consequences for future team members and oversight.

- **S29 — MADR: Markdown Architectural Decision Records**  
  https://adr.github.io/madr/  
  Key takeaways: MADR is a structured markdown template for recording architecturally significant decisions.

- **S30 — The Turing Way**  
  https://book.the-turing-way.org/  
  https://book.the-turing-way.org/project-design/pd-overview/pd-overview-methods/  
  Key takeaways: Reproducible projects should define questions, methods, tools, infrastructure, and make data/code/findings easier to rerun, reuse, and verify.

## Python/testing

- **S31 — Python Packaging User Guide: src layout vs flat layout**  
  https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/  
  Key takeaways: `src` layout separates import packages from top-level project files and helps avoid import/path confusion.

- **S32 — pytest: Good integration practices**  
  https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html  
  Key takeaways: pytest recommends practices that avoid subtle import problems and supports a `src` layout for new projects.

## UX/design systems

- **S33 — Nielsen Norman Group: Design Systems 101**  
  https://www.nngroup.com/articles/design-systems-101/  
  Key takeaways: Design systems include components, patterns, styles, and guidelines, and should be shaped by project scale, replicability, resources, and time.

- **S34 — Figma: Variables**  
  https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma  
  Key takeaways: Variables store reusable values for design properties and prototyping actions, supporting design systems and complex flows.

- **S35 — Material Design: Design tokens**  
  https://m3.material.io/foundations/design-tokens  
  Key takeaways: Design tokens are small, reusable design decisions that replace static values with self-explanatory names.

- **S36 — Atlassian Design System: Design tokens**  
  https://atlassian.design/tokens/design-tokens  
  Key takeaways: Design tokens are name/value pairs representing repeatable design decisions and act as a source of truth.
