from .models import YieldCurve
from .exceptions import YieldCurveError


def rate_at(curve: YieldCurve, term: float) -> float:
    """Return a rate for a term using linear interpolation."""
    if term <= 0:
        raise YieldCurveError("Term must be positive")

    terms = curve.terms
    minimum_term = terms[0]
    maximum_term = terms[-1]

    if term < minimum_term or term > maximum_term:
        raise YieldCurveError(
            f"Term {term} is outside curve range "
            f"[{minimum_term}, {maximum_term}]"
        )

    if term in curve.points:
        return curve.points[term]

    for left_term, right_term in zip(terms, terms[1:]):
        if left_term < term < right_term:
            left_rate = curve.points[left_term]
            right_rate = curve.points[right_term]
            weight = (term - left_term) / (right_term - left_term)
            return left_rate + weight * (right_rate - left_rate)

    raise YieldCurveError("Could not interpolate curve rate")


def rate_with_spread(
    curve: YieldCurve,
    term: float,
    spread: float
) -> float:
    """Return the zero rate increased by a credit spread."""
    return rate_at(curve, term) + spread
