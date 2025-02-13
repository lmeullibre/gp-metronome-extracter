# Guitar Pro Metronome Generator

A Python script that generates a metronome track from Guitar Pro files.
## Features

- Extracts tempo information from Guitar Pro (.gp) files
- Generates a WAV file containing metronome clicks
- Supports variable tempo changes throughout the piece
- Maintains accurate timing based on the original score's tempo markings

## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  - numpy

## Installation

1. Clone this repository or download the script
2. Install the required packages:
```bash
pip install numpy
```

## Usage

Run the script from the command line with two arguments:
1. Path to the input Guitar Pro file
2. Desired output WAV file path

```bash
python metronome_generator.py input.gp output.wav
```

Example:
```bash
python metronome_generator.py mysong.gp mysong_metronome.wav
```

## How It Works

1. Extracts the `score.gpif` file from the Guitar Pro file (XML format)
2. Parses the XML to find tempo changes and their positions
3. Generates click sounds at appropriate intervals
4. Creates a WAV file with the metronome track

## Technical Details

- Sample rate: 44100 Hz
- Audio format: 16-bit mono WAV
- Click duration: 0.02 seconds
- Click frequency: 1000 Hz
- Default time signature: 4/4 (four beats per bar)

## Future Work

- Customizable click sounds:
  - Allow users to select custom sound sources for metronome clicks
  - Support different sounds for the first beat of each bar (accent beat)
- Extended format support:
  - Add support for .mp3 export
  - Add compatibility with legacy Guitar Pro formats (.gpx, .gp5)
  - Implement broader Guitar Pro version compatibility
- Enhanced features:
  - Support for different time signatures
  - Visual metronome interface
  - Real-time tempo adjustment

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.
