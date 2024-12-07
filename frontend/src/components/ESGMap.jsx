import React, { useState } from "react";
import ReactMapGL, { Marker } from "react-map-gl";
import "mapbox-gl/dist/mapbox-gl.css";

const ESGMap = () => {
    const [viewport, setViewport] = useState({
        latitude: 37.7749,
        longitude: -122.4194,
        zoom: 3,
        width: "100%",
        height: "400px",
    });

    const markers = [
        { latitude: 37.7749, longitude: -122.4194, risk: "High" },
        { latitude: 40.7128, longitude: -74.0060, risk: "Medium" },
    ];

    return (
        <div>
            <h2>ESG Risk Map</h2>
            <ReactMapGL
                {...viewport}
                mapboxApiAccessToken="YOUR_MAPBOX_ACCESS_TOKEN"
                onViewportChange={(nextViewport) => setViewport(nextViewport)}
            >
                {markers.map((marker, index) => (
                    <Marker key={index} latitude={marker.latitude} longitude={marker.longitude}>
                        <div style={{ color: "red", fontWeight: "bold" }}>{marker.risk}</div>
                    </Marker>
                ))}
            </ReactMapGL>
        </div>
    );
};

export default ESGMap;
