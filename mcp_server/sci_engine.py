"""
Green Software Foundation Software Carbon Intensity (SCI) Specification Engine.
Implements ISO/IEC 21031 (Software Carbon Intensity Standard).

SCI Formula:
    SCI = ( (E * I) + M ) / R

Where:
    E = Energy consumed by software system in kWh
    I = Marginal or regional grid carbon intensity in gCO2e/kWh
    M = Embodied emissions of the underlying compute hardware in gCO2e
    R = Functional unit (e.g. per 10,000 transactions or per pipeline run)
"""
from typing import Dict, Any, List

# Regional grid carbon intensities (gCO2e/kWh) based on Google Cloud Carbon Footprint & Electricity Maps data
GOOGLE_CLOUD_REGIONS_CARBON = {
    "europe-north1": {
        "location": "Hamina, Finland",
        "grid_intensity_gco2_kwh": 28.4,
        "carbon_free_energy_percentage": 93.0,
        "tier": "Ultra-Low Carbon (Recommended)"
    },
    "europe-west1": {
        "location": "St. Ghislain, Belgium",
        "grid_intensity_gco2_kwh": 110.0,
        "carbon_free_energy_percentage": 78.0,
        "tier": "Low Carbon"
    },
    "us-central1": {
        "location": "Council Bluffs, Iowa, USA",
        "grid_intensity_gco2_kwh": 380.0,
        "carbon_free_energy_percentage": 64.0,
        "tier": "Moderate Carbon"
    },
    "us-east4": {
        "location": "Ashburn, Virginia, USA",
        "grid_intensity_gco2_kwh": 360.0,
        "carbon_free_energy_percentage": 52.0,
        "tier": "Moderate Carbon"
    },
    "asia-east1": {
        "location": "Changhua County, Taiwan",
        "grid_intensity_gco2_kwh": 510.0,
        "carbon_free_energy_percentage": 22.0,
        "tier": "High Carbon"
    }
}

class SCIEngine:
    """Calculates Software Carbon Intensity and optimizes deployment routing."""

    # Server hardware specs: Standard AMD EPYC server (64 cores, 256GB RAM)
    # Average thermal design power: 280W + RAM 75W = ~355W total (~5.5W per vCPU core)
    WATTS_PER_VCPU = 5.5
    WATTS_PER_GB_RAM = 0.38
    # Embodied carbon of dual-socket server approx 1,200 kg CO2e over 4-year lifespan (126,144,000 seconds)
    EMBODIED_CARBON_PER_VCPU_SECOND = 1200000.0 / (64 * 126144000) # ~0.000148 gCO2e per vCPU-sec

    @classmethod
    def calculate_energy(cls, vcpu_cores: float, memory_gb: float, execution_seconds: float) -> float:
        """Computes total energy in kWh (E)."""
        power_watts = (vcpu_cores * cls.WATTS_PER_VCPU) + (memory_gb * cls.WATTS_PER_GB_RAM)
        energy_kwh = (power_watts * execution_seconds) / 3600.0 / 1000.0
        return energy_kwh

    @classmethod
    def calculate_embodied_carbon(cls, vcpu_cores: float, execution_seconds: float) -> float:
        """Computes embodied carbon in gCO2e (M)."""
        return vcpu_cores * execution_seconds * cls.EMBODIED_CARBON_PER_VCPU_SECOND

    @classmethod
    def compute_sci(
        cls,
        region: str,
        vcpu_cores: float = 1.0,
        memory_gb: float = 0.5,
        execution_seconds: float = 120.0,
        functional_unit_count: int = 1000
    ) -> Dict[str, Any]:
        """
        Calculates SCI score for a given workload and region.
        """
        region_data = GOOGLE_CLOUD_REGIONS_CARBON.get(region, GOOGLE_CLOUD_REGIONS_CARBON["europe-north1"])
        grid_intensity = region_data["grid_intensity_gco2_kwh"]

        energy_kwh = cls.calculate_energy(vcpu_cores, memory_gb, execution_seconds)
        operational_carbon = energy_kwh * grid_intensity  # E * I
        embodied_carbon = cls.calculate_embodied_carbon(vcpu_cores, execution_seconds)  # M
        total_carbon_gco2 = operational_carbon + embodied_carbon

        # SCI = (E * I + M) / R
        sci_score = total_carbon_gco2 / max(1, functional_unit_count)

        return {
            "region": region,
            "region_location": region_data["location"],
            "grid_intensity_gco2_kwh": grid_intensity,
            "carbon_free_energy_percentage": region_data["carbon_free_energy_percentage"],
            "energy_consumed_kwh": round(energy_kwh, 8),
            "operational_carbon_gco2": round(operational_carbon, 6),
            "embodied_carbon_gco2": round(embodied_carbon, 6),
            "total_carbon_gco2": round(total_carbon_gco2, 6),
            "functional_unit": f"per {functional_unit_count} requests",
            "sci_score": round(sci_score, 8),
            "rating": region_data["tier"]
        }

    @classmethod
    def find_optimal_green_region(cls, allowed_regions: List[str] = None) -> Dict[str, Any]:
        """Identifies the lowest carbon Google Cloud region."""
        candidates = allowed_regions or list(GOOGLE_CLOUD_REGIONS_CARBON.keys())
        scored = [
            (region, GOOGLE_CLOUD_REGIONS_CARBON[region]["grid_intensity_gco2_kwh"])
            for region in candidates if region in GOOGLE_CLOUD_REGIONS_CARBON
        ]
        scored.sort(key=lambda x: x[1])
        best_region = scored[0][0]
        worst_region = scored[-1][0]

        best_sci = cls.compute_sci(best_region)
        worst_sci = cls.compute_sci(worst_region)

        carbon_reduction_pct = (
            (worst_sci["total_carbon_gco2"] - best_sci["total_carbon_gco2"]) / worst_sci["total_carbon_gco2"]
        ) * 100.0

        return {
            "optimal_region": best_region,
            "optimal_location": GOOGLE_CLOUD_REGIONS_CARBON[best_region]["location"],
            "grid_intensity_gco2_kwh": GOOGLE_CLOUD_REGIONS_CARBON[best_region]["grid_intensity_gco2_kwh"],
            "carbon_reduction_vs_worst_pct": round(carbon_reduction_pct, 1),
            "details": best_sci
        }
