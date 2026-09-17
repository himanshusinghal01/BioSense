import json

class EnvironmentalReasoner:
    def __init__(self):
        pass

    def check_missing_inputs(self, user_data):
        missing = []
        if user_data.get("soil_organic_carbon") is None:
            missing.append("Soil Organic Carbon %")
        if user_data.get("rainfall") is None:
            missing.append("Annual Rainfall / Pattern")
        if user_data.get("land_use") is None:
            missing.append("Land Use / Cropping Type")
        return missing

    def analyze_multi_metric_relationships(self, data):
        insights = []
        soc = data.get("soil_organic_carbon")
        rainfall = data.get("rainfall")
        land_use = str(data.get("land_use", "")).lower()

        if soc is not None and soc < 1.0 and (rainfall == "low" or (isinstance(rainfall, (int, float)) and rainfall < 500)):
            insights.append({
                "variables": ["Soil Organic Carbon", "Rainfall"],
                "finding": "Low organic carbon (<1.0%) combined with low rainfall (<500mm) severely reduces soil water retention and microbial activity."
            })

        if "monoculture" in land_use:
            insights.append({
                "variables": ["Land Use (Monoculture)", "Habitat Diversity"],
                "finding": "Continuous monoculture creates uniform canopy structure, eliminating ecological niches for native pollinators and species richness."
            })

        if len(insights) >= 2:
            insights.append({
                "variables": ["Soil Carbon", "Rainfall", "Monoculture"],
                "finding": "Compounding Risk: Low soil organic carbon + water stress + monoculture land use accelerates land degradation and biodiversity collapse."
            })

        return insights
