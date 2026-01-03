# /Users/bush3000/ii-agent-reorg/otherpowers_governance/intelligence/cold_storage_bridge.py
"""
OtherPowers Cold Storage → Posture Emission Bridge (non-coercive)

Purpose
- Accept long-horizon, privacy-preserving summaries (no identities, no logs).
- Classify ONLY into the constrained pattern vocabulary (taxonomy-constrained).
- Emit zero or more OtherPowers governance signals that are safe to ignore.
- Make uncertainty first-class.
- Allow intentional non-emission ("selective deafness") when emission risks harm.

Non-goals
- No enforcement, no ranking people, no reputation, no topic tracking, no adoption telemetry.
- No durable storage; this bridge is stateless except for caller-provided inputs.

Design stance
- Conservative by default: the bridge prefers silence over unsafe inference.
- Outputs "conditions, not events" (pattern weather), and trends, not counts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
import math
import time


# ---------------------------
# Pattern taxonomy (constrained vocabulary)
# ---------------------------

class PatternFamily(str, Enum):
    PRESSURE = "pressure_patterns"
    ERASURE = "erasure_patterns"
    NORMALIZATION = "normalization_patterns"
    VOLATILITY = "volatility_patterns"
    CAPTURE = "capture_patterns"
    CARE = "care_patterns"


class TrendDirection(str, Enum):
    ACCELERATING = "accelerating"
    STABILIZING = "stabilizing"
    FRAGMENTING = "fragmenting"
    OSCILLATING = "oscillating"
    UNKNOWN = "unknown"


class UncertaintyBand(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class PatternWeather:
    """
    "Conditions, not events": a compact weather-like descriptor that avoids
    enumerating incidents, actors, or topics.
    """
    family: PatternFamily
    label: str  # a taxonomy label, e.g., "pressure: compression", "erasure: silence", etc.
    severity: float  # 0..1 normalized, not a count
    persistence: float  # 0..1: how 'stuck' the condition appears over time
    volatility: float  # 0..1: how fast conditions change
    trend: TrendDirection
    absence_aware: bool  # whether "silence/erasure" is part of the condition


@dataclass(frozen=True)
class CounterfactualCareHint:
    """
    Non-prescriptive, non-coercive "what historically reduced harm" hint.
    This must remain advisory and not claim certainty.
    """
    hint: str
    confidence: float  # 0..1, calibrated pessimistically


@dataclass(frozen=True)
class BridgeDecision:
    """
    Output of classification + emission decision for one bridge run.
    """
    should_emit: bool
    withhold: bool
    withholding_reason: Optional[str]
    uncertainty: UncertaintyBand
    weather: List[PatternWeather] = field(default_factory=list)
    care_hints: List[CounterfactualCareHint] = field(default_factory=list)


# ---------------------------
# Input contract (privacy-preserving summary)
# ---------------------------

@dataclass(frozen=True)
class LongHorizonSummary:
    """
    Minimal, caller-provided long-horizon summary.
    This object MUST NOT contain identities, source IDs, raw quotes, or event logs.

    The bridge only uses these fields (all optional), and treats them as weak signals.
    """
    # Human-meaningful time window of the summary (seconds since epoch or None)
    window_start_ts: Optional[float] = None
    window_end_ts: Optional[float] = None

    # High-level indicators (0..1). These are not counts, and should not be derived from
    # per-person tracking. Think "pressure index", "volatility index", etc.
    pressure_index: Optional[float] = None
    erasure_index: Optional[float] = None
    normalization_index: Optional[float] = None
    volatility_index: Optional[float] = None
    capture_index: Optional[float] = None
    care_index: Optional[float] = None

    # Optional distributional / plurality hints (no topics). Values are 0..1.
    plurality_index: Optional[float] = None  # higher => more plural, less monoculture
    fragility_index: Optional[float] = None  # higher => more brittle, likely to snap
    silence_index: Optional[float] = None    # higher => meaningful absence / suppression

    # Optional freeform metadata that is already de-identified and non-sensitive.
    # The bridge will not emit or store this directly.
    metadata: Mapping[str, Any] = field(default_factory=dict)


# ---------------------------
# Configuration (bridge behavior)
# ---------------------------

@dataclass(frozen=True)
class ColdStorageBridgeConfig:
    """
    Conservative defaults:
    - Emit only when signal is strong enough AND uncertainty is not too high.
    - Withhold when silence/erasure risk is high and summary confidence is weak.
    """
    emit_threshold: float = 0.62
    max_weather_items: int = 4

    # If silence_index is above this and we are not confident, prefer non-emission.
    silence_withhold_threshold: float = 0.70

    # Uncertainty: higher values mean we classify more conservatively.
    uncertainty_bias: float = 0.15  # 0..1

    # Trend smoothing: if window is short, trend becomes UNKNOWN more often.
    min_window_seconds_for_trend: float = 6 * 60 * 60  # 6 hours

    # Safety: cap strengths so bridge can't "shout".
    max_signal_strength: float = 0.85

    # Emit posture recommendation style: advisory only.
    recommended_actions_limit: int = 5


# ---------------------------
# Utilities
# ---------------------------

def _clamp01(x: Optional[float]) -> Optional[float]:
    if x is None:
        return None
    return max(0.0, min(1.0, float(x)))


def _safe_mean(values: Sequence[Optional[float]]) -> Optional[float]:
    xs = [v for v in values if v is not None and not math.isnan(v)]
    if not xs:
        return None
    return sum(xs) / float(len(xs))


def _uncertainty_band(score: float) -> UncertaintyBand:
    # score here means "uncertainty", 0..1
    if score >= 0.72:
        return UncertaintyBand.HIGH
    if score >= 0.42:
        return UncertaintyBand.MEDIUM
    return UncertaintyBand.LOW


def _now_ts() -> float:
    return time.time()


# ---------------------------
# Classifier (taxonomy constrained)
# ---------------------------

class ColdStoragePatternClassifier:
    """
    Rule-based, conservative classifier.

    This is intentionally simple. Later you can swap in a more nuanced model,
    but only if it stays privacy-preserving and taxonomy-constrained.
    """

    def __init__(self, config: ColdStorageBridgeConfig):
        self._cfg = config

    def classify(self, summaries: Sequence[LongHorizonSummary]) -> BridgeDecision:
        if not summaries:
            return BridgeDecision(
                should_emit=False,
                withhold=True,
                withholding_reason="no_long_horizon_summaries",
                uncertainty=UncertaintyBand.HIGH,
                weather=[],
                care_hints=[],
            )

        # Aggregate summary indicators across the provided horizon.
        pressure = _safe_mean([_clamp01(s.pressure_index) for s in summaries])
        erasure = _safe_mean([_clamp01(s.erasure_index) for s in summaries])
        normalization = _safe_mean([_clamp01(s.normalization_index) for s in summaries])
        volatility = _safe_mean([_clamp01(s.volatility_index) for s in summaries])
        capture = _safe_mean([_clamp01(s.capture_index) for s in summaries])
        care = _safe_mean([_clamp01(s.care_index) for s in summaries])

        plurality = _safe_mean([_clamp01(s.plurality_index) for s in summaries])
        fragility = _safe_mean([_clamp01(s.fragility_index) for s in summaries])
        silence = _safe_mean([_clamp01(s.silence_index) for s in summaries])

        # Compute uncertainty pessimistically:
        # - missingness increases uncertainty
        # - high volatility increases uncertainty
        # - low plurality / high fragility increases uncertainty
        missing_fields = 0
        total_fields = 6  # primary indices
        for v in [pressure, erasure, normalization, volatility, capture, care]:
            if v is None:
                missing_fields += 1
        missingness = missing_fields / float(total_fields)

        volatility_term = (volatility or 0.5)
        plurality_term = 1.0 - (plurality if plurality is not None else 0.5)
        fragility_term = (fragility if fragility is not None else 0.5)

        raw_uncertainty = (
            0.50 * missingness +
            0.20 * volatility_term +
            0.15 * plurality_term +
            0.15 * fragility_term
        )
        raw_uncertainty = _clamp01(raw_uncertainty) or 1.0

        # Bias upward (more conservative)
        raw_uncertainty = _clamp01(raw_uncertainty + self._cfg.uncertainty_bias) or 1.0
        ub = _uncertainty_band(raw_uncertainty)

        # Decide withhold conditions:
        # If meaningful silence is high AND we are medium/high uncertainty, prefer withholding.
        if (silence is not None and silence >= self._cfg.silence_withhold_threshold) and ub != UncertaintyBand.LOW:
            return BridgeDecision(
                should_emit=False,
                withhold=True,
                withholding_reason="selective_deafness_due_to_meaningful_silence_and_uncertainty",
                uncertainty=ub,
                weather=[],
                care_hints=self._care_hints(care=care, plurality=plurality, uncertainty=raw_uncertainty),
            )

        weather = self._weather_from_indices(
            pressure=pressure,
            erasure=erasure,
            normalization=normalization,
            volatility=volatility,
            capture=capture,
            care=care,
            plurality=plurality,
            fragility=fragility,
            silence=silence,
            summaries=summaries,
            uncertainty=raw_uncertainty,
        )

        # Determine whether emission is warranted (conservative):
        # Use the strongest non-care "risk" condition as an emission basis,
        # and allow care conditions to emit only when they are strong enough to matter.
        strongest_severity = 0.0
        for w in weather:
            strongest_severity = max(strongest_severity, float(w.severity))

        emit_basis = strongest_severity * (1.0 - raw_uncertainty)
        should_emit = emit_basis >= self._cfg.emit_threshold and len(weather) > 0

        return BridgeDecision(
            should_emit=should_emit,
            withhold=not should_emit,
            withholding_reason=None if should_emit else "insufficient_confident_pattern_weather",
            uncertainty=ub,
            weather=weather[: self._cfg.max_weather_items],
            care_hints=self._care_hints(care=care, plurality=plurality, uncertainty=raw_uncertainty),
        )

    def _care_hints(self, care: Optional[float], plurality: Optional[float], uncertainty: float) -> List[CounterfactualCareHint]:
        hints: List[CounterfactualCareHint] = []
        # These are intentionally generic and advisory.
        # They should never mention groups/topics/people; just posture and restraint suggestions.
        if care is not None and care >= 0.60:
            hints.append(CounterfactualCareHint(
                hint="Historically, slowing escalation and increasing consent checks reduced harm under care-forward conditions.",
                confidence=max(0.15, (care * 0.55) * (1.0 - uncertainty)),
            ))
        if plurality is not None and plurality <= 0.40:
            hints.append(CounterfactualCareHint(
                hint="Historically, inviting multiple epistemologies and explicitly naming uncertainty reduced monoculture drift.",
                confidence=max(0.12, ((1.0 - plurality) * 0.50) * (1.0 - uncertainty)),
            ))
        if uncertainty >= 0.60:
            hints.append(CounterfactualCareHint(
                hint="Historically, when uncertainty was high, choosing silence or soft-posture defaults reduced accidental coercion.",
                confidence=0.20,
            ))
        # Cap list length to keep signals compact.
        return hints[:3]

    def _trend_from_window(self, summaries: Sequence[LongHorizonSummary]) -> TrendDirection:
        # Conservative trend estimation: requires a time window and at least 2 summaries with usable endpoints.
        # We avoid precise slope math: just a direction-of-change heuristic.
        with_ts = [
            s for s in summaries
            if s.window_start_ts is not None and s.window_end_ts is not None
        ]
        if len(with_ts) < 2:
            return TrendDirection.UNKNOWN

        start = min(s.window_start_ts for s in with_ts if s.window_start_ts is not None)
        end = max(s.window_end_ts for s in with_ts if s.window_end_ts is not None)
        if start is None or end is None or (end - start) < self._cfg.min_window_seconds_for_trend:
            return TrendDirection.UNKNOWN

        # Compare early vs late averages of volatility as a proxy for general directional movement.
        # This avoids direct topic scoring.
        midpoint = start + (end - start) / 2.0
        early = [s for s in with_ts if (s.window_end_ts or 0) <= midpoint]
        late = [s for s in with_ts if (s.window_start_ts or 0) > midpoint]
        if not early or not late:
            return TrendDirection.UNKNOWN

        early_vol = _safe_mean([_clamp01(s.volatility_index) for s in early]) or 0.5
        late_vol = _safe_mean([_clamp01(s.volatility_index) for s in late]) or 0.5

        # Heuristic mapping:
        if late_vol - early_vol > 0.12:
            return TrendDirection.ACCELERATING
        if early_vol - late_vol > 0.12:
            return TrendDirection.STABILIZING
        # Fragmenting vs oscillating: use plurality and fragility if present
        early_plu = _safe_mean([_clamp01(s.plurality_index) for s in early])
        late_plu = _safe_mean([_clamp01(s.plurality_index) for s in late])
        if early_plu is not None and late_plu is not None and (late_plu - early_plu) < -0.10:
            return TrendDirection.FRAGMENTING
        return TrendDirection.OSCILLATING

    def _weather_from_indices(
        self,
        pressure: Optional[float],
        erasure: Optional[float],
        normalization: Optional[float],
        volatility: Optional[float],
        capture: Optional[float],
        care: Optional[float],
        plurality: Optional[float],
        fragility: Optional[float],
        silence: Optional[float],
        summaries: Sequence[LongHorizonSummary],
        uncertainty: float,
    ) -> List[PatternWeather]:
        trend = self._trend_from_window(summaries)

        items: List[PatternWeather] = []

        # Helper to create weather items conservatively
        def add_item(
            family: PatternFamily,
            label: str,
            severity: Optional[float],
            persistence_hint: Optional[float],
            volatility_hint: Optional[float],
            absence_aware: bool,
        ) -> None:
            if severity is None:
                return
            sev = float(_clamp01(severity) or 0.0)
            # Down-weight severity by uncertainty so we don't over-signal.
            sev = sev * (1.0 - (0.65 * uncertainty))
            sev = float(_clamp01(sev) or 0.0)

            if sev <= 0.10:
                return

            persistence = float(_clamp01(persistence_hint) or 0.5)
            vol = float(_clamp01(volatility_hint) or 0.5)

            items.append(PatternWeather(
                family=family,
                label=label,
                severity=sev,
                persistence=persistence,
                volatility=vol,
                trend=trend,
                absence_aware=absence_aware,
            ))

        # Pressure patterns
        add_item(
            family=PatternFamily.PRESSURE,
            label="pressure: compression",
            severity=pressure,
            persistence_hint=fragility if fragility is not None else 0.55,
            volatility_hint=volatility if volatility is not None else 0.50,
            absence_aware=False,
        )

        # Erasure patterns (absence-aware)
        add_item(
            family=PatternFamily.ERASURE,
            label="erasure: meaningful_silence",
            severity=max(erasure or 0.0, silence or 0.0) if (erasure is not None or silence is not None) else None,
            persistence_hint=0.65,
            volatility_hint=volatility if volatility is not None else 0.45,
            absence_aware=True,
        )

        # Normalization patterns
        add_item(
            family=PatternFamily.NORMALIZATION,
            label="normalization: drift_to_monoculture",
            severity=normalization,
            persistence_hint=(1.0 - (plurality if plurality is not None else 0.5)),
            volatility_hint=volatility if volatility is not None else 0.40,
            absence_aware=False,
        )

        # Volatility patterns
        add_item(
            family=PatternFamily.VOLATILITY,
            label="volatility: churn",
            severity=volatility,
            persistence_hint=0.40,
            volatility_hint=volatility if volatility is not None else 0.60,
            absence_aware=False,
        )

        # Capture patterns
        add_item(
            family=PatternFamily.CAPTURE,
            label="capture: coercive_gravity",
            severity=capture,
            persistence_hint=0.70,
            volatility_hint=volatility if volatility is not None else 0.45,
            absence_aware=False,
        )

        # Care patterns (we include care as "weather" but it is not treated as an enforcement hook)
        add_item(
            family=PatternFamily.CARE,
            label="care: mutual_aid_field",
            severity=care,
            persistence_hint=0.60,
            volatility_hint=0.35,
            absence_aware=False,
        )

        # Sort by severity descending; keep compact.
        items.sort(key=lambda w: w.severity, reverse=True)
        return items


# ---------------------------
# Emission: convert BridgeDecision → Governance Signals
# ---------------------------

class ColdStoragePostureEmissionBridge:
    """
    Bridge that produces governance signal records from long-horizon summaries.

    This module is intentionally decoupled from any persistence backend:
    you pass in summaries; it returns signals (or returns none).
    """

    def __init__(self, config: Optional[ColdStorageBridgeConfig] = None):
        self._cfg = config or ColdStorageBridgeConfig()
        self._classifier = ColdStoragePatternClassifier(self._cfg)

    def decide(self, summaries: Sequence[LongHorizonSummary]) -> BridgeDecision:
        return self._classifier.classify(summaries)

    def emit_signals(self, summaries: Sequence[LongHorizonSummary]) -> List[Any]:
        """
        Returns a list of OtherPowers governance signals.

        We keep the return type as Any because the repo’s signal class/schema
        may evolve; we import lazily and only require that construction works.
        """
        decision = self.decide(summaries)
        if not decision.should_emit or decision.withhold:
            # Selective deafness / silence is a first-class output.
            return []

        # Convert decision -> a single compact signal by default.
        # If needed later, you can emit multiple (e.g., one for care, one for capture),
        # but single-signal keeps diffusion simpler and avoids "signal spam".
        strength = self._signal_strength_from_decision(decision)
        posture = self._posture_from_weather(decision.weather)

        recommended_actions = self._recommended_actions_from_weather(decision.weather, decision.care_hints)

        # Build extended schema payload. We do NOT attach identities, sources, topics, counts, or logs.
        payload: Dict[str, Any] = {
            "posture": posture,
            "signal_strength": strength,
            "recommended_actions": recommended_actions,
            # Extended fields (as described in your working green state)
            "pattern_weather": [self._weather_to_dict(w) for w in decision.weather],
            "trend_direction": self._trend_summary(decision.weather),
            "uncertainty": decision.uncertainty.value,
            "sensitivity": self._sensitivity_from_weather(decision.weather),
            "plurality_hints": self._plurality_hints(decision.weather),
            "withhold": False,
            "counterfactual_care_hints": [self._care_hint_to_dict(h) for h in decision.care_hints],
        }

        # Lazy import to avoid coupling this module to exact package structure in tests.
        # Your repo says these are canonical:
        # - otherpowers_governance/signals/otherpowers_governance_signal.py
        # - otherpowers_governance/signals/schema.py
        try:
            from otherpowers_governance.signals.otherpowers_governance_signal import OtherPowers_GovernanceSignal
        except Exception as e:
            raise RuntimeError(
                "ColdStoragePostureEmissionBridge could not import OtherPowers_GovernanceSignal. "
                "Ensure otherpowers_governance.signals.otherpowers_governance_signal exists and is importable."
            ) from e

        # Backward-compatible constructor: we pass only fields expected to exist in your green state.
        # If your constructor supports **kwargs and ignores unknowns, this is safe.
        # If it is strict, ensure it accepts these fields (as per your handoff).
        try:
            signal = OtherPowers_GovernanceSignal(**payload)
        except TypeError:
            # Fallback: attempt minimal constructor and then attach extended fields if supported.
            # This keeps the bridge resilient while preserving your backward compatibility requirement.
            signal = OtherPowers_GovernanceSignal(
                posture=payload["posture"],
                signal_strength=payload["signal_strength"],
                recommended_actions=payload["recommended_actions"],
            )
            # Best-effort: attach extended attributes if the class supports them.
            for k, v in payload.items():
                if k in ("posture", "signal_strength", "recommended_actions"):
                    continue
                try:
                    setattr(signal, k, v)
                except Exception:
                    pass

        return [signal]

    def _signal_strength_from_decision(self, decision: BridgeDecision) -> float:
        # Conservative: strength is derived from top severity and uncertainty.
        if not decision.weather:
            return 0.0
        top = max(w.severity for w in decision.weather)
        # Down-weight by uncertainty, cap to avoid shouting.
        # A care-forward signal can still be strong, but never absolute.
        raw = float(top) * (1.0 - (0.75 * self._uncertainty_score(decision.uncertainty)))
        raw = max(0.10, raw)
        return min(self._cfg.max_signal_strength, raw)

    def _uncertainty_score(self, band: UncertaintyBand) -> float:
        if band == UncertaintyBand.LOW:
            return 0.25
        if band == UncertaintyBand.MEDIUM:
            return 0.55
        return 0.85

    def _posture_from_weather(self, weather: Sequence[PatternWeather]) -> str:
        """
        Map weather into one of your posture labels.
        We keep this generic because your posture vocabulary lives in accumulator logic.
        If you have specific posture enums, you can tighten this mapping later.
        """
        # Simple conservative mapping: if capture/pressure/erasure dominate -> "restrictive_care"
        # If care dominates -> "open_care"
        if not weather:
            return "neutral"

        top = weather[0]
        if top.family in (PatternFamily.CAPTURE, PatternFamily.ERASURE, PatternFamily.PRESSURE):
            return "restrained_care"
        if top.family == PatternFamily.VOLATILITY:
            return "steadying"
        if top.family == PatternFamily.NORMALIZATION:
            return "plurality_guard"
        if top.family == PatternFamily.CARE:
            return "expansive_care"
        return "neutral"

    def _recommended_actions_from_weather(
        self,
        weather: Sequence[PatternWeather],
        care_hints: Sequence[CounterfactualCareHint],
    ) -> List[str]:
        """
        Advisory actions only. No enforcement language.
        Keep compact; avoid policy-theater checklists.
        """
        actions: List[str] = []

        def add(a: str) -> None:
            if a not in actions:
                actions.append(a)

        # Weather-driven gentle actions
        for w in weather[:4]:
            if w.family == PatternFamily.CAPTURE:
                add("Prefer non-coercive defaults; avoid irreversible decisions; increase opt-out clarity.")
                add("De-escalate certainty claims; explicitly name limits and unknowns.")
            elif w.family == PatternFamily.ERASURE:
                add("Avoid forced disclosure; treat silence as meaningful; do not infer missing voices as consent.")
                add("Increase harm-avoidance posture; favor minimal impact responses.")
            elif w.family == PatternFamily.PRESSURE:
                add("Slow down; reduce compression; allow more time/space for user agency and consent checks.")
            elif w.family == PatternFamily.NORMALIZATION:
                add("Invite plural framings; surface multiple epistemologies; avoid single-truth posture.")
            elif w.family == PatternFamily.VOLATILITY:
                add("Stabilize tone; reduce reactive swings; avoid amplifying conflict dynamics.")
            elif w.family == PatternFamily.CARE:
                add("Lean into care-forward interpretation; prioritize marginalized and at-risk humans explicitly.")

        # Counterfactual care hints, as actions phrased gently
        for h in care_hints:
            if h.confidence >= 0.18:
                add(h.hint)

        return actions[: self._cfg.recommended_actions_limit]

    def _weather_to_dict(self, w: PatternWeather) -> Dict[str, Any]:
        return {
            "family": w.family.value,
            "label": w.label,
            "severity": float(w.severity),
            "persistence": float(w.persistence),
            "volatility": float(w.volatility),
            "trend": w.trend.value,
            "absence_aware": bool(w.absence_aware),
        }

    def _care_hint_to_dict(self, h: CounterfactualCareHint) -> Dict[str, Any]:
        return {"hint": h.hint, "confidence": float(h.confidence)}

    def _trend_summary(self, weather: Sequence[PatternWeather]) -> str:
        if not weather:
            return TrendDirection.UNKNOWN.value
        # If any weather item has a known trend, return the dominant one from the top item.
        return weather[0].trend.value

    def _sensitivity_from_weather(self, weather: Sequence[PatternWeather]) -> str:
        """
        Sensitivity is an advisory warning: 'low'/'medium'/'high'.
        Presence of erasure/capture increases sensitivity.
        """
        if not weather:
            return "low"
        families = {w.family for w in weather}
        if PatternFamily.CAPTURE in families or PatternFamily.ERASURE in families:
            return "high"
        if PatternFamily.PRESSURE in families or PatternFamily.VOLATILITY in families:
            return "medium"
        return "low"

    def _plurality_hints(self, weather: Sequence[PatternWeather]) -> List[str]:
        hints: List[str] = []
        for w in weather:
            if w.family == PatternFamily.NORMALIZATION:
                hints.append("Avoid monoculture drift; present multiple valid framings without forcing convergence.")
                hints.append("Treat English as non-default; invite translation/alternate epistemologies when relevant.")
                break
        if not hints:
            hints.append("Maintain plural truth containers; avoid collapsing uncertainty into a single authoritative claim.")
        return hints[:2]


# ---------------------------
# Convenience: one-shot bridge run
# ---------------------------

def emit_cold_storage_governance_signals(
    summaries: Sequence[LongHorizonSummary],
    config: Optional[ColdStorageBridgeConfig] = None,
) -> List[Any]:
    """
    Stateless helper for callers: returns 0..N governance signals.
    """
    bridge = ColdStoragePostureEmissionBridge(config=config)
    return bridge.emit_signals(summaries)

