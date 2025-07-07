
import numpy as np

def adsr_envelope(attack, decay, sustain, release, sustain_level, sample_rate, duration):

    total_samples = max(1, int(sample_rate * duration))
    attack_samples = max(1, int(sample_rate * attack))
    decay_samples = max(1, int(sample_rate * decay))
    release_samples = max(1, int(sample_rate * release))

    # Calculate remaining samples for sustain
    sustain_samples = max(1, total_samples - attack_samples - decay_samples - release_samples)

    # Create the envelope phases
    attack_curve = np.linspace(0, 1, attack_samples)
    decay_curve = np.linspace(1, sustain_level, decay_samples)
    sustain_curve = np.ones(sustain_samples) * sustain_level
    release_curve = np.linspace(sustain_level, 0, release_samples)

    # Concatenate the phases
    envelope = np.concatenate([attack_curve, decay_curve, sustain_curve, release_curve])
    return envelope[:total_samples] 

def piano_note(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Fundamental frequency
    wave = np.sin(2 * np.pi * frequency * t)
    
    # Add harmonics
    wave += 0.5 * np.sin(2 * np.pi * 2 * frequency * t)  # Second harmonic
    wave += 0.5 * np.sin(2 * np.pi * 3 * frequency * t)  # Third harmonic
    wave += 0.5 * np.sin(2 * np.pi * 4 * frequency * t)  # Fourth harmonic
    wave += 0.05 * (wave**3)
    adsr = [0.01, 0.2, 0.2, 0.7]
    adsr = [adsr[0]]+[(duration-adsr[0])*(x/sum(adsr[1:])) for x in adsr[1:]]
    # Apply ADSR envelope
    envelope = adsr_envelope(adsr[0],adsr[1],adsr[2],adsr[3],.7, sample_rate, duration)
    wave *= envelope

    # Add slight noise 
    wave += 0.001 * np.random.normal(-1, 1, len(wave))

    # Normalize wave
    wave = wave / np.max(np.abs(wave))
    return wave

def banjo_note(frequency, duration, sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Fundamental frequency
    wave = np.sin(2 * np.pi * frequency * t)

    # Add harmonics (stronger high-frequency harmonics)
    wave += 0.7 * np.sin(2 * np.pi * 2 * frequency * t)  # Second harmonic
    wave += 0.5 * np.sin(2 * np.pi * 3 * frequency * t)  # Third harmonic
    wave += 0.3 * np.sin(2 * np.pi * 4 * frequency * t)  # Fourth harmonic
    wave += 0.2 * np.sin(2 * np.pi * 5 * frequency * t)  # Fifth harmonic
    wave += 0.1 * np.sin(2 * np.pi * 6 * frequency * t)  # Sixth harmonic

    # Introduce slight detuning for resonance
    wave += 0.1 * np.sin(2 * np.pi * 1.01 * frequency * t)
    wave += 0.08 * np.sin(2 * np.pi * 0.99 * frequency * t)

    # Nonlinearity for brightness
    wave += 0.2 * (wave**3)

    # Banjo ADSR envelope (shorter attack, minimal sustain, quick release)
    adsr = [0.003, 0.08, 0.02, 0.1]
    adsr = [adsr[0]] + [(duration - adsr[0]) * (x / sum(adsr[1:])) for x in adsr[1:]]
    envelope = adsr_envelope(adsr[0], adsr[1], adsr[2], adsr[3], 0.2, sample_rate, duration)

    # Apply envelope
    wave *= envelope

    # Bandpass filter to emphasize mid and high frequencies
    from scipy.signal import butter, sosfilt
    sos = butter(10, [500, 4000], btype="band", fs=sample_rate, output="sos")
    wave = sosfilt(sos, wave)

    # Normalize wave
    wave = wave / np.max(np.abs(wave))
    return wave

def sine_note(frequency, duration, sample_rate,envel = True):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # Fundamental frequency
    wave = np.sin(2 * np.pi * frequency * t)
    adsr = [0.01, 0.2, 0.2, 0.7]
    adsr = [adsr[0]]+[(duration-adsr[0])*(x/sum(adsr[1:])) for x in adsr[1:]]
    # Apply ADSR envelope
    envelope = adsr_envelope(adsr[0],adsr[1],adsr[2],adsr[3],.7, sample_rate, duration)
    if envel:
        wave *= envelope

    # Normalize wave
    wave = wave / np.max(np.abs(wave))
    return wave