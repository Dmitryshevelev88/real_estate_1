from typing import Dict, Tuple


def _calculate_weighted_score(source, profile) -> Tuple[float, Dict[str, float]]:
    infrastructure = float(getattr(source, "infrastructure", 0) or 0)
    lighting = float(getattr(source, "lighting", 0) or 0)
    noise = float(getattr(source, "noise", 0) or 0)
    insolation = float(getattr(source, "insolation", 0) or 0)
    development = float(getattr(source, "development", 0) or 0)

    infrastructure_weight = float(getattr(profile, "infrastructure_weight", 0) or 0)
    lighting_weight = float(getattr(profile, "lighting_weight", 0) or 0)
    noise_weight = float(getattr(profile, "noise_weight", 0) or 0)
    insolation_weight = float(getattr(profile, "insolation_weight", 0) or 0)
    development_weight = float(getattr(profile, "development_weight", 0) or 0)

    infra_score = infrastructure * infrastructure_weight
    lighting_score = lighting * lighting_weight
    noise_score = noise * noise_weight
    insolation_score = insolation * insolation_weight
    development_score = development * development_weight

    total = (
        infra_score
        + lighting_score
        + noise_score
        + insolation_score
        + development_score
    )

    details = {
        "infrastructure_score": round(infra_score, 2),
        "lighting_score": round(lighting_score, 2),
        "noise_score": round(noise_score, 2),
        "insolation_score": round(insolation_score, 2),
        "development_score": round(development_score, 2),
    }

    return round(total, 2), details


def calculate_score(assessment, profile) -> Tuple[float, Dict[str, float]]:
    return _calculate_weighted_score(assessment, profile)


def calculate_score_from_analytics(analytics, profile) -> Tuple[float, Dict[str, float]]:
    return _calculate_weighted_score(analytics, profile)