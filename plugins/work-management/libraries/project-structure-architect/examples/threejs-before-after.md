# Example: Three.js Game Before/After

## Before: monolithic

```text
src/
  main.js   # 5,000+ lines
```

Problems:

- render setup, game loop, player logic, enemy AI, collisions, UI, audio, and constants all live together;
- changing a small rule requires scanning the whole file;
- future mechanics have no obvious home;
- agent context cost grows every time.

## After: expansion-aware

```text
src/
  main.js
  core/
    Game.js
    Renderer.js
    Loop.js
  scenes/
    MainScene.js
  entities/
    Player.js
    Enemy.js
  systems/
    InputSystem.js
    CollisionSystem.js
    SpawnSystem.js
  ui/
    HUD.js
  audio/
    AudioManager.js
  config/
    constants.js
```

Benefits:

- new enemies go in `entities/`,
- collision changes go in `systems/CollisionSystem.js`,
- HUD changes go in `ui/HUD.js`,
- balance changes go in `config/`,
- `main.js` stays small.
