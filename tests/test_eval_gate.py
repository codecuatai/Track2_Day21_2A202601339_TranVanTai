import pytest

from src.eval_gate import MIN_ACCURACY, QualityGateError, validate_candidate


def test_rejects_candidate_below_minimum_accuracy():
    with pytest.raises(QualityGateError, match="below the 0.70 threshold"):
        validate_candidate(MIN_ACCURACY - 0.001)


def test_accepts_candidate_at_minimum_accuracy_without_production_model():
    validate_candidate(MIN_ACCURACY)


def test_rejects_candidate_that_regresses_from_production():
    with pytest.raises(QualityGateError, match="lower than production"):
        validate_candidate(0.75, production_accuracy=0.76)


@pytest.mark.parametrize(
    ("new_accuracy", "production_accuracy"),
    [(0.75, 0.75), (0.80, 0.75)],
)
def test_accepts_candidate_equal_to_or_better_than_production(
    new_accuracy,
    production_accuracy,
):
    validate_candidate(new_accuracy, production_accuracy)
