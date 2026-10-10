# Browse Density and Frontmatter Hygiene

Use this reference for imports, archive builds, generated note sets, taxonomy cleanup, relationship mapping, bulk moves, and any Obsidian work that could create a wall of notes.

## Browse Density Norm

- Large durable collections should be browseable without dumping hundreds of notes into one folder.
- Treat any browsable folder over about 50 notes as a split candidate.
- Aim for about 10-40 notes per leaf folder when the metadata supports meaningful categories.
- Avoid fake over-splitting. If category data is weak, write a report or review queue before moving notes.
- For small working folders, prefer links, tags, Bases, and indexes over adding folder layers.

## Category-First Collection Layout

- Use existing source categories, primary categories, families, or browse buckets as the first foldering signal.
- Preserve exact semantic metadata even when the browse folder is simplified for humans.
- For generated or curated collection notes, preserve or add:
  - `browse_group`
  - `browse_path`
  - `canonical_path`
- Keep stable IDs, slugs, titles, aliases, provenance, and source fields unchanged during browse reorganizations.
- Use path-aware wikilinks in generated indexes after moves.

## Relationship Mapping

- Use `related` as the default cross-note relationship property unless the target vault already has a stronger convention.
- Mirror important relationships as wikilinks in note bodies or generated relationship indexes so Obsidian graph views can see them.
- Prefer conservative relationship types first:
  - same concept
  - activity uses pattern
  - term explains pattern
  - bias or fallacy overlap
  - possible duplicate for review
- Flag near-duplicates for review instead of deleting, merging, or renaming them during the mapping pass.

## Bulk Move Workflow

1. Verify the live vault path, not only project-local output.
2. Exclude protected areas such as `.obsidian`, `_Meta`, archives, attachments, and generated backends unless explicitly targeted.
3. Run a density report before moving files.
4. Dry-run the folder map and inspect the largest resulting folders.
5. Make a recoverable backup of touched notes and indexes.
6. Move files deterministically while preserving filenames.
7. Update `canonical_path`, browse metadata, indexes, and path-aware wikilinks.
8. Validate note counts, YAML parsing, and path-aware wikilinks.
9. Clean AppleDouble `._*` sidecars created by macOS or external-drive operations, excluding protected areas.

## Frontmatter Hygiene

- Obsidian Properties require valid YAML frontmatter between the opening and closing `---`.
- If Obsidian renders properties as red/plain Markdown text, suspect malformed YAML before assuming an Obsidian UI bug.
- Scan touched notes with a real YAML parser after bulk generation or repair.
- Watch for stray top-level list items after otherwise valid keys, especially patterns like:

```yaml
canonical_path: "03 Collections/Biases/Entries/bias--example.md"
- class: cognitive
```

- Normalize that shape into valid keyed YAML, for example:

```yaml
canonical_path: "03 Collections/Biases/Entries/Cognitive/bias--example.md"
categories:
  - cognitive
```

- Quote wikilinks inside YAML values or list items:

```yaml
related:
  - "[[01 Patterns/Entries/Analysis/pattern--rubber-duck-debugging|Rubber Duck Debugging]]"
```

- Keep long Markdown, citations, transcriptions, and notes in the body, not in frontmatter.

## Validation Checklist

- All touched notes parse as YAML.
- All moved notes have accurate `canonical_path`.
- Large collection notes have `browse_group` and `browse_path` where appropriate.
- Root collection folders are not left with a giant flat pile of notes.
- Generated indexes point to the new paths.
- Path-aware wikilinks in touched areas resolve.
- AppleDouble sidecars are not counted as notes.
- Protected areas were not touched unless explicitly in scope.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
