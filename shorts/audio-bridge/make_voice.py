import json, numpy as np, soundfile as sf
from scipy.signal import resample_poly
from kokoro_onnx import Kokoro
k = Kokoro('kokoro.onnx', 'voices.bin')
FPS, TOTAL, SR = 30, 2025, 48000
L = [(4,"Seventy-four soldiers knocked down an iron bridge just by walking across it."),
(136,"It's 1831, and the brand new bridge over the river is the pride of the whole town."),
(286,"The men are marching home four across, every boot hitting the planks at the exact same moment."),
(446,"Halfway over, the bridge starts bouncing under their feet."),
(538,"A normal person would slow down, but these guys think it's hilarious."),
(646,"Somebody starts whistling a marching tune, and the whole column stomps along to it, a little harder every step."),
(826,"The bounce gets bigger, the chains start groaning, and nobody wants to be the one who breaks step."),
(990,"Then a single bolt snaps, and the whole end of the bridge drops into the river."),
(1138,"Luckily, the river was only two feet deep."),
(1215,"Unluckily, the river was only two feet deep."),
(1306,"You see, every bridge has a rhythm it naturally likes to sway at."),
(1414,"Ever pushed a kid on a swing? Each push is tiny, but if they all land at just the right moment, the swing goes higher and higher."),
(1623,"Seventy-four men stepping together were pushing that bridge like a swing."),
(1738,"Nobody died, but the army made a rule: never cross a bridge in step."),
(1866,"So now, the best drilled soldiers in the world cross every bridge like a crowd of tourists.")]
out = np.zeros(int(TOTAL/FPS*SR)); words = []
for i,(f,txt) in enumerate(L):
    slot = ((L[i+1][0] if i+1 < len(L) else TOTAL-20) - f)/FPS - 0.15
    sp = 1.05
    while True:
        a, sr = k.create(txt, voice='am_michael', speed=sp, lang='en-us')
        nz = np.where(np.abs(a) > 0.01)[0]; a = a[max(0,nz[0]-240):nz[-1]+480]
        if len(a)/sr <= slot or sp > 1.5: break
        sp += 0.05
    a = resample_poly(a, 2, 1); t0 = f/FPS; d = len(a)/SR
    s = int(t0*SR); out[s:s+len(a)] += a[:len(out)-s]
    ws = txt.split(); tot = sum(len(w)+1 for w in ws); c = 0
    for w in ws:
        st = t0 + d*c/tot; c += len(w)+1
        words.append({"word": w, "start": round(st,3), "end": round(t0+d*c/tot,3)})
    print(i, f"speed {sp:.2f} dur {d:.2f} slot {slot:.2f}")
sf.write('voice.wav', (out/np.abs(out).max()*0.7).astype(np.float32), SR, subtype='PCM_24')
json.dump(words, open('words.json','w'), indent=0)
