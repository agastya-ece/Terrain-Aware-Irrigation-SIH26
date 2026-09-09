# Terraced Precision Irrigation Pipeline
### Integrating GeoTIFF Topography (`irrigation_index.tif`), Raw ADC Sensor Telemetry, FAO-56 Ginger Agronomy, and Random Forest 6-8h Predictive Scoring

This notebook executes the end-to-end pipeline:
1. **Raw ADC Sensor Calibration**: Converts hardware readings (1880 dry $\to$ 0%, 1200 wet $\to$ 100%) to volumetric moisture $[0.0, 1.0]$.
2. **GeoTIFF Topographic Ingestion**: Ingests South Sikkim index data from `D:\Downloads\irrigation_index.tif`.
3. **3D Spatial Interpolation**: Ingests sparse zone anchor telemetry and interpolates unsensored cells.
4. **FAO-56 Penman-Monteith Evapotranspiration**: Dynamic ginger crop water demand ($K_c = 1.10$).
5. **Random Forest 6-8 Hour Decay Model**: Forecasts moisture depletion under terrain drainage.
6. **Weather API Integration**: Checks 6-8 hour rain probability from Open-Meteo / Meteorological forecasts.
7. **Irrigation Need Score ($0.0 - 1.0$)**: Outputs decision score for each solenoid valve.
