# DeepFlow-Engine

![PyPI](https://img.shields.io/pypi/v/deepflow-engine)
![Downloads](https://img.shields.io/pypi/dm/deepflow-engine)
![License](https://img.shields.io/github/license/deependujha/deepflow-engine)

<div align="center">
    <img alt="pygame" src="https://raw.githubusercontent.com/gist/deependujha/da01263a8a0b995289697ab5fc7580b7/raw/97ce6a292d0e78c6f7a35461851b094a244907f1/deepflow-engine.svg" />
</div>

---

## 🚀 What is DeepFlow?

DeepFlow is a **frame-by-frame simulation engine** designed for games and physics systems that lets you:

* 🎮 Run games interactively (like normal pygame) with optional playback recording
* ⚙️ Simulate them headlessly (no window) for batch processing
* 🎞️ Generate frames automatically for video synthesis
* 🔊 Log events (like collisions) and trigger audio events
* 🎬 Render videos with perfectly synced audio (ready for reels/shorts)
* 📤 Publish outputs directly (Telegram, Discord coming soon)

---

## 🧠 Core Idea

Write your game **once**, and use it in multiple modes:

```
Game Logic → Engine → Frames → Video → Publish
```

This separation of concerns allows you to:
- **Develop interactively** with real-time feedback
- **Generate content** programmatically for automation
- **Test deterministically** in headless mode
- **Scale** to batch video generation

---

## 📦 Installation

```bash
pip install deepflow-engine
```

**Requirements:** Python 3.12+

---

## 📚 Documentation & Examples

For complete working examples, **check out the [`example/`](./example) directory**:

- 🎮 Full game implementation with collision detection
- 🎬 Interactive and headless modes
- 📹 Video rendering with audio
- 🎯 Best practices and patterns

Run examples:
```bash
cd example
python main.py --help
```

---

## ⚡ Quick Start

### 1. Create a Game

Extend `DeepFlowGame` with your game logic:

```python
import deepflow_engine as dfe
import pygame


class MyGame(dfe.DeepFlowGame):
    def start(self):
        """Initialize game state"""
        self.x = 100

    def update(self):
        """Update game logic (called every frame)"""
        self.x += 100 * self.dt  # Always use dt for frame-independent movement!

    def render(self, canvas):
        """Render game state to canvas"""
        canvas.fill((255, 255, 255))
        pygame.draw.circle(canvas, (0, 0, 255), (int(self.x), 200), 20)

    def get_audio_map(self):
        """Map event types to audio files"""
        return {}
```

### 2. Run the Engine

#### Interactive Mode (Preview & Play)

```python
game = MyGame()
engine = dfe.DeepFlowEngine(game, interactive=True)
dfe.run_pipeline(engine)
```

#### Headless Mode (Generate Video)

```python
game = MyGame()
engine = dfe.DeepFlowEngine(
    game,
    interactive=False,
    frames_dir="frames",
    video_length_seconds=10,
)

output = dfe.run_pipeline(engine)
print(f"Video saved: {output}")
```

---

## 🎯 Complete Example

For a complete, production-ready example with collision detection, event handling, and video generation, see the [`example/`](./example) directory:

```bash
# Run interactive mode
python example/main.py --interactive

# Generate video headlessly
python example/main.py --headless --duration 10
```

> The example demonstrates best practices for building games with DeepFlow.

---

## 🎥 Output

DeepFlow automatically:

1. **Simulates** your game frame-by-frame
2. **Saves frames** to disk
3. **Logs events** (collisions, audio triggers, etc.)
4. **Renders video** with synced audio

Output structure:
```
frames/                    # Individual frames
collisions_log.json       # Event log
deepflow_output.mp4       # Final video
```

---

## 🔊 Audio System

### Define Audio Assets

In your game class:

```python
def get_audio_map(self):
    return {
        "collision": "assets/crash.wav",
        "score": "assets/point.wav",
    }
```

### Trigger Events

During gameplay:

```python
def update(self):
    if self.collision_detected():
        self.play_audio("collision")
```

### Behavior

- **Interactive mode**: Plays sound instantly
- **Headless mode**: Logs event for final video rendering

---

## 🎮 Input Handling

Use `get_input()` abstraction:

```python
def get_input(self):
    if self._engine.interactive:
        return pygame.key.get_pressed()
    return None
```

---

## ⏱️ Time-Based Movement (IMPORTANT)

Always use `dt`:

```python
self.x += speed * self.dt
```

❌ Don’t do:

```python
self.x += 5
```

---

## 🧩 Engine Modes

| Mode | Use Case | Interactive |
|------|----------|-------------|
| **Interactive** | Play/preview the game in real-time | Yes |
| **Interactive + Record** | Play while recording frames for video | Yes |
| **Headless** | Batch generate deterministic simulations | No |
| **Pipeline** | Full automated video generation | No |

---

## 📤 Publishing (Optional)

### Telegram

Send generated videos directly to Telegram:

```python
from deepflow_engine.publisher import TelegramPublisher

publisher = TelegramPublisher(bot_token="YOUR_BOT_TOKEN", chat_id="YOUR_CHAT_ID")
publisher.send_video("deepflow_output.mp4")
```

### Discord (Open for Contributions 🚀)

A Discord publisher is in the roadmap.

Interested in implementing it?

- Implement `DiscordPublisher` extending `BasePublisher`
- Follow the existing `TelegramPublisher` pattern
- Open a PR with tests

---

## 🧠 Design Philosophy

DeepFlow follows clean architecture principles:

```
Game     → Pure game logic (independent of engine)
Engine   → Execution engine (runs game at any speed)
Renderer → Video output (handles frame->video conversion)
Publisher→ Distribution (sends to external services)
```

This separation ensures:
- ✅ Games are testable and reusable
- ✅ Easy to add new modes (headless, interactive, streaming)
- ✅ Simple to integrate with other tools

---

## 🔥 Use Cases

- **🎮 Game Automation**: Auto-play games and record gameplay
- **🎬 Content Creation**: Generate Instagram Reels/YouTube Shorts automatically
- **🧪 Simulation & Visualization**: Physics simulations with video output
- **🤖 AI/RL Training**: Gym-style environments with video logging (coming soon)
- **🧠 Generative Content**: Batch create variations of games for viral content

---

## 🛠️ Roadmap

- [ ] Discord publisher
- [ ] CLI tool (`deepflow run game.py`)
- [ ] Gymnasium/Gym integration for RL
- [ ] Multi-event timeline system
- [ ] Streaming output support
- [ ] WebGL renderer for browser playback

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and write tests
4. Commit with clear messages (`git commit -m 'Add amazing feature'`)
5. Push and open a Pull Request

**Guidelines:**
- Keep the API clean and intuitive
- Avoid tight coupling between game and engine
- Prefer composition over inheritance
- Add tests for new features
- Update documentation

---

## 📜 License

Apache 2.0 License - see [LICENSE](./LICENSE) for details

---

## 👀 Final Note

DeepFlow is **not just a game engine**.

It's a **content engine** - designed to transform game logic into automated, scalable content production.

Use it to build interactive experiences, and let it generate the reels.

---

Made with ❤️ by [deependujha](https://github.com/deependujha)
