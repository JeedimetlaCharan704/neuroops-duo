# NeuroOps Duo: 3-Minute Hackathon Demo Video Script

**Target Duration:** 2 minutes 45 seconds (Strictly under the 3:00 limit)  
**Tone:** High-energy, crisp, authoritative, engineering-focused.  
**Tools to Display:** 
1. The NeuroOps Visual Dashboard (`http://localhost:8000`)
2. The GitLab Duo Agent files (`.gitlab/duo/`)
3. The Terminal running `python run_autonomous_lifecycle.py`
4. The live Google Cloud Run deployment endpoint

---

## [0:00 - 0:30] Hook & Problem Statement

* **Visual:** Open on the NeuroOps Duo Visual Dashboard (`http://localhost:8000`) with the 9 stages visible.
* **Voiceover:**
  > *"Code generation is solved. But what happens next—triaging production incidents, writing regression tests, verifying mutations, securing containers, routing to green cloud regions, and passing compliance audits—is where engineering teams lose days.*
  >
  > *Welcome to **NeuroOps Duo**: the first 100% hands-off, 9-stage DevSecOps and carbon-adaptive production engine powered by the **GitLab Duo Agent Platform**, Anthropic’s **Model Context Protocol (MCP)**, and **Google Cloud Run**."*

---

## [0:30 - 1:15] Stages 1 to 5: Autonomous Cyber-Reasoning & Verification

* **Visual:** Click the orange button: **"Execute 9-Stage Autonomous Loop"**. Show the terminal and stages 1 through 5 lighting up green in real-time.
* **Voiceover:**
  > *"Watch closely. A critical transaction anomaly is detected in our OmniPay Gateway. Zero humans are involved.
  >
  > First, **Stage 1: Plan**—our Duo Triage Agent ingests the crash dump and maps the AST blast-radius.
  > 
  > Next, **Stage 2: Create**—rather than guessing a fix, our Adversarial Tester Agent writes a reproduction test that demonstrably fails against the bug. This is Cyber Reasoning at work.
  > 
  > In **Stage 3: Verify**, our Remediation Agent generates the minimal AST patch and proves a 100% mutation test score.
  > 
  > In **Stages 4 and 5: Package and Secure**, GitLab CI builds a hardened distroless container, signs it with Cosign, and validates zero critical CVEs."*

---

## [1:15 - 1:55] Stages 6 & 7: Carbon-Aware Google Cloud Run Deployment

* **Visual:** Zoom into Stage 6 (Release) and Stage 7 (Configure). Highlight the SCI metric card on the dashboard showing `28.4 gCO2/kWh` and `79.7% Carbon Saved`.
* **Voiceover:**
  > *"Now for the game-changer: **Stage 6: Release**.
  >
  > Using the Green Software Foundation's ISO/IEC 21031 SCI formula, our Carbon Arbiter Agent queries regional grid data via MCP. Instead of deploying to a fossil-heavy zone, it dynamically deploys a Canary to **Google Cloud Run** in `europe-north1` (Hamina, Finland), which runs on **93% Carbon-Free Energy**.
  > 
  > This slashes lifecycle emissions by **79.7%**.
  > 
  > In **Stage 7: Configure**, the agent auto-tunes Cloud Run concurrency and activates scale-to-zero to eliminate idle carbon waste."*

---

## [1:55 - 2:30] Stages 8 & 9: Telemetry & Cryptographic Governance

* **Visual:** Show Stage 8 (Monitor) and Stage 9 (Govern). Show the live URL `https://omnipay-gateway-omnipay-7x8a9b-europe-north1.a.run.app` in a browser tab.
* **Voiceover:**
  > *"In **Stage 8: Monitor**, our SRE Telemetry Agent polls Google Cloud Monitoring. Error rate is 0.00%, and P99 latency is 39 milliseconds. Satisfying our strict SLOs, it automatically promotes canary traffic to 100%.
  >
  > Finally, in **Stage 9: Govern**, the Compliance Auditor compiles an end-to-end cryptographic audit trail: SLSA Level 3 provenance, signed SBOM, and the official SCI scorecard, closing the incident issue automatically on GitLab."*

---

## [2:30 - 2:45] Conclusion & Call to Action

* **Visual:** Return to the full Dashboard with all 9 stages marked completed and the metrics summary.
* **Voiceover:**
  > *"All 9 DevSecOps stages covered. 100% hands-off autonomy. Deployed on Google Cloud with quantified carbon reduction.
  >
  > This is **NeuroOps Duo**. This is **Life After Code**."*

---

### Recording Tips for Maximum Presentation Points:
1. Start your local dashboard with: `python dashboard_server.py`.
2. Open Chrome in full screen at `http://localhost:8000`.
3. Use OBS Studio or Loom to record at 1080p 60fps.
4. Keep background music off (hackathon rules state: *no copyrighted music*).
5. Ensure your speech is clear and matches the visual transitions.
