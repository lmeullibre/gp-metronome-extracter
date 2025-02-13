import numpy as np
from metronome_extractor.main import create_metronome_track, parse_tempo_changes, generate_click_sound

def test_generate_click_sound():
    sample_rate = 44100
    duration = 0.02
    frequency = 1000

    click = generate_click_sound(sample_rate, duration, frequency)

    assert isinstance(click, np.ndarray)

    expected_length = int(sample_rate * duration)
    assert len(click) == expected_length

    assert np.all(click >= -32768) and np.all(click <= 32767)

def test_parse_tempo_changes():
    xml_data = """
    <Score>
        <Properties>
            <Tempo>120 BPM</Tempo>
        </Properties>
        <MasterBars>
            <MasterBar/>
            <MasterBar/>
        </MasterBars>
    </Score>
    """
    with open("test_score.gpif", "w") as f:
        f.write(xml_data)

    tempos, total_bars = parse_tempo_changes("test_score.gpif")

    assert tempos == [(0, 0, 120)]
    assert total_bars == 2

def test_create_metronome_track():
    tempos = [(0, 0, 120)] 
    bars = 2
    metronome_audio = create_metronome_track(tempos, bars)

    assert isinstance(metronome_audio, np.ndarray)

    assert metronome_audio.dtype == np.int16