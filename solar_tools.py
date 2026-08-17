"""
Solar Industry Chatbot
Solar Tools Interface

Provides calculation tools used by the chatbot.
"""

from solar_calculator import (
    monthly_to_daily_energy,
    calculate_solar_capacity,
    calculate_panel_count,
    calculate_battery_capacity,
    calculate_backup_time,
    calculate_inverter_size,
    recommend_inverter_size,
    recommend_system_type,
    calculate_appliance_load,
)


# ============================================================
# TOOL 1 — SOLAR SIZE
# ============================================================

def solar_size_tool(
    monthly_consumption,
    panel_wattage=550,
    peak_sun_hours=5
):
    """
    Calculate solar capacity and panel requirement.

    monthly_consumption:
        Monthly electricity consumption in kWh.

    panel_wattage:
        Solar panel wattage.

    peak_sun_hours:
        Average peak sun hours per day.
    """

    daily_consumption = monthly_to_daily_energy(
        monthly_consumption
    )

    solar_capacity = calculate_solar_capacity(
        daily_consumption,
        peak_sun_hours=peak_sun_hours
    )

    panel_count = calculate_panel_count(
        solar_capacity,
        panel_wattage
    )

    actual_capacity = (
        panel_count * panel_wattage
    ) / 1000

    return {
        "monthly_consumption_kwh":
            round(monthly_consumption, 2),

        "daily_consumption_kwh":
            round(daily_consumption, 2),

        "peak_sun_hours":
            round(peak_sun_hours, 2),

        "solar_capacity_kw":
            round(solar_capacity, 2),

        "panel_wattage_w":
            panel_wattage,

        "panel_count":
            panel_count,

        "actual_panel_capacity_kw":
            round(actual_capacity, 2)
    }


# ============================================================
# TOOL 2 — BATTERY SIZE
# ============================================================

def battery_size_tool(
    backup_load_kw,
    backup_hours
):
    """Calculate required battery capacity."""

    battery_capacity = calculate_battery_capacity(
        backup_load_kw,
        backup_hours
    )

    return {
        "backup_load_kw":
            round(backup_load_kw, 2),

        "backup_hours":
            round(backup_hours, 2),

        "battery_capacity_kwh":
            round(battery_capacity, 2)
    }


# ============================================================
# TOOL 3 — BACKUP TIME
# ============================================================

def backup_time_tool(
    battery_capacity_kwh,
    load_kw
):
    """Calculate estimated battery backup time."""

    backup_time = calculate_backup_time(
        battery_capacity_kwh,
        load_kw
    )

    return {
        "battery_capacity_kwh":
            round(battery_capacity_kwh, 2),

        "load_kw":
            round(load_kw, 2),

        "backup_hours":
            round(backup_time, 2)
    }


# ============================================================
# TOOL 4 — INVERTER SIZE
# ============================================================

def inverter_size_tool(
    peak_load_kw
):
    """Calculate recommended inverter size."""

    required_size = calculate_inverter_size(
        peak_load_kw
    )

    recommended_size = recommend_inverter_size(
        required_size
    )

    return {
        "peak_load_kw":
            round(peak_load_kw, 2),

        "required_inverter_kw":
            round(required_size, 2),

        "recommended_inverter_kw":
            recommended_size
    }


# ============================================================
# TOOL 5 — SYSTEM TYPE
# ============================================================

def system_type_tool(
    grid_available=True,
    grid_reliable=True,
    backup_required=False,
    battery_required=False
):
    """Recommend ON-GRID, OFF-GRID, or HYBRID."""

    return recommend_system_type(
        grid_available=grid_available,
        grid_reliable=grid_reliable,
        backup_required=backup_required,
        battery_required=battery_required
    )


# ============================================================
# TOOL 6 — APPLIANCE CONSUMPTION
# ============================================================

def appliance_consumption_tool(
    appliances
):
    """Calculate consumption from appliances."""

    return calculate_appliance_load(
        appliances
    )


# ============================================================
# TOOL 7 — AVAILABLE TOOLS
# ============================================================

def available_tools():
    """Return the tools available to the chatbot."""

    return [
        "solar_size_tool",
        "battery_size_tool",
        "backup_time_tool",
        "inverter_size_tool",
        "system_type_tool",
        "appliance_consumption_tool"
    ]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SOLAR TOOLS INTERFACE TEST")
    print("=" * 70)

    # Solar size test
    solar = solar_size_tool(
        monthly_consumption=300,
        panel_wattage=550,
        peak_sun_hours=5
    )

    print("\nSOLAR SIZE TOOL")
    print("-" * 70)
    print(solar)

    # Battery test
    battery = battery_size_tool(
        backup_load_kw=1.5,
        backup_hours=5
    )

    print("\nBATTERY SIZE TOOL")
    print("-" * 70)
    print(battery)

    # Backup test
    backup = backup_time_tool(
        battery_capacity_kwh=10.42,
        load_kw=1.5
    )

    print("\nBACKUP TIME TOOL")
    print("-" * 70)
    print(backup)

    # Inverter test
    inverter = inverter_size_tool(
        peak_load_kw=2.0
    )

    print("\nINVERTER SIZE TOOL")
    print("-" * 70)
    print(inverter)

    # System test
    system = system_type_tool(
        grid_available=True,
        grid_reliable=False,
        backup_required=True,
        battery_required=True
    )

    print("\nSYSTEM TYPE TOOL")
    print("-" * 70)
    print(system)

    # Appliance test
    appliances = [
        {
            "name": "Fan",
            "power": 80,
            "quantity": 4,
            "hours": 8
        },
        {
            "name": "LED Light",
            "power": 12,
            "quantity": 10,
            "hours": 6
        }
    ]

    appliance_result = appliance_consumption_tool(
        appliances
    )

    print("\nAPPLIANCE TOOL")
    print("-" * 70)

    print(
        f"Daily Energy: "
        f"{appliance_result['total_daily_energy_kwh']:.2f} kWh"
    )

    print(
        f"Monthly Energy: "
        f"{appliance_result['estimated_monthly_energy_kwh']:.2f} kWh"
    )

    print(
        f"Peak Load: "
        f"{appliance_result['peak_connected_load_kw']:.2f} kW"
    )

    print("\nAVAILABLE TOOLS")
    print("-" * 70)

    for tool in available_tools():
        print(f"- {tool}")

    print("\n" + "=" * 70)
    print("SOLAR TOOLS TEST COMPLETED")
    print("=" * 70)