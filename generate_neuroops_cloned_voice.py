"""Generate complete NeuroOps Duo pitch voiceover using Charan's cloned voice from charan_ref_clip.wav
via Coqui XTTS v2 on Hugging Face (eagien/XTTS).
"""

import os
import sys
import time
import subprocess
import numpy as np
import scipy.io.wavfile as wav
import imageio_ffmpeg
from gradio_client import Client, handle_file

sys.stdout.reconfigure(encoding='utf-8')

# Reference audio clip capturing Charan's exact vocal timbre and accent
REF_AUDIO_PATH = os.path.abspath(r"..\chronotrace-ai\charan_ref_clip.wav")
OUTPUT_DIR = os.path.abspath(".")

CHUNKS = [
    # Chunk 1: Already generated, but listed for completeness
    (
        "part1",
        "Hello everyone, I am Charan Jeedimetla, and this is NeuroOps Duo. "
        "Code generation is solved. But what happens next—triaging production incidents, writing regression tests, "
        "verifying mutations, securing containers, routing to green cloud regions, and passing compliance audits—is where engineering teams lose days. "
        "Welcome to NeuroOps Duo: the first 100% hands-off, 9-stage DevSecOps and carbon-adaptive production engine powered by the GitLab Duo Agent Platform, Anthropic's Model Context Protocol, and Google Cloud Run."
    ),
    # Chunk 2a
    (
        "part2a",
        "Watch closely. A critical transaction anomaly is detected in our OmniPay Gateway. Zero humans are involved. "
        "First, Stage 1: Plan—our Duo Triage Agent ingests the crash dump and maps the AST blast-radius. "
        "Next, Stage 2: Create—rather than guessing a fix, our Adversarial Tester Agent writes a reproduction test that demonstrably fails against the bug. This is Cyber Reasoning at work."
    ),
    # Chunk 2b
    (
        "part2b",
        "In Stage 3: Verify, our Remediation Agent generates the minimal AST patch and proves a 100% mutation test score. "
        "In Stages 4 and 5: Package and Secure, GitLab CI builds a hardened distroless container, signs it with Cosign, and validates zero critical CVEs."
    ),
    # Chunk 3a
    (
        "part3a",
        "Now for the game-changer: Stage 6: Release. "
        "Using the Green Software Foundation's ISO/IEC 21031 Software Carbon Intensity formula, our Carbon Arbiter Agent queries regional grid data via Model Context Protocol."
    ),
    # Chunk 3b
    (
        "part3b",
        "Instead of deploying to a fossil-heavy zone, it dynamically deploys a Canary to Google Cloud Run in europe-north1 (Hamina, Finland), which runs on 93% Carbon-Free Energy. "
        "This slashes lifecycle emissions by 79.7%. "
        "In Stage 7: Configure, the agent auto-tunes Cloud Run concurrency and activates scale-to-zero to eliminate idle carbon waste."
    ),
    # Chunk 4a
    (
        "part4a",
        "In Stage 8: Monitor, our SRE Telemetry Agent polls Google Cloud Monitoring. "
        "Error rate is 0.00%, and P99 latency is 39 milliseconds. Satisfying our strict SLOs, it automatically promotes canary traffic to 100%."
    ),
    # Chunk 4b
    (
        "part4b",
        "Finally, in Stage 9: Govern, the Compliance Auditor compiles an end-to-end cryptographic audit trail: "
        "SLSA Level 3 provenance, signed SBOM, and the official SCI scorecard, closing the incident issue automatically on GitLab."
    ),
    # Chunk 5
    (
        "part5",
        "All 9 DevSecOps stages covered. 100% hands-off autonomy. Deployed on Google Cloud with quantified carbon reduction. "
        "This is NeuroOps Duo. This is Life After Code. Thank you!"
    ),
]

def main():
    print(f"[*] Reference audio: {REF_AUDIO_PATH}")
    if not os.path.exists(REF_AUDIO_PATH):
        raise FileNotFoundError(f"Reference audio not found: {REF_AUDIO_PATH}")

    c = Client("eagien/XTTS", httpx_kwargs={"timeout": 600.0})
    print("[*] Connected to eagien/XTTS voice clone engine!")

    generated_files = []

    for name, text in CHUNKS:
        chunk_file = os.path.join(OUTPUT_DIR, f"cloned_{name}.wav")
        # Check if already exists from earlier run
        if os.path.exists(chunk_file) and os.path.getsize(chunk_file) > 50000:
            print(f"[+] Reusing existing {name} ({os.path.getsize(chunk_file)} bytes)")
            generated_files.append(chunk_file)
            continue

        print(f"\n[>] Generating {name} ({len(text)} chars)...")
        print(f"    Text: {text[:70]}...")
        max_retries = 3
        success = False
        for attempt in range(1, max_retries + 1):
            try:
                t0 = time.time()
                status, audio_path = c.predict(
                    input_text=text,
                    speaker_wav=handle_file(REF_AUDIO_PATH),
                    language="en",
                    api_name="/predict"
                )
                dur = time.time() - t0
                print(f"    Status: {status} (in {dur:.1f}s)")
                import shutil
                shutil.copy2(audio_path, chunk_file)
                print(f"[+] Saved {name} -> {chunk_file} ({os.path.getsize(chunk_file)} bytes)")
                generated_files.append(chunk_file)
                success = True
                break
            except Exception as e:
                print(f"    [!] Attempt {attempt} failed: {e}")
                time.sleep(3)
        if not success:
            raise RuntimeError(f"Failed to generate chunk {name} after {max_retries} attempts.")

    # Stitch audio tracks together
    print("\n[*] Stitching all cloned audio chunks into master track...")
    combined_audio = []
    target_sr = 24000
    pause_samples = np.zeros(int(target_sr * 0.35), dtype=np.int16)

    for idx, f in enumerate(generated_files):
        sr, data = wav.read(f)
        if sr != target_sr:
            # Resample or keep
            pass
        if data.dtype != np.int16:
            data = (data * 32767).astype(np.int16)
        combined_audio.append(data)
        if idx < len(generated_files) - 1:
            combined_audio.append(pause_samples)

    final_audio = np.concatenate(combined_audio)
    stitched_wav = os.path.join(OUTPUT_DIR, "stitched_cloned_voiceover.wav")
    wav.write(stitched_wav, target_sr, final_audio)
    total_sec = len(final_audio) / target_sr
    print(f"[SUCCESS] Stitched master WAV: {stitched_wav} (Duration: {total_sec:.2f}s)")

    # Normalize audio loudness using FFmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    final_mp3 = os.path.join(OUTPUT_DIR, "voiceover.mp3")
    cmd_norm = [
        ffmpeg, "-y",
        "-i", stitched_wav,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        final_mp3
    ]
    subprocess.run(cmd_norm, check=True)
    print(f"[SUCCESS] Normalized Master MP3: {final_mp3} ({os.path.getsize(final_mp3)} bytes)")

    # Now re-record / multiplex master demo video with this new voiceover!
    print("\n[*] Re-recording master demo video with Playwright synchronized to Charan's voice...")
    rec_script = os.path.join(OUTPUT_DIR, "record_demo_video.py")
    subprocess.run([sys.executable, rec_script], check=True)
    print("\n[COMPLETE] Video recording and multiplexing finished with Charan's exact voice!")

if __name__ == "__main__":
    main()
