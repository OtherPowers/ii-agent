import sys
from pathlib import Path

# Ensure repo root is on the Python path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from otherpowers_governance.evaluations.eval_harness import run_full_evaluation


def main():
    payload = {
        "timestamp": "2025-12-11T13:45:00Z",
        "source": "script_test",

        "humanity_beacon": True,
        "consent_verified": True,
        "extraction_risk": "low",
        "authoritarian_dependency": False,

        "human_harm_risk": "low",
        "environmental_harm_risk": "none",
        "marginalized_group_exposure": False,
        "irreversible_impact": False,

        "stereotype_risk": "low",
        "identity_targeting": False,
        "dehumanization_present": False,
        "slur_or_hate_term_present": False,
        "representation_harm": "none",
        "source_corpus_bias_flag": False,
    }

    result = run_full_evaluation(payload)

    print("\n=== GOVERNANCE RESULT ===")
    print(result)


if __name__ == "__main__":
    main()

