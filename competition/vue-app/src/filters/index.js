import Vue from 'vue';

Vue.filter('millisToMinSec', (millis) => {
  let hours = Math.floor(millis / 3600000); hours = hours === -1 ? 0 : hours;
  let minutes = Math.floor((millis % 3600000) / 60000); minutes = minutes === -1 ? 0 : minutes;
  let seconds = Math.floor((millis % 60000) / 1000); seconds = seconds === -1 ? 0 : seconds;
  seconds = seconds.toFixed(0);

  let res = minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
  if (hours)
    res = hours + ":" + (minutes < 10 ? '0' : '') + res;
  return res;
});

Vue.filter('durationString', (duration) => {
  let p = duration.split(':');
  let milli = 0;
  for (let i = 0; i < p.length; ++i) {
    milli *= 60;
    milli += parseFloat(p[i]);
  }
  return Math.trunc(milli * 1000);
});

Vue.filter('fullName', (runner) => {
  if (!runner) return 'Nobody';
  return `${runner.first_name} ${runner.last_name}`;
});

Vue.filter('dateTimeFilter', (dateTime) => {
  if (!dateTime) return null;
  return dateTime.slice(11,19)
});

Vue.filter('durationFilter', (duration) => {
  if (!duration) return null;

  let m = duration.match(/(.*):(.*):(.*)/);
  if (m[1] === '00')
    return duration.slice(3,8);
  else
    return duration.slice(0,8);
});

Vue.filter('nullFilter', (o, value) => {
  return o ? o : value;
});
