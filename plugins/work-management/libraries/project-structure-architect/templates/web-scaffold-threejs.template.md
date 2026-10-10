# Three.js / Browser Game Scaffold

```text
project/
  README.md
  package.json
  index.html
  public/
    favicon.svg
  src/
    main.js
    core/
      Game.js
      Renderer.js
      Loop.js
      AssetLoader.js
    scenes/
      MainScene.js
    entities/
      Player.js
    systems/
      InputSystem.js
      CollisionSystem.js
    ui/
      HUD.js
    audio/
      AudioManager.js
    config/
      constants.js
      controls.js
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

## Entry point pattern

```js
import { Game } from './core/Game.js';

const game = new Game({
  canvas: document.querySelector('#game-canvas'),
});

game.start();
```
