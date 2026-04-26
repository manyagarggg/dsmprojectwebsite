# Illegal Sand Mining in India - Interactive Dashboard

This Streamlit web application showcases a comprehensive analysis of illegal sand mining in India, combining spatial analysis, causal inference, and environmental monitoring.

## Features

### 🗺️ Interactive Map View
- **Map Types**: Political, physical, or combined views of India
- **Resolution Filters**: State, district, latitude/longitude, and river data layers
- **Mining Data Sources**: Toggle between court documents, mining observations, and news reports
- **Clustering Analysis**: Optional spatial clustering (if performance allows)

### 📊 Visual Results Gallery
Comprehensive gallery of all project visualizations with detailed interpretations:
- Correlation heatmaps
- Spatial distribution maps
- Time series analysis
- Causal inference plots
- Environmental impact visualizations

### 📋 Complete Results & Findings
- Executive summary of key findings
- Detailed methodological explanations
- Policy implications and recommendations
- Links to GitHub repository

## Data Sources

- **IndiaSandWatch**: Mining observations, court documents, news reports
- **PMAY Construction Data**: Pradhan Mantri Awas Yojana housing allocations
- **Economic Indicators**: Literacy rates, poverty levels, urbanization
- **Environmental Sensors**: Ganga and Sangam river water quality data
- **Crime Statistics**: City-level crime data across India

## Key Findings

1. **Causal Impact**: PMAY housing scheme caused 14.7× increase in illegal mining
2. **Spatial Decoupling**: Mining occurs in supply states, not construction demand states
3. **Environmental Damage**: Mining correlates with river quality degradation
4. **Economic Drivers**: Construction demand outweighs poverty/literacy factors

## Installation & Running

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Technologies Used

- **Streamlit**: Web application framework
- **Folium**: Interactive mapping
- **Pandas/Geopandas**: Data manipulation and spatial analysis
- **Matplotlib/Seaborn**: Data visualization

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── data/                  # Raw data files
├── outputs/               # Generated visualizations
├── spatial_figures/       # Spatial analysis plots
├── sangam_ganga_figures/  # Environmental analysis plots
└── README.md             # This file
```

## Contact

For questions about the analysis or methodology, please refer to the original research notebooks in the GitHub repository.