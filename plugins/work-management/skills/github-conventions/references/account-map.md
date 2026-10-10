# Recipient GitHub map

Unconfigured. No originating account repository inventory is included.

Run the complete refresh helper with an explicit receiving owner and an output outside the installed package:

```sh
python3 scripts/refresh_account_map.py --owner RECEIVING_OWNER --output RECIPIENT_ACCOUNT_MAP.md
```

The generated map retains repo count, default branches, repository names, visibility, forks, language, push time, description, branch list, top-level entries, directory/file counts and full file trees. The authenticated account can expose private repository metadata; keep that output under the recipient’s chosen access controls and never treat it as a public fixture.
