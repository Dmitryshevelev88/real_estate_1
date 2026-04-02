from app.models.assessment import Assessment
from app.models.score_profile import ScoreProfile


ddef calculate_score_from_analytics(analytics, profile) -> tuple[float, dict]:
    infra = analytics.infrastructure * float(profile.infrastructure_weight)
    lighting = analytics.lighting * float(profile.lighting_weight)
    noise = analytics.noise * float(profile.noise_weight)
    insolation = analytics.insolation * float(profile.insolation_weight)
    development = analytics.development * float(profile.development_weight)

    total = infra + lighting + noise + insolation + development

    details = {
        "infrastructure_score": round(infra, 2),
        "lighting_score": round(lighting, 2),
        "noise_score": round(noise, 2),
        "insolation_score": round(insolation, 2),
        "development_score": round(development, 2),
    }

    return round(total, 2), details