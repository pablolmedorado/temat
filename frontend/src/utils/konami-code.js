export default function (callback) {
  const code = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
  const length = code.length;
  var pos = 0;
  document.addEventListener(
    "keydown",
    function (event) {
      if (event.keyCode === code[pos]) {
        pos++;
        if (length === pos) {
          callback();
          pos = 0; // ability to start over
        }
      } else {
        pos = 0;
      }
      return false;
    },
    false
  );
}
