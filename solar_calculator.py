"""
SOLAR INDUSTRY CHATBOT
STEP 8 - COMPLETE SOLAR CALCULATION ENGINE

Features:
1. Monthly energy consumption
2. Appliance load calculation
3. Peak connected load
4. Solar system sizing
5. Solar panel count
6. System type recommendation
7. Battery sizing
8. Battery backup time
9. Inverter sizing
10. Complete solar recommendation
"""

import math


# ============================================================
# 1. ENERGY CONSUMPTION
# ============================================================

def monthly_to_daily_energy(monthly_units):
    """Convert monthly electricity consumption to daily kWh."""

    if monthly_units <= 0:
        raise ValueError(
            "Monthly consumption must be greater than 0."
        )

    return monthly_units / 30


def appliance_energy(power_watts, quantity, hours_per_day):
    """Calculate daily energy consumption of an appliance."""

    if power_watts <= 0:
        raise ValueError("Power must be greater than 0.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")

    if hours_per_day < 0:
        raise ValueError(
            "Operating hours cannot be negative."
        )

    return power_watts * quantity * hours_per_day


def calculate_appliance_load(appliances):
    """
    Calculate:
    - Individual appliance consumption
    - Total daily energy
    - Monthly energy
    - Peak connected load
    """

    results = []

    total_daily_wh = 0
    total_peak_load_w = 0

    for appliance in appliances:

        name = appliance["name"]
        power = appliance["power"]
        quantity = appliance["quantity"]
        hours = appliance["hours"]

        energy_wh = appliance_energy(
            power,
            quantity,
            hours
        )

        connected_load_w = power * quantity

        results.append({
            "name": name,
            "power_w": power,
            "quantity": quantity,
            "hours_per_day": hours,
            "daily_energy_wh": energy_wh,
            "daily_energy_kwh": energy_wh / 1000,
            "connected_load_w": connected_load_w
        })

        total_daily_wh += energy_wh
        total_peak_load_w += connected_load_w

    return {
        "appliances": results,

        "total_daily_energy_kwh":
            total_daily_wh / 1000,

        "estimated_monthly_energy_kwh":
            (total_daily_wh * 30) / 1000,

        "peak_connected_load_kw":
            total_peak_load_w / 1000
    }


# ============================================================
# 2. SOLAR SYSTEM SIZING
# ============================================================

def calculate_solar_capacity(
    daily_energy_kwh,
    peak_sun_hours=5,
    system_efficiency=0.80
):
    """
    Estimate required solar capacity.

    Formula:

    Solar Capacity =
    Daily Energy /
    (Peak Sun Hours × System Efficiency)
    """

    if daily_energy_kwh <= 0:
        raise ValueError(
            "Daily energy must be greater than 0."
        )

    if peak_sun_hours <= 0:
        raise ValueError(
            "Peak sun hours must be greater than 0."
        )

    if not 0 < system_efficiency <= 1:
        raise ValueError(
            "System efficiency must be between 0 and 1."
        )

    return daily_energy_kwh / (
        peak_sun_hours * system_efficiency
    )


def calculate_panel_count(
    solar_capacity_kw,
    panel_wattage
):
    """Calculate required panel count."""

    if solar_capacity_kw <= 0:
        raise ValueError(
            "Solar capacity must be greater than 0."
        )

    if panel_wattage <= 0:
        raise ValueError(
            "Panel wattage must be greater than 0."
        )

    panel_capacity_kw = panel_wattage / 1000

    return math.ceil(
        solar_capacity_kw / panel_capacity_kw
    )


# ============================================================
# 3. BATTERY SIZING
# ============================================================

def calculate_battery_capacity(
    backup_load_kw,
    backup_hours,
    depth_of_discharge=0.80,
    system_efficiency=0.90
):
    """
    Estimate required battery capacity.

    Formula:

    Battery =
    (Load × Backup Time)
    /
    (DoD × Efficiency)
    """

    if backup_load_kw <= 0:
        raise ValueError(
            "Backup load must be greater than 0."
        )

    if backup_hours <= 0:
        raise ValueError(
            "Backup hours must be greater than 0."
        )

    if not 0 < depth_of_discharge <= 1:
        raise ValueError(
            "Depth of discharge must be between 0 and 1."
        )

    if not 0 < system_efficiency <= 1:
        raise ValueError(
            "Battery efficiency must be between 0 and 1."
        )

    return (
        backup_load_kw * backup_hours
    ) / (
        depth_of_discharge * system_efficiency
    )


def calculate_backup_time(
    battery_capacity_kwh,
    load_kw,
    depth_of_discharge=0.80,
    system_efficiency=0.90
):
    """Estimate battery backup duration."""

    if battery_capacity_kwh <= 0:
        raise ValueError(
            "Battery capacity must be greater than 0."
        )

    if load_kw <= 0:
        raise ValueError(
            "Load must be greater than 0."
        )

    usable_energy = (
        battery_capacity_kwh
        * depth_of_discharge
        * system_efficiency
    )

    return usable_energy / load_kw


# ============================================================
# 4. INVERTER SIZING
# ============================================================

def calculate_inverter_size(
    peak_load_kw,
    safety_margin=1.25
):
    """
    Estimate inverter capacity.

    Formula:

    Inverter Size =
    Peak Load × Safety Margin
    """

    if peak_load_kw <= 0:
        raise ValueError(
            "Peak load must be greater than 0."
        )

    if safety_margin <= 1:
        raise ValueError(
            "Safety margin should be greater than 1."
        )

    required_size = (
        peak_load_kw * safety_margin
    )

    return required_size


def recommend_inverter_size(
    required_inverter_kw
):
    """
    Round inverter requirement to a practical
    standard size for basic recommendation.
    """

    standard_sizes = [
        1,
        1.5,
        2,
        3,
        5,
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
        40,
        50
    ]

    for size in standard_sizes:

        if required_inverter_kw <= size:
            return size

    return math.ceil(required_inverter_kw)


# ============================================================
# 5. SYSTEM TYPE
# ============================================================

def recommend_system_type(
    grid_available=True,
    grid_reliable=True,
    backup_required=False,
    battery_required=False
):
    """Recommend ON-GRID, OFF-GRID, or HYBRID."""

    if not grid_available:

        return {
            "system_type": "OFF-GRID",

            "reason":
                "The utility grid is unavailable. "
                "An independent solar and battery "
                "system may be appropriate."
        }

    if backup_required or battery_required:

        return {
            "system_type": "HYBRID",

            "reason":
                "The grid is available but battery "
                "storage or backup capability is required."
        }

    if not grid_reliable:

        return {
            "system_type": "HYBRID",

            "reason":
                "The grid is available but unreliable. "
                "Battery backup may provide additional flexibility."
        }

    return {
        "system_type": "ON-GRID",

        "reason":
            "The grid is available and reliable, "
            "and battery backup is not required."
    }


# ============================================================
# 6. COMPLETE RECOMMENDATION
# ============================================================

def generate_recommendation(
    monthly_units,
    panel_wattage=550,
    peak_sun_hours=5,
    solar_efficiency=0.80,

    grid_available=True,
    grid_reliable=True,

    backup_required=False,
    battery_required=False,

    backup_load_kw=0,
    backup_hours=0,

    battery_depth_of_discharge=0.80,
    battery_efficiency=0.90,

    peak_load_kw=None
):
    """
    Generate a complete solar recommendation.

    Returns:
    - Daily consumption
    - Solar capacity
    - Panel count
    - Inverter requirement
    - Recommended inverter size
    - System type
    - Battery requirement
    """

    # --------------------------------------------------------
    # ENERGY
    # --------------------------------------------------------

    daily_energy = monthly_to_daily_energy(
        monthly_units
    )

    # --------------------------------------------------------
    # SOLAR
    # --------------------------------------------------------

    solar_capacity = calculate_solar_capacity(
        daily_energy,
        peak_sun_hours,
        solar_efficiency
    )

    panel_count = calculate_panel_count(
        solar_capacity,
        panel_wattage
    )

    actual_panel_capacity = (
        panel_count * panel_wattage
    ) / 1000

    # --------------------------------------------------------
    # SYSTEM
    # --------------------------------------------------------

    system = recommend_system_type(
        grid_available,
        grid_reliable,
        backup_required,
        battery_required
    )

    # --------------------------------------------------------
    # INVERTER
    # --------------------------------------------------------

    if peak_load_kw is None:

        peak_load_kw = solar_capacity

    required_inverter = calculate_inverter_size(
        peak_load_kw
    )

    recommended_inverter = recommend_inverter_size(
        required_inverter
    )

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    battery_capacity = None

    if backup_required or battery_required:

        if backup_load_kw <= 0:

            raise ValueError(
                "Backup load must be provided when "
                "battery backup is required."
            )

        if backup_hours <= 0:

            raise ValueError(
                "Backup hours must be provided when "
                "battery backup is required."
            )

        battery_capacity = calculate_battery_capacity(
            backup_load_kw,
            backup_hours,
            battery_depth_of_discharge,
            battery_efficiency
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "monthly_consumption_kwh":
            round(monthly_units, 2),

        "daily_consumption_kwh":
            round(daily_energy, 2),

        "estimated_solar_capacity_kw":
            round(solar_capacity, 2),

        "panel_wattage_w":
            panel_wattage,

        "estimated_panel_count":
            panel_count,

        "actual_panel_capacity_kw":
            round(actual_panel_capacity, 2),

        "peak_load_kw":
            round(peak_load_kw, 2),

        "required_inverter_kw":
            round(required_inverter, 2),

        "recommended_inverter_kw":
            recommended_inverter,

        "recommended_system":
            system["system_type"],

        "recommendation_reason":
            system["reason"],

        "backup_load_kw":
            backup_load_kw,

        "backup_hours":
            backup_hours,

        "estimated_battery_capacity_kwh":
            (
                round(battery_capacity, 2)
                if battery_capacity is not None
                else None
            )
    }


# ============================================================
# 7. TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 75)
    print("SOLAR INDUSTRY CHATBOT")
    print("STEP 8 - COMPLETE CALCULATION ENGINE TEST")
    print("=" * 75)

    recommendation = generate_recommendation(

        monthly_units=300,

        panel_wattage=550,

        peak_sun_hours=5,

        solar_efficiency=0.80,

        grid_available=True,

        grid_reliable=False,

        backup_required=True,

        battery_required=True,

        backup_load_kw=1.5,

        backup_hours=5,

        battery_depth_of_discharge=0.80,

        battery_efficiency=0.90,

        peak_load_kw=2.0
    )

    print("\nCUSTOMER ENERGY")
    print("-" * 75)

    print(
        f"Monthly Consumption: "
        f"{recommendation['monthly_consumption_kwh']} kWh"
    )

    print(
        f"Daily Consumption: "
        f"{recommendation['daily_consumption_kwh']} kWh"
    )

    print("\nSOLAR SIZING")
    print("-" * 75)

    print(
        f"Estimated Solar Capacity: "
        f"{recommendation['estimated_solar_capacity_kw']} kW"
    )

    print(
        f"Panel Requirement: "
        f"{recommendation['estimated_panel_count']} × "
        f"{recommendation['panel_wattage_w']}W"
    )

    print(
        f"Actual Panel Capacity: "
        f"{recommendation['actual_panel_capacity_kw']} kW"
    )

    print("\nINVERTER SIZING")
    print("-" * 75)

    print(
        f"Peak Load: "
        f"{recommendation['peak_load_kw']} kW"
    )

    print(
        f"Calculated Inverter Requirement: "
        f"{recommendation['required_inverter_kw']} kW"
    )

    print(
        f"Recommended Inverter Size: "
        f"{recommendation['recommended_inverter_kw']} kW"
    )

    print("\nBATTERY SIZING")
    print("-" * 75)

    print(
        f"Backup Load: "
        f"{recommendation['backup_load_kw']} kW"
    )

    print(
        f"Backup Duration: "
        f"{recommendation['backup_hours']} hours"
    )

    print(
        f"Estimated Battery Capacity: "
        f"{recommendation['estimated_battery_capacity_kwh']} kWh"
    )

    print("\nSYSTEM TYPE")
    print("-" * 75)

    print(
        f"Recommended System: "
        f"{recommendation['recommended_system']}"
    )

    print(
        f"Reason: "
        f"{recommendation['recommendation_reason']}"
    )

    print("\n" + "=" * 75)
    print("STEP 8 COMPLETE TEST PASSED")
    print("=" * 75)