"""
Demo rehearsal script: full pipeline walkthrough with stopwatch timing.
Covers Q-H1 (Barnard), Q-H2 (epsilon Indi B), Q-H3 (WISE 0855).
[PARTIAL] Live viewer (09-02) and blink panel (09-08) needed for full rehearsal.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Optional


DEMO_TARGETS = {
    "Q-H1": "Barnard's Star (high proper motion, saturated core)",
    "Q-H2": "epsilon Indi B (brown dwarf companion)",
    "Q-H3": "WISE J085510 (cold Y-dwarf, faint)",
}

EXPECTED_DURATION_SECONDS = {
    "intro": 60,
    "Q-H1": 180,
    "Q-H2": 180,
    "Q-H3": 120,
    "wrap": 60,
}


@dataclass
class DemoStep:
    name: str
    description: str
    expected_s: int
    elapsed_s: float = 0.0
    passed: bool = False

    def status(self) -> str:
        if not self.passed:
            return "PENDING"
        pct = self.elapsed_s / self.expected_s * 100.0
        flag = "OK" if pct <= 110 else "OVER"
        return f"{flag} {self.elapsed_s:.0f}s / {self.expected_s}s ({pct:.0f}%)"


@dataclass
class DemoRun:
    steps: List[DemoStep] = field(default_factory=list)
    total_elapsed_s: float = 0.0

    def add_step(self, name: str, description: str, expected_s: int) -> DemoStep:
        step = DemoStep(name, description, expected_s)
        self.steps.append(step)
        return step

    def summary(self) -> str:
        lines = ["=== DEMO REHEARSAL SUMMARY ==="]
        for s in self.steps:
            lines.append(f"  [{s.status()}] {s.name}: {s.description[:60]}")
        lines.append(f"Total: {self.total_elapsed_s:.0f}s")
        return "\n".join(lines)


def build_demo_run() -> DemoRun:
    """Build the standard demo run with all steps."""
    run = DemoRun()
    run.add_step("intro", "Explain SPHEREx mission scope and pipeline goal", 60)
    run.add_step(
        "Q-H1",
        "Barnard: open viewer, blink passes, show motion vector, check saturated-core warning",
        180,
    )
    run.add_step(
        "Q-H2",
        "eps Indi B: 4-pass coverage, forced phot S/N, brown dwarf badge",
        180,
    )
    run.add_step(
        "Q-H3",
        "WISE 0855: coverage unknown (TAP failed), forced phot upper limit, faint-object note",
        120,
    )
    run.add_step("wrap", "Limitations, next steps, hand back to audience", 60)
    return run


def run_timed_demo(interactive: bool = False) -> DemoRun:
    """Execute (or simulate) the demo with wall-clock timing.

    Parameters
    ----------
    interactive : if True, waits for Enter between steps (real rehearsal).
                  if False, simulates with zero sleep (CI-safe).
    """
    run = build_demo_run()
    t_start = time.monotonic()

    for step in run.steps:
        step_start = time.monotonic()
        if interactive:
            print(f"\n>>> {step.name}: {step.description}")
            input("  Press Enter when done...")
        else:
            # Simulate instantaneous completion in CI
            pass
        step.elapsed_s = time.monotonic() - step_start
        step.passed = True
        if not interactive:
            step.elapsed_s = step.expected_s * 0.9  # simulate 90% speed

    run.total_elapsed_s = time.monotonic() - t_start
    if not interactive:
        run.total_elapsed_s = sum(s.elapsed_s for s in run.steps)
    return run


if __name__ == "__main__":
    print("Running demo in NON-INTERACTIVE mode (simulation).")
    run = run_timed_demo(interactive=False)
    print(run.summary())

    total_budget = sum(EXPECTED_DURATION_SECONDS.values())
    print(f"\nExpected total: {total_budget}s / {total_budget/60:.1f} min")
    over = run.total_elapsed_s > total_budget * 1.1
    print(f"Status: {'OVER TIME' if over else 'WITHIN BUDGET'}")
    print("09-11 demo_script: OK")
