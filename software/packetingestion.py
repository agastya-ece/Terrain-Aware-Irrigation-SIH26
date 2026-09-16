# SEGMENT 6: LIVE EXECUTION & REAL PACKET INGESTION INTERFACE
def process_live_packets(sensor_packets_json, current_hour=13.0):
    parsed = [parse_sensor_packet(pkt) for pkt in sensor_packets_json]
    weather = fetch_weather_rain_forecast()
    interp = interpolate_terrace_moisture(tif_meta, parsed)
    results = compute_zone_irrigation_scores(interp, parsed, weather, current_hour=current_hour)
    return {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "weather": weather, "zones": results, "interp": interp}

# Example live telemetry packets coming from physical nodes
incoming_live_packets = [
    {
        "sensor_id": "Ridge_Crest_Node",
        "zone_id": "Valve_A",
        "raw_moisture": 1690,  # ADC: 1690 -> ~28% (Dry upper ridge)
        "temperature_c": 26.8,
        "coordinates": {"grid_x": 90, "grid_y": 210}
    },
    {
        "sensor_id": "Mid_Slope_Node",
        "zone_id": "Valve_B",
        "raw_moisture": 1580,  # ADC: 1580 -> ~44% (Mid bench)
        "temperature_c": 25.4,
        "coordinates": {"grid_x": 180, "grid_y": 126}
    },
    {
        "sensor_id": "Valley_Basin_Node",
        "zone_id": "Valve_C",
        "raw_moisture": 1440,  # ADC: 1440 -> ~65% (Moist valley floor)
        "temperature_c": 23.9,
        "coordinates": {"grid_x": 270, "grid_y": 42}
    }
]

output = process_live_packets(incoming_live_packets, current_hour=13.0)

print(f"Weather: {output['weather']['source']} | Rain Probability (Next 8h): {output['weather']['rain_prob_8h']:.0%}\n")
for v_id, z in output["zones"].items():
    print(f"[{v_id}] {z['zone_name']}")
    print(f"  * Irrigation Need Score: {z['irrigation_need_score']:.3f} / 1.000")
    print(f"  * Actuator Command:     {z['actuator_status']}")
    print(f"  * Current Min Moisture: {z['current_min_moisture']:.3f} | 6h ML Forecast: {z['predicted_6h_moisture']:.3f}")
    print(f"  * FAO-56 Ginger ETc:    {z['fao56_etc_mm_hr']:.3f} mm/hr\n")
