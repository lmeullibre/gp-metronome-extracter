import xml.etree.ElementTree as ET
import numpy as np
import wave
import zipfile
import os
import argparse
import subprocess

def extract_gpif(gp_file):
    """Extracts score.gpif from a .gp file."""
    with zipfile.ZipFile(gp_file, 'r') as zip_ref:
        zip_ref.extract("Content/score.gpif", "temp")
    return "temp/Content/score.gpif"

def parse_tempo_changes(file_path):
    """Extracts tempo changes and total bars from a Guitar Pro XML file."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    tempos = []
    
    default_tempo = root.find(".//Score/Properties/Tempo")
    if default_tempo is not None:
        default_bpm = int(default_tempo.text.split()[0])
        tempos.append((0, 0, default_bpm))
    else:
        tempos.append((0, 0, 120))
    
    for automation in root.findall(".//Automation[Type='Tempo']"):
        bar = int(automation.find("Bar").text)
        position_decimal = float(automation.find("Position").text)
        position = int(position_decimal * 960)  # Convert to internal GP position
        tempo_value = automation.find("Value").text.split()[0]
        bpm = int(tempo_value)
        tempos.append((bar, position, bpm))
    
    total_bars = 0
    bars = root.findall(".//Score/Bars/Bar")
    if bars:
        total_bars = len(bars)
    else:
        master_bars = root.findall(".//MasterBar")
        if master_bars:
            total_bars = len(master_bars)
    
    if tempos:
        total_bars = max(total_bars, max(bar for bar, _, _ in tempos) + 1)
    
    tempos.sort(key=lambda x: (x[0], x[1]))
    
    return tempos, total_bars

def generate_click_sound(sample_rate=22050, duration=0.005, frequency=1000):
    """Generates a short metronome click sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    click = 0.5 * np.sin(2 * np.pi * frequency * t)
    click = (click * 127).astype(np.int8)  # Convert to 8-bit
    return click

def create_metronome_track(tempos, bars, beats_per_bar=4, sample_rate=22050):
    """Creates a metronome track as a NumPy array."""
    if not tempos:
        raise ValueError("No tempo information available")
    
    click = generate_click_sound(sample_rate)
    silence = np.zeros(int(sample_rate * 0.02), dtype=np.int8)  # Shorter silence
    
    metronome_track = []
    tempo_index = 0
    
    for bar in range(bars):
        for beat in range(beats_per_bar):
            current_position = (beat * 960) // beats_per_bar
            
            while (tempo_index + 1 < len(tempos) and 
                   (tempos[tempo_index + 1][0] < bar or 
                    (tempos[tempo_index + 1][0] == bar and 
                     tempos[tempo_index + 1][1] <= current_position))):
                tempo_index += 1
            
            current_tempo = tempos[tempo_index][2]
            
            beat_duration = 60.0 / current_tempo
            samples_per_beat = int(beat_duration * sample_rate)
            
            if beat == 0: 
                metronome_track.extend(click * 2)
            else:
                metronome_track.extend(click)
            
            metronome_track.extend(silence)
            
            remaining_samples = samples_per_beat - len(click) - len(silence)
            if remaining_samples > 0:
                metronome_track.extend(np.zeros(remaining_samples, dtype=np.int8))
    
    return np.array(metronome_track, dtype=np.int8)

def save_as_wav(filename, audio_data, sample_rate=22050):
    """Saves the generated audio as an optimized .wav file (8-bit, 22kHz)."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(1)  # 8-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())

    print(f"Optimized metronome track saved as {filename}")

def save_as_mp3(filename, audio_data, sample_rate=22050, bitrate="64k"):
    """Converts and saves the metronome track as an MP3 using FFmpeg."""
    wav_filename = filename.replace(".mp3", ".wav")
    save_as_wav(wav_filename, audio_data, sample_rate)

    subprocess.run(["ffmpeg", "-i", wav_filename, "-b:a", bitrate, filename], check=True)
    os.remove(wav_filename)

    print(f"Metronome track saved as {filename} (MP3)")

def main():
    """Main function to process the .gp file and generate a metronome track."""
    parser = argparse.ArgumentParser(description="Extract a metronome track from a Guitar Pro file.")
    parser.add_argument("input_file", help="Path to the Guitar Pro (.gp) file.")
    parser.add_argument("output_file", help="Path to save the metronome track (MP3 or WAV).")
    parser.add_argument("--format", choices=["wav", "mp3"], default="mp3", help="Output file format.")
    args = parser.parse_args()
    
    gpif_path = extract_gpif(args.input_file)
    tempos, total_bars = parse_tempo_changes(gpif_path)
    metronome_audio = create_metronome_track(tempos, bars=total_bars)
    
    if args.format == "mp3":
        save_as_mp3(args.output_file, metronome_audio)
    else:
        save_as_wav(args.output_file, metronome_audio)

if __name__ == "__main__":
    main()
