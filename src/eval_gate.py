"""Quality gates used by the CI/CD evaluation job."""

MIN_ACCURACY = 0.70


class QualityGateError(RuntimeError):
    """Raised when a candidate model must not be promoted to production."""


def validate_candidate(
    new_accuracy: float,
    production_accuracy: float | None = None,
    threshold: float = MIN_ACCURACY,
) -> None:
    """Reject candidates below the minimum quality or current production score."""
    new_accuracy = float(new_accuracy)
    threshold = float(threshold)

    if not 0.0 <= new_accuracy <= 1.0:
        raise QualityGateError(
            f"Candidate accuracy {new_accuracy:.4f} is outside the valid [0, 1] range."
        )

    if new_accuracy < threshold:
        raise QualityGateError(
            f"Candidate accuracy {new_accuracy:.4f} is below the {threshold:.2f} threshold."
        )

    if production_accuracy is None:
        return

    production_accuracy = float(production_accuracy)
    if not 0.0 <= production_accuracy <= 1.0:
        raise QualityGateError(
            f"Production accuracy {production_accuracy:.4f} is outside the valid [0, 1] range."
        )

    if new_accuracy < production_accuracy:
        raise QualityGateError(
            f"Candidate accuracy {new_accuracy:.4f} is lower than production "
            f"accuracy {production_accuracy:.4f}."
        )
