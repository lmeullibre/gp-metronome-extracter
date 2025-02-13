# Guitar Pro Metronome Extractor

  

A Python package that generates a metronome track from Guitar Pro files.

  

## Features

  

- Extracts tempo information from Guitar Pro (`.gp`) files.

- Generates a WAV file containing metronome clicks.

- Supports variable tempo changes throughout the piece.

- Supports tempo changes in the middle of a bar.

  

## Installation

  

You can install the package directly from PyPI using `pip`:

  

```bash

pip  install  metronome_extractor

```

  

## Usage

### As a Python Package

  

    from metronome_extractor import create_metronome_track, save_as_wav

  

# Example: Generate a metronome track from a Guitar Pro file

    input_file = "input.gp"
    
    output_file = "output.wav"

  

# Extract tempo information and generate the metronome track

    tempos, total_bars = parse_tempo_changes(extract_gpif(input_file))
    
    metronome_audio = create_metronome_track(tempos, bars=total_bars)
    
    save_as_wav(output_file, metronome_audio)

  

### As a Command-Line Tool

  

```

metronome_extractor input.gp output.wav

```

  

## How it works

1. Extracts the score.gpif file from the Guitar Pro file (XML format).

2. Parses the XML to find tempo changes and their positions.

3. Generates click sounds at appropriate intervals.

4. Creates a WAV file with the metronome track.

  

## Technical Details

* Sample rate: 44100 Hz

* Audio format: 16-bit mono WAV

* Click duration: 0.02 seconds

* Click frequency: 1000 Hz

* Default time signature: 4/4 (four beats per bar)

  

## Future Work

  

- **Customizable click sounds**  
  - Allow users to select custom sound sources for metronome clicks.  
  - Support different sounds for the first beat of each bar (accent beat).  

- **Extended format support**  
  - Add support for `.mp3` export.  
  - Add compatibility with legacy Guitar Pro formats (`.gpx`, `.gp5`).  
  - Implement broader Guitar Pro version compatibility.  

  

## Contributing

  

Feel free to submit issues and enhancement requests! Contributions are welcome.

  

1. Fork the repository.

2. Create a new branch for your feature or bugfix.

3. Submit a pull request.

  

## License

  

This project is open source and available under the [MIT License](LICENSE).
