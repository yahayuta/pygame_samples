
import numpy as np
import wave
import os

SAMPLE_RATE = 44100

def generate_sound(path, frequency, duration, volume=0.1):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    amplitude = np.iinfo(np.int16).max * volume
    data = amplitude * np.sin(2 * np.pi * frequency * t)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.astype(np.int16).tobytes())

def generate_dig_sound(path):
    # A short, low-pitched sound
    generate_sound(path, 100, 0.1, volume=0.05)

def generate_pump_sound(path):
    # A quick rising pitch
    t = np.linspace(0, 0.15, int(SAMPLE_RATE * 0.15), False)
    frequency = np.linspace(400, 800, len(t))
    amplitude = np.iinfo(np.int16).max * 0.05
    data = amplitude * np.sin(2 * np.pi * frequency * t)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.astype(np.int16).tobytes())

def generate_pop_sound(path):
    # A short burst of noise
    duration = 0.2
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    decay = np.exp(-t * 10)
    amplitude = np.iinfo(np.int16).max * 0.1
    data = amplitude * noise * decay
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.astype(np.int16).tobytes())

def generate_rock_sound(path):
    # A rumbling noise
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    noise = np.random.uniform(-1, 1, len(t))
    amplitude = np.iinfo(np.int16).max * 0.08
    data = amplitude * noise
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.astype(np.int16).tobytes())

def generate_death_sound(path):
    # A descending tone
    duration = 0.5
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    frequency = np.linspace(800, 200, len(t))
    amplitude = np.iinfo(np.int16).max * 0.1
    data = amplitude * np.sin(2 * np.pi * frequency * t)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(data.astype(np.int16).tobytes())

if __name__ == '__main__':
    ASSETS_DIR = 'assets'
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)

    generate_dig_sound(os.path.join(ASSETS_DIR, 'dig.wav'))
    generate_pump_sound(os.path.join(ASSETS_DIR, 'pump.wav'))
    generate_pop_sound(os.path.join(ASSETS_DIR, 'pop.wav'))
    generate_rock_sound(os.path.join(ASSETS_DIR, 'rock.wav'))
    generate_death_sound(os.path.join(ASSETS_DIR, 'death.wav'))

    print("Dig Dug sounds generated successfully!")
