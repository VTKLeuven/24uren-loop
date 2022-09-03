
let oneTimeEvent = function(item, event, handler, timeout) {
  let f = function(e) {
    item.removeEventListener(event, f, true);
    return handler(e);
  }

  setTimeout(() => item.removeEventListener(event, f, true), timeout);
  item.addEventListener(event, f, true);
}

export {oneTimeEvent};
