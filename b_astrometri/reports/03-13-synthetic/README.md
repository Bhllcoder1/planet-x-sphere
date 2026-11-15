# 03-13 synthetic phase-bias evidence

These artifacts are a synthetic prototype only. The run used `test_epsf.fixture(detector=2)` with `norm=1`, 20 phases from 0 through 0.95 px in 0.05 px steps, 200 trials per phase/SNR, noise sigma 1, and seed 2026.

- `phase_bias.csv`: 60 phase/SNR rows with x/y bias, RMS, predicted sigma, and RMS/sigma.
- `bias_vs_phase.png`: x/y mean bias curves for SNR 20, 50, and 100.
- `rms_sigma_histogram.png`: x/y RMS/predicted-sigma counts for SNR 50 and 100, with the 0.8–1.25 interval marked.
- `summary.json`: run parameters, synthetic qualification, and summarized measurements.

For SNR 50, the maximum absolute x/y bias was 0.00435/0.00280 px and RMS/sigma ranged 0.895–1.100 (descriptive only; the task criterion is strictly SNR > 50). For SNR 100, maximum absolute x/y bias was 0.00287/0.00201 px and RMS/sigma ranged 0.924–1.136; the numerical criteria pass on this fixture.

This is not the 03-12 production T2 harness, not the 03-03 production fitter integration, and not real FITS validation. Human visual review (“is the curve flat?”) remains pending in [HUMAN_ACTIONS.md](../../../docs/second-brain/HUMAN_ACTIONS.md) as H-07; input paths remain pending as H-06.
