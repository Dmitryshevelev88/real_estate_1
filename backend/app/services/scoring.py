from typing import Dict, Tuple


def calculate_score_from_analytics(analytics, profile) -> Tuple[float, Dict[str, float]]:
    metrics = {
        "infrastructure": float(getattr(analytics, "infrastructure", 0) or 0),
        "lighting": float(getattr(analytics, "lighting", 0) or 0),
        "noise": float(getattr(analytics, "noise", 0) or 0),
        "insolation": float(getattr(analytics, "insolation", 0) or 0),
        "development": float(getattr(analytics, "development", 0) or 0),
    }

    breakdown: Dict[str, float] = {}
    total_score = 0.0

    for metric_name, metric_value in metrics.items():
        weight = float(getattr(profile, f"{metric_name}_weight", 0) or 0)
        weighted_value = metric_value * weight
        breakdown[metric_name] = round(weighted_value, 2)
        total_score += weighted_value

    return round(total_score, 2), breakdown