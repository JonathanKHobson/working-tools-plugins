# 04 — Game Project Structure Guide

## Goal

Prevent games from turning into one giant `main.js`, `Game.cs`, `GameManager`, or scene file.

Games naturally accumulate systems:

- rendering,
- input,
- player state,
- enemies,
- physics/collision,
- levels,
- spawning,
- audio,
- UI/HUD,
- save/persistence,
- settings,
- assets,
- animation,
- effects,
- debug tools.

If these start in one file, future changes become expensive.

## Browser / Three.js game default

`src/main.js` should initialize and start the game. It should not contain the entire game.

```text
project/
  README.md
  index.html
  package.json
  src/
    main.js
    core/
      Game.js
      Renderer.js
      Loop.js
      CameraController.js
      AssetLoader.js
    scenes/
      MainScene.js
      MenuScene.js
    entities/
      Player.js
      Enemy.js
      Projectile.js
    systems/
      InputSystem.js
      PhysicsSystem.js
      CollisionSystem.js
      SpawnSystem.js
      ScoreSystem.js
    ui/
      HUD.js
      Menu.js
    audio/
      AudioManager.js
    config/
      constants.js
      controls.js
      balance.js
    utils/
      math.js
  assets/
    models/
    textures/
    audio/
    fonts/
  docs/
    project-map.md
    roadmap.md
  tests/
```

## Three.js file responsibilities

| File/folder | Responsibility |
|---|---|
| `main.js` | Create `Game`, call `start()`, handle top-level errors. |
| `core/Game.js` | Own lifecycle, high-level orchestration. |
| `core/Renderer.js` | Renderer/canvas setup and resize. |
| `core/Loop.js` | Fixed/variable update loop. |
| `scenes/` | Scene construction and scene-specific object composition. |
| `entities/` | Player, enemy, pickups, interactive objects. |
| `systems/` | Cross-entity behavior: input, physics, collision, spawning. |
| `ui/` | HUD, menus, overlays. |
| `config/` | Controls, constants, balance values. |
| `assets/` | Static game assets. |

## Unity guidance

Unity does not have one universal structure, but Unity recommends documenting naming conventions and folder structure so teams can find and organize files. [S17](source-index.md)

Common structure:

```text
Assets/
  _Project/
    Scripts/
      Core/
      Gameplay/
      UI/
      Systems/
    Scenes/
    Prefabs/
    Art/
      Models/
      Textures/
      Materials/
    Audio/
      Music/
      SFX/
    UI/
    ScriptableObjects/
    Editor/
    Resources/        # only when truly needed
    StreamingAssets/  # only when truly needed
```

Avoid:

- all scripts in one `GameManager`,
- all assets in root `Assets/`,
- duplicate "final" prefabs/scenes,
- mixing third-party asset packs directly into project source without a boundary.

## Godot guidance

Godot recommends `snake_case` for folder and file names, except C# scripts, and `PascalCase` for node names. [S18](source-index.md)

Common structure:

```text
project/
  scenes/
    player/
      player.tscn
      player.gd
    levels/
      level_01.tscn
  scripts/
    systems/
    ui/
  assets/
    sprites/
    audio/
    fonts/
  resources/
  autoload/
  addons/
  docs/
```

Feature/scene colocation is often useful:

```text
characters/
  player/
    player.tscn
    player.gd
    player_stats.tres
    animations/
```

## Unreal guidance

Unreal recommends naming conventions early for large projects, using asset prefixes/descriptors to reduce ambiguity. [S19](source-index.md)

Unreal projects also have important engine directories such as `Config`, `Content`, `Plugins`, `Source`, and generated/cache/build folders. [S20](source-index.md)

Common content organization:

```text
Content/
  ProjectName/
    Characters/
    Environments/
    Materials/
    UI/
    Blueprints/
    Maps/
    Audio/
    VFX/
Source/
  ProjectName/
Config/
Plugins/
```

Avoid committing or treating generated/cache directories as source unless the engine/tooling requires it.

## Game docs

Minimum:

```text
docs/
  project-map.md
  roadmap.md
```

Useful additions:

```text
docs/
  design/
    game-loop.md
    mechanics.md
    balancing.md
  architecture/
    adr/
  content-pipeline.md
  controls.md
```

## Game-specific decision records

Use ADRs or design decision records for:

- engine/framework choice,
- ECS vs object-oriented entity approach,
- physics/collision strategy,
- asset pipeline,
- save system,
- networking model,
- level format,
- procedural generation,
- input abstraction,
- UI architecture.

## Game done checklist

- [ ] Entry file is thin.
- [ ] Rendering, input, entities, systems, UI, audio, config, and assets are separated.
- [ ] Game constants/balance values are not scattered through behavior code.
- [ ] Assets have predictable folders and naming.
- [ ] Project map explains where to add new enemies, levels, UI, controls, and assets.
- [ ] Engine-specific generated/cache folders are ignored or separated.
- [ ] Future mechanics have obvious homes without refactoring the whole project.
