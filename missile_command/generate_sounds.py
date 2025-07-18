import wave
import struct
import math
import random
import os

def generate_launch_sound():
    """Generate a missile launch sound (ascending tone)"""
    sample_rate = 44100
    duration = 0.3
    samples = int(sample_rate * duration)
    
    # Create ascending frequency tone
    data = []
    for i in range(samples):
        # Frequency increases from 200Hz to 800Hz
        freq = 200 + (600 * i / samples)
        t = i / sample_rate
        value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))
        data.append(struct.pack('<h', value))
    
    with wave.open('launch.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(data))

def generate_explosion_sound():
    """Generate an explosion sound (noise burst)"""
    sample_rate = 44100
    duration = 0.5
    samples = int(sample_rate * duration)
    
    data = []
    for i in range(samples):
        # Create noise with decreasing amplitude
        amplitude = 0.5 * (1 - i / samples)
        value = int(32767 * amplitude * (2 * random.random() - 1))
        data.append(struct.pack('<h', value))
    
    with wave.open('explosion.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(data))

def generate_city_destruction_sound():
    """Generate a city destruction sound (low rumble)"""
    sample_rate = 44100
    duration = 0.8
    samples = int(sample_rate * duration)
    
    data = []
    for i in range(samples):
        # Low frequency rumble with decreasing amplitude
        freq = 80 + 20 * math.sin(i / 100)
        amplitude = 0.4 * (1 - i / samples)
        t = i / sample_rate
        value = int(32767 * amplitude * math.sin(2 * math.pi * freq * t))
        data.append(struct.pack('<h', value))
    
    with wave.open('city_destroyed.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(data))

def generate_game_over_sound():
    """Generate a game over sound (descending tone)"""
    sample_rate = 44100
    duration = 1.0
    samples = int(sample_rate * duration)
    
    data = []
    for i in range(samples):
        # Frequency decreases from 400Hz to 100Hz
        freq = 400 - (300 * i / samples)
        t = i / sample_rate
        value = int(32767 * 0.3 * math.sin(2 * math.pi * freq * t))
        data.append(struct.pack('<h', value))
    
    with wave.open('game_over.wav', 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(data))

if __name__ == "__main__":
    print("Generating Missile Command sound effects...")
    generate_launch_sound()
    generate_explosion_sound()
    generate_city_destruction_sound()
    generate_game_over_sound()
    print("Sound effects generated successfully!") 