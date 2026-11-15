# 03-06 - Existing synthetic coverage run results

The pre-existing coverage process completed; no new run was started after the user requested skipping new tests.

- Attempted trials: 1000;20 synthetic frames per trial.
- Successful single-frame/joint-fit pairs: 999; failed pairs: 1.
- Pairs inside the two-dimensional Mahalanobis-squared<=1 ellipse: 400/999 (40.040040%).
- Nominal two-dimensional Gaussian coverage: 39.346934%. This is a descriptive comparison, not an invented pass tolerance.
- Median single-frame/joint-fit formal sigma ratios (east,north): [5.55544870938413, 5.579086020195854].
- Elapsed time: 1436.063 seconds.

The denominator includes only successful PAIRS. Trial584 had an unmeasurable single-frame baseline while its joint fit was successful; that joint-only result was excluded by the runner. Therefore these figures do not establish complete coverage of all1000 joint solutions. No rerun was performed.

Synthetic source model and EPSF are shared between generation and fitting. No real Barnard pass, corrected production WCS or physical uncertainty calibration is validated by this experiment.03-06 real-data acceptance remains open.

External evidence: C:/Users/behlu/reports/03-06-coverage.json
SHA256: 95f71288ed09698d4ef1bc9fb6912faaccc068851f22a2881b0fc585f7b64776
Runner: b_astrometri/centroid/joint_coverage.py
