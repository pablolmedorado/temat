export function hex2rgba(hex, alpha = 1) {
  const [r, g, b] = hex.match(/\w\w/g).map((x) => parseInt(x, 16));
  return `rgba(${r},${g},${b},${alpha})`;
}

export function hex2hsp(hex) {
  const [r, g, b] = hex.match(/\w\w/g).map((x) => parseInt(x, 16));
  return Math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b));
}

export function applyDarkVariant(hex) {
  const hsp = hex2hsp(hex);
  return hsp < 170; // Default threshold: 127.5
}

export function getFontColourFromBackground(hex, alpha = 1) {
  return applyDarkVariant(hex) ? `rgba(255, 255, 255, 1)` : `rgba(0, 0, 0, ${alpha})`;
}
