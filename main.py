import xml.etree.ElementTree as ET
import numpy as np
import wave
import zipfile
import os
import argparse

def extract_gpif(gp_file):
    """Extracts score.gpif from a .gp file."""
    with zipfile.ZipFile(gp_file, 'r') as zip_ref:
        zip_ref.extract("Content/score.gpif", "temp")
    return "temp/Content/score.gpif"

def parse_tempo_changes(file_path):
    """Extracts tempo changes and total bars from a Guitar Pro XML file."""
    """Extracts tempo changes from a Guitar Pro XML file."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    tempos = []
    for automation in root.findall(".//Automation[Type='Tempo']"):
        bar = int(automation.find("Bar").text)
        position = int(automation.find("Position").text)
        bpm = int(automation.find("Value").text.split()[0])
        tempos.append((bar, position, bpm))
    
        total_bars = max(bar for bar, _, _ in tempos) + 1 if tempos else 0
    return tempos, total_bars

def generate_click_sound(sample_rate=44100, duration=0.02, frequency=1000):
    """Generates a short metronome click sound."""
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    click = 0.5 * np.sin(2 * np.pi * frequency * t)
    click = (click * 32767).astype(np.int16)
    return click

def create_metronome_track(tempos, bars, beats_per_bar=4, sample_rate=44100):
    """Creates a .wav file metronome track based on tempo changes."""
    click = generate_click_sound(sample_rate)
    silence = np.zeros(int(sample_rate * 0.05), dtype=np.int16) 
    
    tempo_map = {bar: bpm for bar, _, bpm in tempos}
    
    metronome_track = []
    for bar in range(bars):
        bpm = tempo_map.get(bar, tempos[0][2])
        interval = 60 / bpm 
        samples_per_beat = int(interval * sample_rate)
        
        for _ in range(beats_per_bar):
            metronome_track.extend(click)
            metronome_track.extend(silence)
            metronome_track.extend(np.zeros(samples_per_beat - len(click) - len(silence), dtype=np.int16))
    
    return np.array(metronome_track, dtype=np.int16)

def save_as_wav(filename, audio_data, sample_rate=44100):
    """Saves the generated audio as a .wav file."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"Metronome track saved as {filename}")

def main():
    """Main function to process the .gp file and generate a metronome track."""
    parser = argparse.ArgumentParser(description="Extract a metronome track from a Guitar Pro file.")
    parser.add_argument("input_file", help="Path to the Guitar Pro (.gp) file.")
    parser.add_argument("output_file", help="Path to save the metronome track as .wav.")
    args = parser.parse_args()
    
    gpif_path = extract_gpif(args.input_file)
    tempos, total_bars = parse_tempo_changes(gpif_path)
    metronome_audio = create_metronome_track(tempos, bars=total_bars)
    save_as_wav(args.output_file, metronome_audio)
    
    # Cleanup
    os.remove(gpif_path)
    os.rmdir("temp/Content")
    os.rmdir("temp")

if __name__ == "__main__":
    main()
