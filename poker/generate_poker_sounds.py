import os
import numpy as np
import wave

SOUNDS = {
    'deal':    (440, 0.08),   # A4 short
    'bet':     (523, 0.12),   # C5
    'call':    (587, 0.12),   # D5
    'raise':   (659, 0.15),   # E5
    'fold':    (220, 0.18),   # A3
    'draw':    (392, 0.10),   # G4
    'win':     (784, 0.25),   # G5
    'lose':    (130, 0.25),   # C3
    'gameover':(100, 0.5),    # Low C
}

RATE = 44100
VOLUME = 0.5

# Change output directory to 'poker/sounds'
sound_dir = os.path.join('poker', 'sounds')
os.makedirs(sound_dir, exist_ok=True)

def write_tone(filename, freq, duration):
    t = np.linspace(0, duration, int(RATE * duration), False)
    tone = np.sin(freq * 2 * np.pi * t) * VOLUME
    audio = (tone * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(RATE)
        wf.writeframes(audio.tobytes())

for name, (freq, dur) in SOUNDS.items():
    path = os.path.join(sound_dir, f'{name}.wav')
    write_tone(path, freq, dur)
    print(f'Generated {path}') 