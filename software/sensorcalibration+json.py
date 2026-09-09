# SEGMENT 2: SENSOR CALIBRATION & JSON PACKET HANDLER
ADC_AIR_DRY = 1880.0
ADC_WATER_WET = 1200.0

def calibrate_moisture_adc(raw_adc):
    """Maps raw analog sensor ADC reading (1880 dry, 1200 wet) to [0.0, 1.0]."""
    moisture = (ADC_AIR_DRY - float(raw_adc)) / (ADC_AIR_DRY - ADC_WATER_WET)
    return float(np.clip(moisture, 0.0, 1.0))

def parse_sensor_packet(packet):
    if isinstance(packet, str):
        packet = json.loads(packet)
    
    if "raw_moisture" in packet:
        calibrated_moisture = calibrate_moisture_adc(packet["raw_moisture"])
    elif "raw_adc" in packet:
        calibrated_moisture = calibrate_moisture_adc(packet["raw_adc"])
    else:
        calibrated_moisture = float(packet.get("moisture", 0.35))

    return {
        "sensor_id": packet.get("sensor_id", "Unknown_Sensor"),
        "zone_id": packet.get("zone_id", "Valve_A"),
        "moisture_norm": calibrated_moisture,
        "raw_adc": packet.get("raw_moisture", packet.get("raw_adc", 1500)),
        "temp_c": float(packet.get("temperature_c", packet.get("temp_c", 25.0))),
        "coords": packet.get("coordinates", {"grid_x": 50, "grid_y": 50}),
        "timestamp": packet.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ"))
    }
