# Choose the surface and execution owner

| Requested surface | Design decisions | Execution owner and verification |
| --- | --- | --- |
| Website or browser app | Existing tokens, information hierarchy, real content, responsive states | Owning repo plus Build Web Apps for relevant framework/testing; Sites only for an explicit Sites project. Check desktop, narrow and short-height layouts when affected. |
| Touch/mobile web | Reachability, readable text, target spacing, soft-keyboard and scroll behavior | Same web owner; exercise the core path with touch-size viewport and keyboard focus, not merely resized screenshots. |
| Native iPhone/iPad | Platform controls, safe areas, dynamic type, touch and accessibility | Build iOS Apps provider; test in its supported simulator/device path. Web CSS guidance does not establish native behavior. |
| Native macOS | Window resizing, menus, keyboard conventions, focus and desktop density | Build macOS Apps/native-macos-app-builder; use native runtime evidence. |
| Android or cross-platform | Platform navigation, adaptive layouts, text scaling, input behavior | Verified project framework plus Test Android Apps when applicable. Do not switch stacks based on a generic style recommendation. |
| Figma or Stitch | Authoritative frame/version, source fidelity and design direction | Current Figma provider or personal Figma UI operator; Stitch Design Studio for Stitch. A exported mockup is not implemented behavior. |
| Workbook | Editable versus computed cells, scenario context, navigation and error recovery | Primary Spreadsheets provider for workbook mechanics, with spreadsheet-usability.md for the human task. |
| PDF/doc/deck | Reading order, page/slide fit, typography and evidence | Current PDF/Documents/Presentations provider; render and inspect changed pages. |
| Poster/brand/infographic | Composition, typography, truthful visual encoding and format constraints | Graphic Design Studio; MyFonts, Color Designer - Palette Maker or Infographic Artist only for the specific unresolved input. |

Discover the current provider at use time. Tool exposure, authentication, generated output, exported file and verified behavior are separate states. Do not create an environment or load every platform skill for a task on one surface.
