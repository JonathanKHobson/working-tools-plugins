# Data Quality and Fraud

## Principle

Quality controls should detect risk without silently excluding legitimate respondents, especially people using assistive technology, translation, shared devices, privacy tools, slow connections, or atypical but real response patterns.

## Prevention

- Recruit through controlled channels when possible.
- Use unique links or tokens proportionately.
- Avoid revealing all eligibility criteria.
- Apply sensible frequency caps, quotas, and duplicate rules.
- Use bot protection with accessible alternatives.
- Keep incentives proportionate and fulfillment controlled.
- Minimize public exposure of high-value survey links.
- Log instrument version, source, timestamps, and relevant technical events with notice and minimization.

## Signals, not verdicts

Potential signals include impossible eligibility combinations, duplicate tokens, extreme speed, repeated exact patterns, straightlining where variation is expected, contradictory answers, nonsensical verbatims, copy/paste repetition, unusual source/IP/device clusters, and failed attention/comprehension checks.

Any single signal can have an innocent cause. Combine evidence, inspect distributions, document thresholds before analysis, and manually review a sample of exclusions.

## Attention checks

Avoid insulting trick questions, obscure knowledge, inaccessible visual traps, or instructions designed only to catch inattentive people. Prefer comprehension checks tied to necessary study content and consistency/quality indicators that do not contaminate primary measures.

## Speeding

Use empirical duration distributions by device/language/path, not one universal seconds-per-question threshold. Fast respondents may know the topic; slow respondents may be distracted or use assistive technology. Treat speed as one flag.

## Duplicates

Define duplicate at the correct unit: person, invitation, household, account, device, IP, transaction, or event. Shared networks/devices and privacy relays make IP-only rules unsafe. Preserve an audit trail and decide which record to retain.

## Open text and AI-generated responses

Look for relevance, specificity, internal consistency, repeated templates, and cross-response duplication. Do not claim authorship detection with certainty. An articulate or translated response is not automatically fraudulent.

## Exclusion plan

Before seeing outcomes, define hard invalidations, soft flags, review process, sensitivity analyses with/without flagged records, and reporting. Keep raw data immutable; create versioned exclusion variables and reasons.

## Operational monitoring

During fielding monitor source, invitation delivery, eligibility, start/completion, breakoff page, duration, device/browser, missingness, quotas, duplicates, and incentive claims. Pause when a source or instrument defect threatens a material share of data.
