// https://markus.oberlehner.net/blog/using-the-google-maps-api-with-vue/

const fetchApiKey = async () => {
  await fetch('/api/request_map_api_key/')
    .then(response => response.json())
    .then((data) => {
      API_KEY = data.key;
      VENDOR = data.vendor;
    })
    .catch((err) => {
      console.error(err);
    });
};

let API_KEY = '';
let VENDOR = '';
const CALLBACK_NAME = 'mapsCallback';

fetchApiKey();

let initialized = !!window[VENDOR];
let resolveInitPromise;
let rejectInitPromise;
// This promise handles the initialization
// status of the google maps script.
const initPromise = new Promise((resolve, reject) => {
  resolveInitPromise = resolve;
  rejectInitPromise = reject;
});

export default function init() {
  // If Google Maps already is initialized
  // the `initPromise` should get resolved
  // eventually.
  if (initialized) return initPromise;

  initialized = true;
  // The callback function is called by
  // the Google Maps script if it is
  // successfully loaded.
  window[CALLBACK_NAME] = () => resolveInitPromise(window[VENDOR]);

  // We inject a new script tag into
  // the `<head>` of our HTML to load
  // the Google Maps script.
  const script = document.createElement('script');
  script.async = true;
  script.defer = true;
  script.onerror = rejectInitPromise;
  if (VENDOR === 'google') {
    script.src = `https://maps.googleapis.com/maps/api/js?key=${API_KEY}&callback=${CALLBACK_NAME}`;
  } else {
    script.src = `https://api-maps.yandex.ru/2.1/?apikey=${API_KEY}&lang=en_US&onload=${CALLBACK_NAME}`;
  }
  document.querySelector('head').appendChild(script);

  return initPromise;
}