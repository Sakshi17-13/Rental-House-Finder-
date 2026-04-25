import { GoogleMap, Marker, useLoadScript } from "@react-google-maps/api";

const MapView = ({ lat, lng }) => {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "YOUR_API_KEY", // replace later
  });

  if (!isLoaded) return <p>Loading map...</p>;

  return (
    <GoogleMap
      center={{ lat, lng }}
      zoom={12}
      mapContainerStyle={{ width: "100%", height: "200px" }}
    >
      <Marker position={{ lat, lng }} />
    </GoogleMap>
  );
};

export default MapView;