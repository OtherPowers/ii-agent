from otherpowers_governance.intelligence.field_observer import FieldObserver


def main():
    observer = FieldObserver()

    neutral = observer.observe(None)
    assert neutral.tempo == 1.0
    assert neutral.optimization_pressure == 1.0

    silence = observer.observe({
        "posture": "silence",
        "confidence": "moderate",
    })
    assert silence.optimization_pressure < 1.0
    assert silence.silence_affinity > neutral.silence_affinity

    care = observer.observe({
        "posture": "increase_care",
        "confidence": "moderate",
    })
    assert care.expressive_range > neutral.expressive_range

    high_care = observer.observe({
        "posture": "high_care",
        "confidence": "high",
    })
    assert high_care.tempo < care.tempo

    print("OK: field observer smoke test passed")


if __name__ == "__main__":
    main()
