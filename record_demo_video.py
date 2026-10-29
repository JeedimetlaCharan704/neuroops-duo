"""NeuroOps Duo — Master 1080p Hackathon Demo Video Recorder.
Records the 9-stage DevSecOps and carbon-adaptive autonomous execution,
choreographed synchronously with the 2-minute 54-second voiceover narration.
"""

import os
import sys
import time
import subprocess
import imageio_ffmpeg
from playwright.sync_api import sync_playwright

CURRENT_MOUSE_POS = [960, 540]

def inject_virtual_cursor(page):
    """Inject a razor-sharp SVG pointer arrow with expanding click ripple rings."""
    js_code = """
    (() => {
        if (document.getElementById('playwright-cursor-container')) return;

        const container = document.createElement('div');
        container.id = 'playwright-cursor-container';
        container.style.position = 'fixed';
        container.style.top = '0';
        container.style.left = '0';
        container.style.width = '100vw';
        container.style.height = '100vh';
        container.style.pointerEvents = 'none';
        container.style.zIndex = '2147483647';
        document.body.appendChild(container);

        const cursor = document.createElement('div');
        cursor.id = 'playwright-cursor';
        cursor.style.position = 'fixed';
        cursor.style.width = '28px';
        cursor.style.height = '28px';
        cursor.style.pointerEvents = 'none';
        cursor.style.transform = 'translate(-2px, -2px)';
        cursor.style.transition = 'transform 0.08s ease';
        cursor.innerHTML = `
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 2L22 13L13.5 15.5L10 24L4 2Z" fill="#fc6d26" stroke="#ffffff" stroke-width="2.5" stroke-linejoin="round"/>
        </svg>
        `;
        container.appendChild(cursor);

        window.addEventListener('mousemove', (e) => {
            cursor.style.left = e.clientX + 'px';
            cursor.style.top = e.clientY + 'px';
        });

        window.addEventListener('mousedown', (e) => {
            cursor.style.transform = 'translate(-2px, -2px) scale(0.85)';
            const ripple = document.createElement('div');
            ripple.style.position = 'fixed';
            ripple.style.left = e.clientX + 'px';
            ripple.style.top = e.clientY + 'px';
            ripple.style.width = '12px';
            ripple.style.height = '12px';
            ripple.style.borderRadius = '50%';
            ripple.style.backgroundColor = 'rgba(252, 109, 38, 0.4)';
            ripple.style.border = '2px solid #fc6d26';
            ripple.style.boxShadow = '0 0 16px #fc6d26';
            ripple.style.transform = 'translate(-50%, -50%)';
            ripple.style.pointerEvents = 'none';
            ripple.style.zIndex = '2147483646';
            document.body.appendChild(ripple);

            let scale = 1;
            let opacity = 1;
            const anim = setInterval(() => {
                scale += 0.25;
                opacity -= 0.06;
                ripple.style.transform = `translate(-50%, -50%) scale(${scale})`;
                ripple.style.opacity = opacity;
                if (opacity <= 0) {
                    clearInterval(anim);
                    ripple.remove();
                }
            }, 16);
        });

        window.addEventListener('mouseup', () => {
            cursor.style.transform = 'translate(-2px, -2px) scale(1.0)';
        });
    })();
    """
    page.evaluate(js_code)

def smooth_move(page, target_x, target_y, steps=25):
    global CURRENT_MOUSE_POS
    start_x, start_y = CURRENT_MOUSE_POS
    for i in range(1, steps + 1):
        t = i / steps
        ease = t * t * (3.0 - 2.0 * t)
        curr_x = start_x + (target_x - start_x) * ease
        curr_y = start_y + (target_y - start_y) * ease
        page.mouse.move(curr_x, curr_y)
        time.sleep(0.016)
    CURRENT_MOUSE_POS = [target_x, target_y]

def smooth_click(page, selector):
    box = page.locator(selector).bounding_box()
    if box:
        center_x = box["x"] + box["width"] / 2
        center_y = box["y"] + box["height"] / 2
        smooth_move(page, center_x, center_y, steps=20)
        time.sleep(0.15)
        page.mouse.down()
        time.sleep(0.12)
        page.mouse.up()
        time.sleep(0.1)

def record():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    recorded_dir = os.path.join(output_dir, "recorded_video")
    os.makedirs(recorded_dir, exist_ok=True)

    html_file = os.path.join(output_dir, "dashboard", "index.html")
    file_url = f"file:///{os.path.abspath(html_file).replace(os.sep, '/')}"

    print("[*] Launching Chromium (1920x1080) for NeuroOps Duo Recording...")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--start-maximized",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-features=Translate",
                "--hide-scrollbars",
            ],
        )

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=recorded_dir,
            record_video_size={"width": 1920, "height": 1080},
        )

        t_start = time.time()
        page = context.new_page()
        page.goto(file_url)
        page.wait_for_selector(".brand")
        page.evaluate("() => document.fonts.ready")
        inject_virtual_cursor(page)

        # Let the UI settle
        time.sleep(1.5)
        trim_offset = time.time() - t_start
        print(f"[*] Dark UI rendered & settled! Trim offset established at: {trim_offset:.2f}s")

        # -------------------------------------------------------------
        # PART 1 (0:00 - 0:28): Hook & Problem Statement
        # -------------------------------------------------------------
        print("[>] Part 1: Header, Branding, & Overview...")
        smooth_move(page, 220, 45, steps=30)   # Logo & NeuroOps Duo
        time.sleep(6.5)
        smooth_move(page, 1500, 45, steps=25)  # GitLab Duo & Google Cloud badges
        time.sleep(7.5)
        smooth_move(page, 240, 130, steps=25)  # Incident MTTR metric card
        time.sleep(6.5)
        smooth_move(page, 720, 130, steps=25)  # Lifecycle Autonomy metric card
        time.sleep(7.5)

        # -------------------------------------------------------------
        # PART 2 (0:28 - 1:12): Stages 1 to 5: Autonomous Cyber-Reasoning
        # -------------------------------------------------------------
        print("[>] Part 2: Triggering 9-Stage Autonomous DevSecOps Loop...")
        # Move to Execute button and click
        smooth_click(page, "#runBtn")
        page.evaluate("window.startDemoLifecycle()")
        time.sleep(4.0)

        # Stage 1: Plan
        print("    [Stage 1: Plan] AST Blast-Radius...")
        page.evaluate("window.advanceStage(1)")
        smooth_move(page, 100, 275, steps=25)  # Stage 1 box
        time.sleep(6.5)

        # Stage 2: Create (Adversarial reproduction test)
        print("    [Stage 2: Create] Adversarial Test...")
        page.evaluate("window.advanceStage(2)")
        smooth_move(page, 290, 275, steps=25)  # Stage 2 box
        time.sleep(6.5)
        smooth_move(page, 480, 550, steps=20)  # Terminal log view
        time.sleep(4.5)

        # Stage 3: Verify (Minimal AST patch & 100% mutation score)
        print("    [Stage 3: Verify] 100% Mutation Score...")
        page.evaluate("window.advanceStage(3)")
        smooth_move(page, 480, 275, steps=25)  # Stage 3 box
        time.sleep(5.0)
        smooth_move(page, 1500, 630, steps=25) # Audit card: Mutation Score
        time.sleep(6.0)

        # Stage 4: Package (Distroless image & SBOM)
        print("    [Stage 4: Package] Hardened Container...")
        page.evaluate("window.advanceStage(4)")
        smooth_move(page, 680, 275, steps=25)
        time.sleep(6.5)

        # Stage 5: Secure (Zero critical CVEs)
        print("    [Stage 5: Secure] CVE Audit...")
        page.evaluate("window.advanceStage(5)")
        smooth_move(page, 880, 275, steps=25)
        time.sleep(8.0)

        # -------------------------------------------------------------
        # PART 3 (1:12 - 1:52): Stages 6 & 7: Carbon-Aware Google Cloud Run
        # -------------------------------------------------------------
        print("[>] Part 3: Carbon-Aware Canary to Google Cloud Run...")
        # Stage 6: Release (SCI grid query -> europe-north1 93% CFE)
        page.evaluate("window.advanceStage(6)")
        smooth_move(page, 1080, 275, steps=25) # Stage 6 box
        time.sleep(6.5)

        # Move to Regional Carbon Intensity & Carbon Saved metric cards
        smooth_move(page, 1200, 130, steps=25) # Metric 3: Regional Carbon Intensity (28.4 gCO2/kWh)
        time.sleep(8.0)
        smooth_move(page, 1680, 130, steps=25) # Metric 4: Carbon Cut (79.7%)
        time.sleep(9.5)

        # Stage 7: Configure (Scale-to-zero tuning)
        print("    [Stage 7: Configure] Concurrency auto-tuning...")
        page.evaluate("window.advanceStage(7)")
        smooth_move(page, 1280, 275, steps=25) # Stage 7 box
        time.sleep(7.5)
        smooth_move(page, 500, 680, steps=20)  # Terminal log view
        time.sleep(8.5)

        # -------------------------------------------------------------
        # PART 4 (1:52 - 2:30): Stages 8 & 9: Telemetry & Cryptographic Governance
        # -------------------------------------------------------------
        print("[>] Part 4: Cloud Monitoring Telemetry & Governance...")
        # Stage 8: Monitor (P99 39ms, promote traffic)
        page.evaluate("window.advanceStage(8)")
        smooth_move(page, 1480, 275, steps=25) # Stage 8 box
        time.sleep(7.5)
        smooth_move(page, 1500, 715, steps=25) # Audit card: Live Service URL
        time.sleep(9.0)

        # Stage 9: Govern (SLSA Level 3, Cosign provenance, auto-close issue)
        print("    [Stage 9: Govern] Cryptographic Provenance...")
        page.evaluate("window.advanceStage(9)")
        smooth_move(page, 1680, 275, steps=25) # Stage 9 box
        time.sleep(6.5)
        smooth_move(page, 1500, 670, steps=25) # Audit card: Cosign Provenance VERIFIED_VALID
        time.sleep(12.0)

        # -------------------------------------------------------------
        # PART 5 (2:30 - 2:54): Conclusion & Call to Action
        # -------------------------------------------------------------
        print("[>] Part 5: Conclusion & Full Completed Overview...")
        # Glide cursor smoothly over the full completed 9 stages
        smooth_move(page, 960, 275, steps=30)
        time.sleep(8.0)
        # Settle on brand header
        smooth_move(page, 960, 45, steps=30)
        time.sleep(16.0)

        # Close page to flush video
        page.close()
        video_path = page.video.path()
        context.close()
        browser.close()

    print(f"\n[+] Raw browser video saved: {video_path}")

    # Multiplex with Voiceover
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    audio_path = os.path.join(output_dir, "voiceover.mp3")
    final_output = os.path.join(output_dir, "NeuroOps_Duo_Official_Demo.mp4")

    trim_str = f"{trim_offset:.3f}"
    print(f"[*] Trimming initial {trim_str}s browser startup and multiplexing audio...")

    cmd = [
        ffmpeg,
        "-y",
        "-ss", trim_str,
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        "-shortest",
        final_output
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
        print(f"\n[SUCCESS] Master Demo Video Created: {final_output} ({file_size_mb:.2f} MB)")
    else:
        print("[!] Multiplexing failed:", res.stderr)

if __name__ == "__main__":
    record()
