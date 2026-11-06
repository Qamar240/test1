# Cartoon shorts: run on your own PC

What is in this repo:
- `shorts/`: the Remotion + three.js project (the finished bridge short is composition `BridgeShort`).
- `shorts/audio-bridge/`: the bridge short's voice (`voice/voice.wav`, `words.json`) and final sound mix (`audio/mix.wav`).
- `vasa-short/`: the Vasa script (`SCRIPT.md`) and the voice generator. The Vasa scenes are still to be built.
- `bridge_short.mp4`: the 10 fps cloud preview of the bridge short.

## 1. Install (once)
1. Node.js 20 or 22 LTS: https://nodejs.org
2. Python 3.11+ (tick "Add to PATH"), then `pip install numpy scipy soundfile kokoro-onnx`
3. ffmpeg: `winget install Gyan.FFmpeg`
4. Git: `winget install Git.Git`
5. Claude Code: https://code.claude.com, then `claude auth login` with the same claude.ai account
6. The skill: `git clone https://github.com/mromidev/claude-animated-shorts "%USERPROFILE%\.claude\skills\cartoon-3d-short"`
7. Update your NVIDIA driver (GTX 1060 works).

## 2. Get the project
```
git clone https://github.com/qamar240/test1
cd test1
git checkout ccr-b1151a73-g1js70
cd shorts
npm install
```

## 3. Continue this exact chat on your PC
From inside the `test1` folder (same repo, clean git state):
```
claude --teleport
```
Pick this session from the list. Alternatives: on claude.ai/code open the session menu > Open in > Terminal and paste
the command it copies, or type `/teleport` in a running `claude`. The move is one-way: new work on the PC stays on the PC.

## 4. Render the bridge short in 4K (2160x3840) on the GTX 1060
```
cd shorts
set REMOTION_TMP=D:\remotion-tmp
npx remotion render src/index.ts BridgeShort out/bridge_4k.mp4 --codec h264 --crf 16 --scale 2 --gl=angle --concurrency=1
ffmpeg -i out/bridge_4k.mp4 -i audio-bridge/audio/mix.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -shortest bridge_4k_final.mp4
```
- `--scale 2` = 4K. Use `--scale 1.3333` for 2K (1440x2560), which is much faster.
- Keep `--concurrency=1` or `2`: 6 GB of VRAM is the limit at 4K.
- If the render is very slow, Chrome is using software graphics. Try `--gl=angle-egl` or `--gl=vulkan`.
- First test a few frames: add `--frames=0-59`.
