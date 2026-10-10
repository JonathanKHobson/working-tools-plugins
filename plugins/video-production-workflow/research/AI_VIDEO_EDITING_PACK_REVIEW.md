# AI Video Editing Pack review

Source: [Payton Bilodeau's AI Video Editing Pack](https://github.com/paytonbilodeau/ai-video-editing-pack),
revision `23902d2676bf2597389d4b2ad1a9de1942ebd0e4`, reviewed 2026-10-07.
Original upstream author: Payton Bilodeau. Reviewed sections: setup/intake,
editor connections and Resolve playbook, editorial judgment/workflow, cut-list
export, review/delivery, and the Resolve/system setup guide.

## License and security decision

The root and pack `LICENSE AND USE.md` use custom Free Use Terms, not MIT. They
permit private/commercial working adaptations and modified working files, retain
attribution for substantially unchanged copies and restrict repackaging the
substantially unchanged library as a competing template product. Third-party
materials retain their own terms. The vendored Animate subtree has separate MIT
terms; this plugin already has an independent motion-methods owner.

**Decision:** independently author bounded operational guidance with attribution
and primary-source verification. Do not copy/vend its skill text, templates,
Python tools, scripts, assets, email funnel, updater or provider configuration
into this MIT plugin. No upstream executable was run and no MCP was configured.
This review is not a security certification of the whole upstream repository.

Inspected setup/cut-list tools perform local file work, media probing and
subprocess calls; setup guides also contain optional remote services, packages
and connector configuration. Those are separate dependency/execution decisions.
The imported scope is methods only: no credentials, inherited provider settings,
network services, telemetry, background agent or browser-profile access.

## Adopt / keep / defer

| Source idea | Existing owner and decision |
| --- | --- |
| Reuse an editing profile; classify control route and prove a real edit | Adopt in **edit-davinci-resolve**; private host facts/proof stay in the owning project |
| Edition-specific Resolve control and UI readback | Adopt original narrow editor owner; Free uses import/UI, supported Studio routes remain conditional |
| Output plus editable project; short import/save/reopen test | Extend **exchange-video-timelines** with Resolve round-trip acceptance |
| Meaning-preserving cuts, room tone, reaction/learning pauses | Keep **edit-dialogue-footage** as owner; no duplicated craft skill |
| Audio/color/motion/caption review | Keep existing audio, editorial-treatment, typography, motion and QA owners; feature availability checked in Resolve |
| Repurposing/waterfall and platform refresh | Keep current conform/course/social handoffs; do not import the pack's release calendar or funnel |
| Python cut-list exporter / FCPXML generation | Defer executable adoption: custom license and actual import fidelity need a separate bounded implementation review/test |
| Native MCP setup | Conditional Studio integration only; no native MCP dependency or config added |
| Community Python bridge | Defer for Free 21.1; older-version proof does not establish latest Free support |
| JavaScript animation library | Defer duplicate adoption; existing pinned procedural-video library owns this route |

The new skill has a distinct operational output: a verified editable Resolve
project/timeline and rendered deliverable. It does not replace editorial stages
or create a universal editor router.

## Edition and connector evidence

- [Blackmagic support catalogue](https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion)
  and [primary download catalogue](https://www.blackmagicdesign.com/api/support/us/downloads.json):
  21.1 separates Free and Studio releases and assigns assistant integration to
  Studio. Reverify current release and read installed edition/build documentation.
- [Official 21.1 manual](https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_21.1_Reference_Manual.pdf):
  same-version operation reference; precise actions still require the installed
  manual and live app. The online PDF retrieval did not succeed during this
  review, so its detailed API claims are not treated as independently verified.
- [Pack Resolve playbook](https://github.com/paytonbilodeau/ai-video-editing-pack/blob/23902d2676bf2597389d4b2ad1a9de1942ebd0e4/AI%20Video%20Editing%20Pack/references/EDITOR%20PLAYBOOK%20RESOLVE.md):
  the author's Studio 21.1 inspected-build account distinguishes vendor-native
  MCP, Python and file/UI routes. It is upstream evidence, not this host's test.
- [`samuelgursky/davinci-resolve-mcp`](https://github.com/samuelgursky/davinci-resolve-mcp):
  the exact external community project, MIT. Its current README restricts the
  measured Free bridge to 21.0.x; Free 21.1 Python script enumeration is absent
  in a reported build and Console support remains unconfirmed. This is distinct
  from Blackmagic's bundled `ResolveMCP`. No repository code was imported.

## Validation boundary

The baseline found no specific Resolve owner/edition route. Routing scenarios
cover current Free support, editable round trip, native finishing and a motion
task that bypasses Resolve. Plugin structure/tests, entrypoint validation, link
checks and bounded independent text review validate packaging/guidance. Actual
Resolve installation, import, saved-state reopen and render are separate host
acceptance evidence. Synthetic FFmpeg release renders do not prove app control.
