const dotenv = require('dotenv');
const google = require('googlemaps');
import { Loader } from "./Loader";

dotenv.config();

const API_KEY = process.env.GOOGLE_MAPS_API_KEY;

let map;

function initMap() {
  const mapElement = document.getElementById("map");
  if (!mapElement) return;

  const mapOptions = {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  };

  map = new google.maps.Map(mapElement, mapOptions);
}

const loader = new Loader({
  apiKey: API_KEY,
  version: "weekly",
});

loader.load().then(() => {
  initMap();
});