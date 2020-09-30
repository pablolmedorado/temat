// https://github.com/imcvampire/vue-truncate-filter/blob/master/vue-truncate.js
export function truncate(text, length, clamp) {
  text = text || "";
  clamp = clamp || "...";
  length = length || 30;

  if (text.length <= length) {
    return text;
  }
  let tcText = text.slice(0, length - clamp.length);

  let last = tcText.length - 1;
  while (last > 0 && tcText[last] !== " " && tcText[last] !== clamp[0]) {
    last -= 1;
  }

  // Fix for case when text dont have any `space`
  last = last || length - clamp.length;
  tcText = tcText.slice(0, last);

  return tcText + clamp;
}
