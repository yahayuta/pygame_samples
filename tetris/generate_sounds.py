import pygame
import numpy as np
import os

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave sound"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return (wave * 32767).astype(np.int16)

def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a square wave sound"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    return (wave * 32767).astype(np.int16)

def generate_triangle_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a triangle wave sound"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * frequency * t))
    return (wave * 32767).astype(np.int16)

def generate_chord(frequencies, duration, sample_rate=44100, amplitude=0.3):
    """Generate a chord from multiple frequencies"""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = np.zeros_like(t)
    for freq in frequencies:
        wave += amplitude * np.sin(2 * np.pi * freq * t)
    return (wave * 32767).astype(np.int16)

def save_sound(wave, filename, sample_rate=44100):
    """Save a sound wave to a WAV file"""
    import wave as wave_module
    with wave_module.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave.tobytes())

def main():
    pygame.mixer.init(44100, -16, 1, 1024)
    
    # Always save to the tetris folder (where this script is located)
    tetris_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(tetris_dir)
    
    print("Generating Tetris sound effects...")
    
    # Move sound - short beep
    move_sound = generate_sine_wave(800, 0.1)
    save_sound(move_sound, 'move.wav')
    print("✓ Generated move.wav")
    
    # Rotate sound - higher pitch beep
    rotate_sound = generate_sine_wave(1000, 0.15)
    save_sound(rotate_sound, 'rotate.wav')
    print("✓ Generated rotate.wav")
    
    # Drop sound - low thud
    drop_sound = generate_square_wave(200, 0.2)
    save_sound(drop_sound, 'drop.wav')
    print("✓ Generated drop.wav")
    
    # Line clear sound - ascending chord
    line_clear_sound = generate_chord([400, 600, 800], 0.3)
    save_sound(line_clear_sound, 'line_clear.wav')
    print("✓ Generated line_clear.wav")
    
    # Game over sound - descending tone
    game_over_sound = generate_triangle_wave(300, 0.5)
    save_sound(game_over_sound, 'game_over.wav')
    print("✓ Generated game_over.wav")
    
    print("\nAll sound effects generated successfully!")
    print("Sound files created in the tetris folder.")

if __name__ == "__main__":
    main() 