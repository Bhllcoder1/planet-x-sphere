/**
 * Alan D - Görev 11-18 & 11-19: Durum Yöneticisi, 3 Adımlı İlk Kullanım Tanıtımı ve Klavye Kısayolları
 * Kısayollar (SITE_SPEC W23):
 *   Space   -> Oynat / Duraklat (Play / Pause)
 *   Left    -> 1 kare geri
 *   Right   -> 1 kare ileri
 *   [ / ]   -> Blink hızını yavaşlat / hızlandır
 *   g       -> Piksel ızgarasını (Grid) aç / kapat
 *   i       -> Ters çevir (Invert) aç / kapat
 *   f       -> Bayrak (Flag) katmanını aç / kapat
 *   r       -> Döngü başına dön (Restart)
 *   ?       -> Klavye kısayolları yardım penceresini aç / kapat
 */

export const KEYBOARD_SHORTCUTS = [
  { key: "Space", action: "togglePlay", description: "Play / Pause blink time series" },
  { key: "ArrowLeft", action: "stepBackward", description: "Step 1 frame backward" },
  { key: "ArrowRight", action: "stepForward", description: "Step 1 frame forward" },
  { key: "[", action: "slowerBlink", description: "Decrease blink speed (longer frame interval)" },
  { key: "]", action: "fasterBlink", description: "Increase blink speed (shorter frame interval)" },
  { key: "g", action: "toggleGrid", description: "Toggle native pixel grid overlay" },
  { key: "i", action: "toggleInvert", description: "Toggle grayscale inversion" },
  { key: "f", action: "toggleFlags", description: "Toggle BITMASK flag layer" },
  { key: "r", action: "restartBlink", description: "Jump to first frame of current pass/sequence" },
  { key: "?", action: "toggleHelpModal", description: "Open / close keyboard shortcuts & onboarding help" },
];

export const ONBOARDING_STEPS = [
  {
    step: 1,
    id: "select-target",
    title: "1. Pick a Competition Target or Enter Coordinates",
    body: "Select one of the 5 NASA Space Apps test targets (e.g., Barnard's Star) or enter exact ICRS RA/Dec coordinates. Missing archive coverage or busy TAP servers are always reported honestly.",
  },
  {
    step: 2,
    id: "blink-and-inspect",
    title: "2. Blink at Integer Zoom & Compare with Gaia DR3",
    body: "Press Space to blink frames on their native pixel grid (Mode N) or server R-k grid. Each native pixel is drawn z × z screen pixels and float centroids (e.g., 4.47 px) are never rounded.",
  },
  {
    step: 3,
    id: "save-and-export",
    title: "3. Export Provenance-Stamped PNG & Measurement CSV",
    body: "Download the current view as an 8-bit PNG (with badges and grid burned in) or export the float32 measurement table as CSV with full provenance and honesty notes.",
  },
];

export function resolveScreenStateText(uiStrings, screenName, stateKey, params = {}) {
  const screenObj = uiStrings?.screens?.[screenName];
  if (!screenObj || !screenObj[stateKey]) {
    throw new Error(`Unknown screen/state: ${screenName}.${stateKey}`);
  }
  const entry = screenObj[stateKey];
  const fallback = uiStrings?.meta?.unmeasured_fallback || "not measured";
  let msg = entry.message;
  for (const [k, v] of Object.entries(params)) {
    const safeVal = v === undefined || v === null || Number.isNaN(v) ? fallback : String(v);
    msg = msg.replace(`{${k}}`, safeVal);
  }
  return {
    screen: screenName,
    state: stateKey,
    title: entry.title,
    message: msg,
    actionLabel: entry.action_label,
  };
}

export function attachKeyboardShortcuts(handlers, doc = typeof document !== "undefined" ? document : null) {
  if (!doc) return () => {};
  const listener = (event) => {
    const tag = (event.target?.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select") {
      return;
    }
    const key = event.key === " " ? "Space" : event.key;
    const match = KEYBOARD_SHORTCUTS.find((s) => s.key.toLowerCase() === key.toLowerCase());
    if (match && typeof handlers[match.action] === "function") {
      event.preventDefault();
      handlers[match.action](event);
    }
  };
  doc.addEventListener("keydown", listener);
  return () => doc.removeEventListener("keydown", listener);
}
