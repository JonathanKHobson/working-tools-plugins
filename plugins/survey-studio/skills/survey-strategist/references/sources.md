# Sources and Inspiration

Accessed 2026-07-16 unless noted. This bibliography records sources that materially informed the skill. The skill paraphrases and synthesizes them; it does not copy their prose wholesale. Product documentation can change, so verify current versions before production use.

## Codex skill architecture

| Source | URL | Influence |
|---|---|---|
| OpenAI, “Build skills” | https://learn.chatgpt.com/docs/build-skills | Required `SKILL.md`, optional `scripts/`, `references/`, `assets/`, `agents/openai.yaml`, progressive disclosure, invocation and installation guidance |
| OpenAI Skills repository, `skill-creator` | https://github.com/openai/skills/tree/main/skills/.system/skill-creator | Skill anatomy, naming, frontmatter, validation, reusable resource design, UI metadata |
| Agent Skills specification | https://agentskills.io/specification | Cross-agent skill metadata and directory conventions |
| Cookiy AI, user-research skill | https://github.com/cookiy-ai/user-research-skill | Inspiration for routing a broad user-research request into focused workflows; no Cookiy-specific promotion or workflow was copied |
| Cross AI Tools, “Survey” skill listing | https://crossaitools.com/skills/akillness/oh-my-skills/survey | Reviewed as an adjacent skill; it is oriented toward pre-build research rather than questionnaire construction, reinforcing the need for clear triggering and artifact contracts |

## Questionnaire and survey methodology

| Source | URL | Influence |
|---|---|---|
| American Association for Public Opinion Research, “Best Practices for Survey Research” | https://aapor.org/standards-and-ethics/best-practices/ | Method choice, population/sample, neutral wording, choice-set quality, burden, pretesting, monitoring and transparency |
| Pew Research Center, “Writing Survey Questions” | https://www.pewresearch.org/writing-survey-questions/ | Multistage question development, open vs closed items, order effects and pretesting |
| CDC/NCHS, Collaborating Center for Questionnaire Design and Evaluation Research | https://www.cdc.gov/nchs/ccqder/index.html | Cognitive evaluation and respondent-interpretation testing |
| Dillman, Smyth, and Christian, *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method* | https://www.wiley.com/en-us/Internet%2C+Phone%2C+Mail%2C+and+Mixed+Mode+Surveys%3A+The+Tailored+Design+Method%2C+4th+Edition-p-9781118456149 | General mixed-mode, contact, visual design and response-process background; consult the book for full treatment |
| Tourangeau, Rips, and Rasinski, *The Psychology of Survey Response* | https://www.cambridge.org/core/books/psychology-of-survey-response/7BAE4A1B4C738A4AE466F21A7F471D6B | Comprehension, retrieval, judgment and response mapping framework |
| Groves et al., *Survey Methodology* | https://www.wiley.com/en-us/Survey+Methodology%2C+2nd+Edition-p-9780470465462 | Total survey error framework and sampling/nonresponse background |

## User-provided source material

| Source | Location | Influence |
|---|---|---|
| `QuestionTypes.txt` supplied with the original request | Excluded from public distribution; exact identity/hash in PROVENANCE.json | Historical inventory informed common taxonomy labels. Its table wording is not redistributed. Original safeguards and synthesized selection guidance remain. |

## Qualtrics

| Source | URL | Influence |
|---|---|---|
| Qualtrics, “Import & Export Surveys” | https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/ | Simple/Advanced TXT tags, encoding/import guidance, QSF cautions and format distinctions |
| Qualtrics, “Question Types” | https://www.qualtrics.com/support/survey-platform/survey-module/editing-questions/question-types-guide/question-types-overview/ | Platform question-type inventory and terminology |
| Qualtrics, “Exporting Response Data” | https://www.qualtrics.com/support/survey-platform/data-and-analysis-module/data/download-data/export-data-overview/ | Response export formats and labels-versus-values considerations |

## Form and accessibility design

| Source | URL | Influence |
|---|---|---|
| W3C Web Accessibility Initiative, “Forms Tutorial” | https://www.w3.org/WAI/tutorials/forms/ | Labels, grouping, instructions, validation, notifications and accessible controls |
| GOV.UK Service Manual, “Structuring forms” | https://www.gov.uk/service-manual/design/form-structure | Asking only necessary questions, coherent sequencing, one-thing-at-a-time patterns and mobile/common-path focus |
| Web Content Accessibility Guidelines (WCAG) 2.2 | https://www.w3.org/TR/WCAG22/ | Perceivable, operable, understandable and robust interaction requirements |

## Privacy, ethics and law

These sources support issue-spotting only. The skill does not provide legal advice or certify compliance.

| Source | URL | Influence |
|---|---|---|
| EU General Data Protection Regulation | https://eur-lex.europa.eu/eli/reg/2016/679/oj | Purpose limitation, data minimization, transparency, rights and special-category concepts |
| U.S. HHS, 45 CFR 46 | https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html | Human-subjects protections and informed-consent/IRB issue spotting |
| U.S. FTC, COPPA Rule | https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa | Children’s online privacy and parental-consent issue spotting |
| California Attorney General, CCPA | https://oag.ca.gov/privacy/ccpa | California notice and privacy-rights issue spotting |

## File and interchange standards

| Source | URL | Influence |
|---|---|---|
| RFC 4180, CSV | https://www.rfc-editor.org/info/rfc4180/ | Common CSV quoting/record conventions and interoperability cautions |
| RFC 8259, JSON | https://www.rfc-editor.org/info/rfc8259/ | JSON syntax/interchange rules |
| YAML 1.2.2 specification | https://yaml.org/spec/1.2.2/ | Conservative YAML subset and typing cautions |
| W3C XML 1.0, Fifth Edition | https://www.w3.org/TR/xml/ | Generic XML syntax and validation background |
| XLSForm documentation | https://xlsform.org/en/ | Workbook structure and platform-mapping concepts |
| SurveyJS Form Library documentation | https://surveyjs.io/form-library/documentation/design-survey/create-a-simple-survey | SurveyJS model and runtime mapping orientation |
| DDI Alliance | https://ddialliance.org/ | Formal data/documentation interchange context for survey metadata |
| REDCap data dictionary documentation | https://kb.wisc.edu/smph/informatics/page.php?id=111729 | Orientation to REDCap’s CSV field dictionary; verify against the target REDCap version |
| LimeSurvey manual | https://www.limesurvey.org/manual/Display/Exporting_a_survey_structure | Orientation to LSS survey-structure export; verify against the target version |

## Validated and standardized measures

The skill names measure families but deliberately does not reproduce full copyrighted/licensed instruments. Retrieve wording, scoring, permissions and benchmark evidence from authoritative sources for the exact measure/version.

- Brooke, “SUS: A Quick and Dirty Usability Scale.”
- Lewis et al. publications on UMUX-Lite and post-study usability measures.
- Sauro/Lewis publications on the Single Ease Question and UX benchmarking.
- Hart and Staveland on NASA-TLX.
- Official/licensed sources for SUPR-Q and domain-specific clinical, health or wellbeing measures.

## Maintenance rule

Before changing a platform export or legal/compliance reference, record the documentation version/date, update tests and examples, and rerun `scripts/qa_all.sh`.
