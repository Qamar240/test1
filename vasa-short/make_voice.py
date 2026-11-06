# voice.wav + words.json for the Vasa short: Kokoro (am_michael), one sentence per call, word ends from prefix renders
import json, re, numpy as np, soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro
k = Kokoro('voice/kokoro.onnx', 'voice/voices.bin')
SR, SPEED, VOICE = 48000, 1.08, 'am_michael'
SAY = {"1625": "sixteen twenty-five", "1628": "sixteen twenty-eight", "64": "sixty-four", "30": "thirty", "20": "twenty",
       "333": "three hundred and thirty-three", "10th,": "tenth,"}
lines = [l for l in open('SCRIPT.md').read().split('\n\n', 1)[1].strip().split('\n') if l.strip()]
sents = []
for l in lines: sents += [s for s in re.split(r'(?<=[.?!])\s+', l.strip()) if s]
def say(ws): return ' '.join(SAY.get(w, w) for w in ws)
def gen(txt):
    a, sr = k.create(txt, voice=VOICE, speed=SPEED, lang='en-us')
    nz = np.where(np.abs(a) > 0.008)[0]
    return a[max(0, nz[0] - 120):nz[-1] + 240], sr
out, words, t = [], [], 0.35
GAP = {'.': 0.32, '?': 0.32}
for si, s in enumerate(sents):
    ws = s.split()
    a, sr = gen(say(ws)); d = len(a) / sr
    ends = []
    for n in range(1, len(ws)):
        p, _ = gen(say(ws[:n]).rstrip(',') + ',')
        ends.append(min(len(p) / sr - 0.05, d))
    ends = list(np.maximum.accumulate(ends)) + [d]
    st = 0.0
    for w, e in zip(ws, ends):
        words.append({"w": w, "s": round(t + st, 3), "e": round(t + e, 3)}); st = e
    out.append((t, resample_poly(a, 2, 1)))
    t += d + (0.55 if si == 1 else 0.3)
    print(si, f"{d:.2f}s", s[:50], flush=True)
total = t + 0.6
buf = np.zeros(int(total * SR))
for t0, a in out: s = int(t0 * SR); buf[s:s + len(a)] += a
sf.write('voice/voice.wav', (buf / np.abs(buf).max() * 0.7).astype(np.float32), SR, subtype='PCM_24')
json.dump(words, open('voice/words.json', 'w'), indent=0)
print("TOTAL", total, "words", len(words))
