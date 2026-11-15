/**
 * Alan D - Görev 05-03, 05-15, 10-05, 11-20: Blink Oynatıcı, Aynı Dedektör Eşleme,
 * Epoch Göstergesi (+ − .) ve Aşamalı Yükleme (Progressive Ready Counter)
 */

export class BlinkController {
  constructor(frames = [], options = {}) {
    this.allFrames = Array.isArray(frames) ? frames : [];
    this.detectorFilter = options.detectorFilter || null;
    this.intervalMs = Number(options.intervalMs || 200);
    this.currentIndex = 0;
    this.isPlaying = false;
    this.droppedFrames = 0;
    this.readyFrameIds = new Set(options.readyFrameIds || this.allFrames.map((f) => f.frame_id));
    this.excludedFrameIds = new Set(options.excludedFrameIds || []);
    this.unusedFrameIds = new Set(options.unusedFrameIds || []);
    this.onChange = typeof options.onChange === "function" ? options.onChange : null;
  }

  getActiveSequence() {
    return this.allFrames.filter((f) => {
      if (this.excludedFrameIds.has(f.frame_id) || this.unusedFrameIds.has(f.frame_id)) {
        return false;
      }
      if (this.detectorFilter && f.detector !== this.detectorFilter) {
        return false;
      }
      return this.readyFrameIds.has(f.frame_id);
    });
  }

  getCurrentFrame() {
    const seq = this.getActiveSequence();
    if (seq.length === 0) return null;
    const safeIdx = ((this.currentIndex % seq.length) + seq.length) % seq.length;
    return seq[safeIdx];
  }

  isAtLoopStart() {
    const seq = this.getActiveSequence();
    return seq.length > 0 && ((this.currentIndex % seq.length) + seq.length) % seq.length === 0;
  }

  stepForward() {
    const seq = this.getActiveSequence();
    if (seq.length === 0) return null;
    this.currentIndex = (this.currentIndex + 1) % seq.length;
    this._emit();
    return this.getCurrentFrame();
  }

  stepBackward() {
    const seq = this.getActiveSequence();
    if (seq.length === 0) return null;
    this.currentIndex = (this.currentIndex - 1 + seq.length) % seq.length;
    this._emit();
    return this.getCurrentFrame();
  }

  restart() {
    this.currentIndex = 0;
    this._emit();
    return this.getCurrentFrame();
  }

  setSpeed(intervalMs) {
    this.intervalMs = Math.max(50, Math.min(2000, Number(intervalMs)));
    this._emit();
  }

  setDetectorFilter(detector) {
    this.detectorFilter = detector || null;
    this.currentIndex = 0;
    this._emit();
  }

  markFrameReady(frameId) {
    this.readyFrameIds.add(frameId);
    this._emit();
  }

  getProgressiveStatus() {
    const total = this.allFrames.length;
    const ready = this.allFrames.filter((f) => this.readyFrameIds.has(f.frame_id)).length;
    return {
      ready,
      total,
      label: `${ready} / ${total} ready`,
      canStartBlink: ready >= 2,
    };
  }

  /**
   * Görev 05-15: Epoch göstergesi (+ dahil, - çıkarılmış, . kullanılmamış)
   * ve döngü başı kenarlığı (isLoopStartBorder).
   */
  getEpochBarItems() {
    const current = this.getCurrentFrame();
    return this.allFrames.map((f, idx) => {
      let symbol = "+";
      let status = "included";
      if (this.excludedFrameIds.has(f.frame_id)) {
        symbol = "-";
        status = "excluded";
      } else if (
        this.unusedFrameIds.has(f.frame_id) ||
        (this.detectorFilter && f.detector !== this.detectorFilter)
      ) {
        symbol = ".";
        status = "unused";
      }
      return {
        index: idx,
        frame_id: f.frame_id,
        pass_id: f.pass_id ?? 0,
        detector: f.detector,
        symbol,
        status,
        isCurrent: current ? current.frame_id === f.frame_id : false,
        isLoopStartBorder: idx === 0,
      };
    });
  }

  getCounterLabel() {
    const seq = this.getActiveSequence();
    if (seq.length === 0) return "0 / 0";
    const safeIdx = ((this.currentIndex % seq.length) + seq.length) % seq.length;
    return `${safeIdx + 1} / ${seq.length}`;
  }

  _emit() {
    if (this.onChange) {
      this.onChange({
        currentFrame: this.getCurrentFrame(),
        counterLabel: this.getCounterLabel(),
        isAtLoopStart: this.isAtLoopStart(),
        progressive: this.getProgressiveStatus(),
      });
    }
  }
}
