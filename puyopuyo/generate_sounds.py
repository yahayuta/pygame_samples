
import pygame
import numpy as np
import os
import wave

# Ensure the sound_files directory exists
if not os.path.exists('sound_files'):
    os.makedirs('sound_files')

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    # Fade out
    fade_out = np.linspace(1, 0, int(sample_rate * 0.05)) # 50ms fade out
    wave[len(wave)-len(fade_out):] *= fade_out
    return (wave * 32767).astype(np.int16)

def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a square wave sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    return (wave * 32767).astype(np.int16)

def generate_pop_sound(start_freq, end_freq, duration, sample_rate=44100, amplitude=0.4):
    """Generate a sound that quickly sweeps in frequency."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency = np.linspace(start_freq, end_freq, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    # Apply a decay envelope
    decay = np.exp(-t * 10)
    wave *= decay
    return (wave * 32767).astype(np.int16)

def generate_chord(frequencies, duration, sample_rate=44100, amplitude=0.25):
    """Generate a chord from multiple frequencies."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += amplitude * np.sin(2 * np.pi * freq * t)
    # Fade out
    fade_out = np.linspace(1, 0, int(sample_rate * 0.05)) # 50ms fade out
    wave[len(wave)-len(fade_out):] *= fade_out
    return (wave * 32767).astype(np.int16)

def save_sound(wave_data, filename, sample_rate=44100):
    """Save a sound wave to a WAV file."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())

def main():
    pygame.mixer.init(44100, -16, 1, 512)
    
    # Set the working directory to the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    sound_dir = 'sound_files'
    if not os.path.exists(sound_dir):
        os.makedirs(sound_dir)
        
    print("Generating Puyo Puyo sound effects...")
    
    # Rotation sound
    rotate_sound = generate_sine_wave(1200, 0.05)
    save_sound(rotate_sound, os.path.join(sound_dir, 'rotate.wav'))
    print(" Generated rotate.wav")
    
    # Landing sound
    land_sound = generate_square_wave(150, 0.1)
    save_sound(land_sound, os.path.join(sound_dir, 'land.wav'))
    print(" Generated land.wav")
    
    # Pop sound
    pop_sound = generate_pop_sound(800, 1600, 0.1)
    save_sound(pop_sound, os.path.join(sound_dir, 'pop.wav'))
    print(" Generated pop.wav")

    # Combo sounds
    combo_sound_2 = generate_chord([523, 659, 784], 0.2) # C Major
    save_sound(combo_sound_2, os.path.join(sound_dir, 'combo2.wav'))
    print(" Generated combo2.wav")
    
    combo_sound_3 = generate_chord([587, 740, 880], 0.25) # D# Major
    save_sound(combo_sound_3, os.path.join(sound_dir, 'combo3.wav'))
    print(" Generated combo3.wav")

    combo_sound_4 = generate_chord([659, 830, 987], 0.3) # E Major
    save_sound(combo_sound_4, os.path.join(sound_dir, 'combo4.wav'))
    print(" Generated combo4.wav")

    # Game Over sound
    game_over_sound = generate_square_wave(200, 0.5)
    save_sound(game_over_sound, os.path.join(sound_dir, 'game_over.wav'))
    print(" Generated game_over.wav")
    
    print("\nAll sound effects generated successfully!")
    print(f"Sound files created in the '{sound_dir}' folder.")

if __name__ == "__main__":
    main()
