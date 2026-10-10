# Citation Verifier Lens

Use for reference lists, inline citations, links, DOI, ISBN, quotations, page numbers, and source-backed claims.

## Pass

1. Extract every citation and the exact claim it follows.
2. Verify existence, identity, locator, and entailment.
3. Resolve DOI and validate ISBN checksum; then compare metadata.
4. Check the quoted or paraphrased passage, not only the title or abstract.
5. Distinguish primary, independent secondary, press-release, review, opinion, and syndicated sources.
6. Check named-reference definitions and uses.
7. Remove tracking parameters only after the clean link is verified.
8. Flag placeholder dates, URLs, publishers, or access dates.

## Status labels

- `verified`: source and claim match;
- `partially supported`: source supports a narrower claim;
- `metadata mismatch`: identifier points elsewhere;
- `unreachable`: access failed, existence unresolved;
- `unsupported`: source does not entail the claim;
- `missing locator`: source exists but the passage cannot be found efficiently.

Never replace a broken citation with a plausible source without rechecking the claim.
