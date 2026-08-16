def recommend_system(
    grid_available,
    grid_reliable,
    backup_required=False,
    battery_required=False
):
    """
    Recommend a suitable solar system type.

    Returns:
        dict: System recommendation and explanation.
    """

    if not grid_available:
        system_type = "OFF-GRID"
        reason = (
            "The utility grid is unavailable. "
            "An independent solar and battery system may be appropriate."
        )

    elif grid_reliable and not backup_required and not battery_required:
        system_type = "ON-GRID"
        reason = (
            "The grid is available and reliable, "
            "and battery backup is not required."
        )

    else:
        system_type = "HYBRID"
        reason = (
            "The grid is available but battery storage "
            "or backup capability is required."
        )

    return {
        "grid_available": bool(grid_available),
        "grid_reliable": bool(grid_reliable),
        "backup_required": bool(backup_required),
        "battery_required": bool(battery_required),
        "recommended_system": system_type,
        "reason": reason
    }
