import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import threading

def generate_click(samplerate=44100):
    """Generates a short, percussive click sound."""
    duration = 0.1  # 10ms for sharp click
    samples = int(samplerate * duration)

    # White noise burst
    noise = np.random.uniform(-1.0, 1.0, samples) * 0.5  

    # Apply an envelope for fast decay
    envelope = np.linspace(1, 0, samples)  # Fast fade-out
    click_sound = noise * envelope

    return click_sound.astype(np.float32), duration  # Return both sound & duration

def generate_tone(frequency=1000, duration=0.1, samplerate=44100):
    """Generates a beep sound for count-in."""
    t = np.linspace(0, duration, int(samplerate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32), duration  # Return both sound & duration

def metronome_thread(bpm, num_clicks,count_in):
    """Plays a count-in (8 beeps) followed by exactly `num_clicks` metronome clicks."""
    global recording_active
    beat_interval = 60.0 / bpm  # Exact time per beat (seconds)

    beep_sound, beep_duration = generate_tone(frequency=1000, duration=0.1)  # Count-in sound
    click_sound, click_duration = generate_click()  # Sharp click

    with sd.OutputStream(samplerate=44100, channels=1) as stream:
        start_time = time.monotonic()  # Start timing reference

        # Count-in (8 beeps)
        for _ in range(count_in):
            if not recording_active:
                return
            stream.write(beep_sound)
            next_beat_time = start_time + (_ + 1) * beat_interval
            time.sleep(max(0, next_beat_time - time.monotonic()))  # Sync precisely

        # Play exactly `num_clicks` metronome clicks
        for i in range(num_clicks):
            if not recording_active:
                return
            stream.write(click_sound)
            next_beat_time = start_time + (i + 9) * beat_interval  # Continue timing after count-in
            time.sleep(max(0, next_beat_time - time.monotonic()))  # Sync precisely

def record_audio_with_metronome(bpm, num_clicks, samplerate,count_in):
    """Records audio while playing exactly `num_clicks` metronome clicks after a count-in."""
    global recording_active
    recording_active = True

    # Calculate recording duration (8 count-in beeps + num_clicks clicks)
    duration = ((num_clicks + count_in) * 60) / bpm  

    print(f"Recording for {duration:.2f} seconds with metronome at {bpm} BPM...")

    # Start the metronome in a separate thread
    metronome_threading = threading.Thread(target=metronome_thread, args=(bpm, num_clicks,count_in))
    metronome_threading.start()
    
    time.sleep(0.1)  # Ensures metronome starts before recording

    # Start recording
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=2, dtype=np.int16)
    audio_data = np.mean(audio_data, axis=1, dtype=np.int16)
    sd.wait()  # Ensure the recording completes

    recording_active = False  # Stop metronome after recording
    metronome_threading.join()

    # Save the recording
    return audio_data
    print(f"Recording saved as {filename}")

# Example usage
#bpm = 200
#num_clicks = 65 # Play exactly 64 clicks
#count_in = 9
#record_audio_with_metronome("metronome_record2.wav", bpm=bpm, num_clicks=num_clicks,count_in=count_in,samplerate=44100)
