# Image Gen Templates

Read this when a user wants help choosing a repeatable image generation or edit approach, or wants a prompt they can inspect before generating. The shared **Image Gen Templates** MCP selects methods and prepares prompts; it is not an image generator. Check whether its tools are available on the current host. If absent, make the same selection from the brief and continue with the available official `imagegen` skill; do not claim a library search or handoff occurred.

## Select and hand off

- `search_image_workflows` is assistant-only retrieval. Filter to the task's domain (`graphic`, `ux`, `creative`, or `video`) and intent, then inspect promising records with `read_image_workflow`. Search results are candidates, not completed prompts or proof of an output.
- `browse_image_workflows` is the human chooser when the user wants to explore options. Opening a chooser is not generation and does not authorize uploading references or running a model.
- `read_image_workflow` supplies the full selected method, needed inputs, constraints and examples. Apply only the fields relevant to this request.
- `prepare_image_workflow_handoff` returns a visible, editable prompt and a concise handoff with workflow ID, intended asset or edit target, reference roles, constraints and preferences. Show the prompt before execution when the user is choosing or revising it. Treat its output as a proposal; reconcile it against the user's brief and the official tool instructions.

The library owns selection and prompt preparation. The official `imagegen` skill and built-in `image_gen` tool own generation, edits, transparency, input handling, persistence and output review. An aspect ratio or level of detail from a workflow is a **prompt preference**, not a native `image_gen` parameter or a promise of exact dimensions. Do not invent a size, quality, mask, or model argument for the built-in tool. The API/CLI fallback requires the user's explicit request or confirmation under `imagegen`; an unavailable built-in tool or library does not authorize it.

## References and execution

Label each input as an edit target, reference image, or supporting insert. A description, search result, URL, library record or chooser state is not an attached image. Before generating, verify that every image the prompt relies on is actually available: inspect local files with `view_image` when needed, or use the smallest recent conversation image window that includes the intended images. If an image cannot be provided to the tool, remove the claim that it is attached and either proceed from its description alone when that serves the request or obtain the missing image.

Do not design a widget upload flow for this library. References remain in the host's supported file or conversation-image path. Keep the user's editable prompt, exact text, protected subjects, and exclusions visible through handoff. For project assets, save selected output to a stable project path and review the rendered use according to the owning design or story workflow.

For motion, select a workflow only for **separable still assets or styleframes**. Graphic Design may define visual continuity; Video Production owns timed footage, clip generation, audio, editing and render. UX motion concepts become behavior and visuals rebuilt in code by the UX owner. A still handoff does not imply alpha channels, editable native layers, exact pixel dimensions, or a ready animation; verify any such property from the actual produced file.

Bypass the library for a straightforward edit to an existing SVG, editable vector, code-native icon or established logo system. Edit the source directly under its owning workflow. A user may also bring a sufficiently complete prompt; preserve its specificity and use `imagegen` directly when choosing a library method would add no value.
