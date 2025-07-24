import wave
import struct
import os
import math

# Function to generate a simple sound wave
def generate_wave(file_path, frequency, duration, amplitude):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    with wave.open(file_path, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            value = int(amplitude * 32767.0 * math.sin(2.0 * math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframesraw(data)

# Generate collision sound
collision_path = os.path.join('frogger', 'assets', 'sounds', 'collision.wav')
generate_wave(collision_path, frequency=440, duration=0.2, amplitude=0.5)

# Generate score sound
score_path = os.path.join('frogger', 'assets', 'sounds', 'score.wav')
generate_wave(score_path, frequency=880, duration=0.2, amplitude=0.5)

# Generate move sound
move_path = os.path.join('frogger', 'assets', 'sounds', 'move.wav')
generate_wave(move_path, frequency=660, duration=0.1, amplitude=0.3)

print("Sound files generated successfully!")
