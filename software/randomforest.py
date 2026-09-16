# SEGMENT 4: RANDOM FOREST 6-8 HOUR MOISTURE DECAY PREDICTOR
def train_rf_moisture_decay_model():
    np.random.seed(42)
    n_samples = 1500

    init_moisture = np.random.uniform(0.10, 0.85, n_samples)
    etc_vals = np.random.uniform(0.05, 0.60, n_samples)
    topo_idx = np.random.uniform(0.0, 1.0, n_samples)
    temps = np.random.uniform(15.0, 32.0, n_samples)
    forecast_hours = np.random.uniform(6.0, 8.0, n_samples)

    drainage_rate = 0.012 * (1.0 + 0.5 * topo_idx)
    evap_loss = (etc_vals * 0.035) * (temps / 25.0)
    decay_total = (drainage_rate + evap_loss) * forecast_hours
    noise = np.random.normal(0.0, 0.008, n_samples)

    future_moisture = np.clip(init_moisture - decay_total + noise, 0.04, 0.90)
    X = np.column_stack([init_moisture, etc_vals, topo_idx, temps, forecast_hours])
    y = future_moisture

    rf = RandomForestRegressor(n_estimators=50, max_depth=8, random_state=42)
    rf.fit(X, y)
    return rf

ML_MODEL = train_rf_moisture_decay_model()
print("Random Forest 6-8h Decay Predictor Trained Successfully.")
