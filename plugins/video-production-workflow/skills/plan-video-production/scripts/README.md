# Script boundary

`run.py` is the deterministic helper for **Plan Video Production**. It intentionally delegates shared behavior to the root `video_workflow` package. Read or patch it only when the project needs behavior that cannot be represented in the manifest or shared CLI.
