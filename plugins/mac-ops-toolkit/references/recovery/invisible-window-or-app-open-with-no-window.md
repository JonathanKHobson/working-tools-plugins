## Invisible Window or "App Open With No Window"

1. Confirm whether the app has real windows.
   Compare:
   - `osascript` window counts from the app
   - `System Events` window counts from the process
   - raw process arguments from `ps`
2. Check whether the tracked app process is actually:
   - a headless browser process
   - a helper or renderer
   - an updater or login item
3. Try the least-destructive recovery:
   - activate the app
   - request a new window explicitly
   - relaunch the app normally
4. If stale helper or headless processes are holding the app open, clear those
   first and retry a normal launch.
5. Only if the symptom persists, back up the smallest relevant support files and
   reset crash/session/window-placement state.
