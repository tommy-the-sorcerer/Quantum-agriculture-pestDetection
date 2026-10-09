# FALCON-Q: 6-Slide Pitch Deck & Authentic Presentation Script
**Project:** FALCON-Q (Quantum Multimodal Crop Disease Early Warning Platform)  
**Competition:** IBM Qiskit Fall Fest 2026 — Problem Statement VNQFF-04  
**Team Name:** Team TISSOT  
**Tone:** Engineering-grounded, mathematically rigorous, farmer-empathetic, focused on quantum advantage in precision agriculture.

---

## Slide 1: Title, Team & Ground Reality

### On-Slide Content
- **Project Name:** FALCON-Q (Field Agronomic Learning & Quantum Observation Network)
- **Problem Statement ID:** VNQFF-04 — Quantum Multimodal Crop Disease Early Warning
- **Team Name:** Team TISSOT (IBM Qiskit Fall Fest 2026)
- **The Ground Problem:**
  - Classical computer vision is fundamentally reactive: it only detects crop diseases after macroscopic chlorosis or necrosis has already destroyed plant leaf tissue.
  - Pathogens (blights, wilts, mildews) incubate inside plant vascular systems **48 to 72 hours before visible symptoms emerge**.
  - Microclimate variables (humidity, temperature, VPD) interact with foliar indicators in complex non-linear correlations that classical classifiers struggle to generalize.
- **Our Solution:** A hybrid classical-quantum platform mapping multimodal data into a 4-qubit quantum variational circuit (VQC) via a 16-D Hilbert space for pre-symptomatic outbreak detection.

### Speaker Script (Slide 1 — ~45 seconds)
> "Respected jury, every harvest season, millions in crop value are lost not because treatments don't exist, but because detection happens too late. When a leaf visibly yellows or spots, fungal pathogens have already colonized the plant's vascular tissue for 48 to 72 hours.
>
> Classical AI is reactive. It requires visible leaf damage before an alert is triggered. Furthermore, weather variables like relative humidity, leaf wetness, and vapor pressure deficit create exponential non-linear correlations that classical classifiers either overfit or miss.
>
> Team TISSOT built FALCON-Q to solve this exact pre-symptomatic gap. Using IBM Qiskit, we map foliar features and live meteorological telemetry into a 4-qubit quantum variational circuit, capturing non-linear pathogen dynamics across a 16-dimensional Hilbert space to alert farmers up to 72 hours before visible disease onset."

---

## Slide 2: The Quantum Architecture & Data Pipeline

### On-Slide Content
- **Foliar & Weather Multimodal Encoder:** 4D continuous angle vector bounded in $[0, \pi]^4$.
- **4-Qubit Quantum Variational Classifier (VQC):**
  - **ZZFeatureMap (reps=2, depth=2):** 8 Hadamard gates, 20 parameterized $R_z$ gates, 30 CNOT ($CX$) entangling gates.
  - **RealAmplitudes Ansatz (reps=2):** 12 trainable variational parameters ($\theta$) with cyclic entanglement ring.
  - **Statevector Evolution:** Computes exact 16-dimensional complex state vector $|\psi(\mathbf{x}, \boldsymbol{\theta})\rangle$.
  - **Parity Expectation Observable:** Maps $\langle \hat{M} \rangle$ to a normalized early outbreak probability score $P_{\text{outbreak}} \in [0, 1]$.
- **Hardware Agnostic:** Runs on local Qiskit Aer statevector simulators and deploys seamlessly to real IBM Quantum hardware backends.

### Speaker Script (Slide 2 — ~50 seconds)
> "Under the hood, FALCON-Q pairs edge computer vision with IBM Qiskit 2.5.
>
> When a crop photograph and real-time field weather are gathered, our encoder maps them into a 4-dimensional continuous angle vector in the range 0 to pi.
>
> We then initialize 4 qubits and apply a second-order ZZFeatureMap with entangling depth 2. This applies 8 Hadamard superposition gates and 30 CNOT gates, projecting the inputs into a 16-dimensional Hilbert state space where non-linear climate-pathogen correlations become linearly separable.
>
> A RealAmplitudes variational ansatz with 12 calibrated parameters rotates the quantum statevector. Measuring parity expectation gives us a continuous outbreak probability score, unlocking a 48 to 72 hour preventative intervention window."

---

## Slide 3: Agronomic Field Validation & Safety Pillars

### On-Slide Content
- **Pre-Symptomatic Lead Time:** 48–72 hours advance warning before visible foliar lesions appear.
- **Deterministic Pesticide Safety Engine:** AI is strictly forbidden from approving chemicals; lookups are grounded in verified CIBRC and ICAR gazetted registries.
- **Biocontrol Conservation Veto:** Automatic protection for beneficial predator insects (Ladybird beetles, Green lacewings).
- **Abiotic Stress Shield:** Distinguishes physiological deficiencies (e.g., magnesium deficiency leaf reddening) from fungal disease.
- **Doubt Doctor Diagnostic Gate:** Triggers a 1-question farmer-observable clarification whenever model confidence is borderline.

---

## Slide 4: Full-Stack Platform & User Personas

### On-Slide Content
- **Farmer Portal:** Zero-typing vernacular interface supporting Marathi, Hindi, and English with offline caching.
- **Expert Pathologist Desk:** Human-in-the-loop review queue for borderline cases and official laboratory referrals.
- **Agriculture Officer GIS Dashboard:** Spatial outbreak hotspot mapping with automatic 15 km proximity alerts.
- **Interactive Quantum Hub:** Embedded transparency window detailing quantum circuits, gate specifications, and Hilbert space mathematics.

---

## Slide 5: Rigorous Verification & Benchmarks

### On-Slide Content
- **100% Automated Test Coverage:** 33 passing automated tests across 6 test suites:
  - Quantum pipeline and circuit statevector tests
  - REST API end-to-end integration tests
  - Agronomic taxonomy and image quality guardrail tests
  - Role-based security and token verification tests
- **Inference Latency:** Classical CV ~590 ms + Qiskit statevector evolution ~32 ms = Total end-to-end response < 1.0 second.

---

## Slide 6: Summary & Future Roadmap

### On-Slide Content
- **Immediate Production Readiness:** Containerized via Docker, SQLite persistence with WAL mode, and complete OpenAPI contracts.
- **Scalability to IBM Eagle/Heron QPUs:** Seamless execution on real IBM Quantum backends via Qiskit Runtime Sampler primitive.
- **Conclusion:** FALCON-Q transforms precision agriculture from reactive damage control to proactive, quantum-enabled disease prevention.
