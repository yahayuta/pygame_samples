import numpy as np
import wave
import os

def save_wav(filename, data, framerate=44100):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(framerate)
        wf.writeframes(data.astype(np.int16).tobytes())

def beep(frequency, duration, volume=0.5, framerate=44100):
    t = np.linspace(0, duration, int(framerate * duration), False)
    tone = np.sin(frequency * 2 * np.pi * t) * (volume * 32767)
    return tone

# Level up sound
levelup = np.concatenate([beep(880, 0.1), beep(1320, 0.1)])
save_wav('sound_files/levelup.wav', levelup)

# Game over sound
gameover = np.concatenate([beep(220, 0.3), beep(110, 0.2)])
save_wav('sound_files/gameover.wav', gameover)

# Background music (simple repeating tone)
bgm = np.concatenate([beep(440, 0.2), beep(660, 0.2), beep(550, 0.2), beep(660, 0.2)])
bgm = np.tile(bgm, 10)  # Repeat to make it longer
save_wav('sound_files/bgm.wav', bgm)

print('Breakout sound files generated: levelup.wav, gameover.wav, bgm.wav')
