# Qualtrics QSF

## What QSF is

QSF is Qualtrics’ survey project definition/backup and transfer format. It is not a response-data export.

## Policy

Do not hand-author, patch, or synthesize QSF in this skill. Qualtrics documentation warns against editing QSF contents, and internal structures can be version-sensitive. A superficially valid JSON file can corrupt a project or misrepresent logic.

## Safe workflow

1. Build/import the survey through supported Qualtrics UI or documented import formats.
2. Program and test it in Qualtrics.
3. Export QSF from Qualtrics for backup or transfer.
4. Preserve the original file and hash; do not reformat it.
5. Import into a nonproduction project to verify transfer before relying on it.

## When a user asks for QSF

Provide canonical JSON/YAML, Advanced TXT, programming checklist, and instructions to produce the QSF from Qualtrics. If they supply a QSF for analysis, treat it as version-sensitive untrusted JSON, make a copy, avoid writing it back, and use official Qualtrics documentation/API support for modifications.

## Distinction

A QSF may contain survey definition and settings; collected responses must be exported separately in a response-data format.
