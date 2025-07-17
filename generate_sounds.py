import numpy as np
import wave
import struct
import os

def create_sound_file(filename, frequency, duration, volume=0.3, sample_rate=44100):
    """Generate a simple sine wave sound file"""
    
    # Create the audio data
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    audio_data = np.sin(2 * np.pi * frequency * t) * volume
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Create WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_explosion_sound(filename):
    """Create explosion sound with multiple frequencies"""
    sample_rate = 44100
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Multiple frequencies for explosion effect
    audio_data = (np.sin(2 * np.pi * 100 * t) * 0.2 +  # Low frequency
                  np.sin(2 * np.pi * 200 * t) * 0.15 +  # Medium frequency
                  np.sin(2 * np.pi * 400 * t) * 0.1)    # High frequency
    
    # Add decay
    decay = np.exp(-3 * t)
    audio_data = audio_data * decay * 0.3
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_shoot_sound(filename):
    """Create shooting sound"""
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # High frequency sound that drops
    frequency = 800 * np.exp(-5 * t)  # Frequency drops from 800 to ~0
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.2
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_hit_sound(filename):
    """Create hit sound"""
    sample_rate = 44100
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Multiple frequencies for hit effect
    audio_data = (np.sin(2 * np.pi * 300 * t) * 0.15 +
                  np.sin(2 * np.pi * 600 * t) * 0.1)
    
    # Add decay
    decay = np.exp(-4 * t)
    audio_data = audio_data * decay * 0.25
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_ping_sound(filename):
    """Create ping sound for Pong"""
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Clean ping sound
    audio_data = np.sin(2 * np.pi * 800 * t) * 0.2
    
    # Add slight decay
    decay = np.exp(-2 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_pong_sound(filename):
    """Create pong sound for wall hits"""
    sample_rate = 44100
    duration = 0.15
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Lower frequency for wall hit
    audio_data = np.sin(2 * np.pi * 400 * t) * 0.15
    
    # Add decay
    decay = np.exp(-3 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_get_sound(filename):
    """Create get sound for scoring"""
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Rising frequency for scoring
    frequency = 400 + 400 * t / duration
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.2
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_brick_sound(filename):
    """Create brick breaking sound"""
    sample_rate = 44100
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Multiple frequencies for brick breaking
    audio_data = (np.sin(2 * np.pi * 200 * t) * 0.1 +
                  np.sin(2 * np.pi * 400 * t) * 0.08 +
                  np.sin(2 * np.pi * 800 * t) * 0.05)
    
    # Add decay
    decay = np.exp(-2 * t)
    audio_data = audio_data * decay * 0.3
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_paddle_sound(filename):
    """Create paddle hit sound"""
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Simple paddle hit sound
    audio_data = np.sin(2 * np.pi * 600 * t) * 0.15
    
    # Add slight decay
    decay = np.exp(-1 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_wall_sound(filename):
    """Create wall hit sound"""
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Lower frequency for wall hit
    audio_data = np.sin(2 * np.pi * 300 * t) * 0.1
    
    # Add decay
    decay = np.exp(-2 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_invader_killed_sound(filename):
    """Create invader killed sound"""
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Multiple frequencies for alien death
    audio_data = (np.sin(2 * np.pi * 200 * t) * 0.1 +
                  np.sin(2 * np.pi * 400 * t) * 0.08)
    
    # Add decay
    decay = np.exp(-3 * t)
    audio_data = audio_data * decay * 0.25
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_end_sound(filename):
    """Create game end sound"""
    sample_rate = 44100
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Descending tone for game end
    frequency = 600 * np.exp(-2 * t)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.2
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_win_sound(filename):
    """Create win sound"""
    sample_rate = 44100
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Ascending tones for win
    frequency = 400 + 600 * t / duration
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.2
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_start_sound(filename):
    """Create start sound"""
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Simple start sound
    audio_data = np.sin(2 * np.pi * 500 * t) * 0.15
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_eat_sound(filename):
    """Create eat sound for Snake"""
    sample_rate = 44100
    duration = 0.15
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Quick, satisfying eat sound
    frequency = 600 + 200 * t / duration
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.2
    
    # Add slight decay
    decay = np.exp(-1 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_game_over_sound(filename):
    """Create game over sound for Snake"""
    sample_rate = 44100
    duration = 0.4
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Descending tone for game over
    frequency = 400 * np.exp(-1.5 * t)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.25
    
    # Add decay
    decay = np.exp(-2 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_power_sound(filename):
    """Create power pellet sound for Pac-Man"""
    sample_rate = 44100
    duration = 0.3
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Ascending power sound
    frequency = 300 + 400 * t / duration
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Add slight decay
    decay = np.exp(-1 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_ghost_eaten_sound(filename):
    """Create ghost eaten sound for Pac-Man"""
    sample_rate = 44100
    duration = 0.2
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Quick, satisfying ghost eaten sound
    frequency = 800 + 600 * t / duration
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.25
    
    # Add decay
    decay = np.exp(-2 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def create_death_sound(filename):
    """Create death sound for Pac-Man"""
    sample_rate = 44100
    duration = 0.5
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Descending death sound
    frequency = 600 * np.exp(-2 * t)
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Add decay
    decay = np.exp(-1.5 * t)
    audio_data = audio_data * decay
    
    # Convert to 16-bit integers
    audio_data = (audio_data * 32767).astype(np.int16)
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

def main():
    """Generate all sound files"""
    
    # Create sound directories
    sound_dirs = [
        'space_invaders/sound_files',
        'pong/sound_files', 
        'breakout/sound_files',
        'tictactoe/sound_files',
        'slot_machine/sound_files',
        'torpedo_attack/sound_files',
        'snake/sound_files',
        'pacman/sound_files'
    ]
    
    for sound_dir in sound_dirs:
        os.makedirs(sound_dir, exist_ok=True)
    
    # Generate Space Invaders sounds
    create_shoot_sound('space_invaders/sound_files/shoot.wav')
    create_explosion_sound('space_invaders/sound_files/explosion.wav')
    create_invader_killed_sound('space_invaders/sound_files/invaderkilled.wav')
    
    # Generate Pong sounds
    create_ping_sound('pong/sound_files/ping.mp3')
    create_pong_sound('pong/sound_files/pong.mp3')
    create_get_sound('pong/sound_files/get.mp3')
    
    # Generate Breakout sounds
    create_paddle_sound('breakout/sound_files/paddle.mp3')
    create_brick_sound('breakout/sound_files/brick.mp3')
    create_wall_sound('breakout/sound_files/wall.mp3')
    
    # Generate Tic Tac Toe sounds
    create_hit_sound('tictactoe/sound_files/hit.mp3')
    create_end_sound('tictactoe/sound_files/end.mp3')
    
    # Generate Slot Machine sounds
    create_start_sound('slot_machine/sound_files/start.mp3')
    create_win_sound('slot_machine/sound_files/win.wav')
    
    # Generate Torpedo Attack sounds (reuse existing)
    create_shoot_sound('torpedo_attack/sound_files/shoot.wav')
    create_explosion_sound('torpedo_attack/sound_files/explosion.wav')
    
    # Generate Snake sounds
    create_eat_sound('snake/sound_files/eat.wav')
    create_game_over_sound('snake/sound_files/game_over.wav')
    
    # Generate Pac-Man sounds
    create_eat_sound('pacman/sound_files/eat.wav')
    create_power_sound('pacman/sound_files/power.wav')
    create_ghost_eaten_sound('pacman/sound_files/ghost_eaten.wav')
    create_death_sound('pacman/sound_files/death.wav')
    
    print("✅ All sound files generated successfully!")
    print("Generated sounds for:")
    print("- Space Invaders: shoot.wav, explosion.wav, invaderkilled.wav")
    print("- Pong: ping.mp3, pong.mp3, get.mp3")
    print("- Breakout: paddle.mp3, brick.mp3, wall.mp3")
    print("- Tic Tac Toe: hit.mp3, end.mp3")
    print("- Slot Machine: start.mp3, win.wav")
    print("- Torpedo Attack: shoot.wav, explosion.wav")
    print("- Snake: eat.wav, game_over.wav")
    print("- Pac-Man: eat.wav, power.wav, ghost_eaten.wav, death.wav")

if __name__ == "__main__":
    os.makedirs('asteroids/sound_files', exist_ok=True)
    create_shoot_sound('asteroids/sound_files/shoot.wav')
    create_explosion_sound('asteroids/sound_files/explosion.wav')
    create_hit_sound('asteroids/sound_files/hit.wav')
    create_game_over_sound('asteroids/sound_files/game_over.wav')
    print('Asteroids sound effects generated.')
    main() 