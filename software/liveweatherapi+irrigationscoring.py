# SEGMENT 5: LIVE WEATHER API & IRRIGATION SCORING
def fetch_weather_rain_forecast(lat=27.14, lon=88.30):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=precipitation_probability,precipitation&forecast_days=2&timezone=Asia%2FKolkata"
    try:
        resp = requests.get(url, timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            hourly_probs = data.get("hourly", {}).get("precipitation_probability", [])
            next_8h_prob = float(np.mean(hourly_probs[:8])) / 100.0
            return {"status": "online", "rain_prob_8h": float(np.clip(next_8h_prob, 0.0, 1.0)), "source": "Open-Meteo API"}
    except Exception:
        pass
    return {"status": "simulated_offline", "rain_prob_8h": 0.15, "source": "Weather Fallback"}

def compute_zone_irrigation_scores(interpolated_res, parsed_packets, weather_info, current_hour=13.0):
    moist_grid = interpolated_res["moisture_grid"]
    h, w = moist_grid.shape
    rain_prob = weather_info["rain_prob_8h"]

    zones = {
        "Valve_A": {"name": "Upper Ridge Terrace", "rows": slice(int(h * 0.66), h), "sensor": parsed_packets[0]},
        "Valve_B": {"name": "Mid Terrace Bench", "rows": slice(int(h * 0.33), int(h * 0.66)), "sensor": parsed_packets[1]},
        "Valve_C": {"name": "Lower Valley Basin", "rows": slice(0, int(h * 0.33)), "sensor": parsed_packets[2]}
    }

    zone_results = {}
    for z_id, z_data in zones.items():
        z_moist = moist_grid[z_data["rows"], :]
        min_moisture = float(np.min(z_moist))
        temp_c = z_data["sensor"]["temp_c"]

        etc = calculate_fao56_etc(temp_c, hour_of_day=current_hour)
        X_pred = np.array([[min_moisture, etc, 0.65 if z_id=="Valve_A" else (0.45 if z_id=="Valve_B" else 0.20), temp_c, 7.0]])
        pred_6h_moisture = float(ML_MODEL.predict(X_pred)[0])

        deficit_factor = max(0.0, (FIELD_CAPACITY - pred_6h_moisture) / (FIELD_CAPACITY - 0.15))
        rain_discount = max(0.0, 1.0 - (rain_prob * 1.5))
        irrigation_score = float(np.clip(deficit_factor * rain_discount, 0.0, 1.0))

        status = "TRIGGER_IRRIGATION_HIGH" if irrigation_score >= 0.65 else ("MODERATE_IRRIGATION" if irrigation_score >= 0.35 else "STANDBY_OPTIMAL")

        zone_results[z_id] = {
            "zone_name": z_data["name"],
            "irrigation_need_score": round(irrigation_score, 3),
            "actuator_status": status,
            "current_min_moisture": round(min_moisture, 3),
            "predicted_6h_moisture": round(pred_6h_moisture, 3),
            "fao56_etc_mm_hr": round(etc, 3),
            "rain_probability_8h": round(rain_prob, 2)
        }

    return zone_results
