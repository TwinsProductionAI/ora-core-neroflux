"""Deterministic emotional signal indexing for GPV2_EXOTIQUE_ANCOLIE."""

from __future__ import annotations

import unicodedata
from copy import deepcopy
from typing import Any

from .neroflux import clamp

MODE_KEYS = ("LIGHT", "FULL", "TRACE")
VOICE_FIELDS = (
    "loudness",
    "speech_rate",
    "pause_ratio",
    "pitch_variation",
    "tension",
)
EMOTION_ORDER = (
    "frustr",
    "urgency",
    "doubt",
    "vision",
    "focus",
    "control",
    "clarity",
    "security",
    "fear",
    "trust",
    "calm",
    "curiosity",
    "joy",
    "fatigue",
    "pride",
    "anger",
)
ROUTE_ORDER = (
    "λ.rim",
    "π.pri",
    "ε.eco",
    "σ.son",
    "α.aur",
    "τ.hal",
    "μ.me",
    "χ.cre",
    "ω.com",
    "ANCOLIE",
)

DETECTION_MIN = 0.45
STORE_MIN = 0.75
ROUTE_ADJUST_MIN = 0.55
TRACE_MIN = 0.70
UNCERTAINTY_MIN = 0.50

TEXT_SIGNAL_KEYWORDS: dict[str, tuple[str, ...]] = {
    "joy": ("genial", "super", "top", "parfait", "j adore", "excellent"),
    "focus": (
        "concret",
        "precis",
        "pratique",
        "action",
        "etape",
        "checklist",
        "structure",
        "direct",
        "simple",
        "exploitable",
    ),
    "urgency": (
        "urgent",
        "vite",
        "rapidement",
        "maintenant",
        "tout de suite",
        "court",
        "fast",
        "asap",
    ),
    "fear": ("peur", "inquiet", "risque", "dangereux", "bloque", "echoue"),
    "frustr": (
        "arrete",
        "stop",
        "vague",
        "flou",
        "vide",
        "superficiel",
        "mauvais",
        "reprends",
        "corrige",
        "pas ca",
    ),
    "trust": ("merci", "je compte sur toi", "comme d habitude", "je te fais confiance"),
    "doubt": (
        "tu es sur",
        "tu es certain",
        "doute",
        "incertain",
        "verifie",
        "preuve",
        "source",
        "factuel",
        "fiable",
        "exact",
    ),
    "fatigue": ("fatigue", "epuise", "surcharge", "trop", "dense", "lourd"),
    "pride": ("premium", "haut niveau", "excellence", "prestige", "propre"),
    "calm": ("calme", "tranquillement", "prends ton temps", "pose", "sereinement"),
    "anger": ("colere", "agace", "ridicule", "n importe quoi", "saoule"),
    "curiosity": ("comment", "pourquoi", "explique", "exploration", "idee", "curieux"),
    "vision": (
        "vision",
        "ambition",
        "roadmap",
        "strategie",
        "strategique",
        "futur",
        "long terme",
        "scale",
        "croissance",
    ),
    "control": (
        "je veux",
        "strict",
        "respecte",
        "brief",
        "sans",
        "cadre",
        "controle",
        "proprement",
    ),
    "security": ("securite", "safe", "sur", "garantie", "budget", "cout", "fiable"),
    "clarity": ("clair", "clarte", "lisible", "net", "pas vague", "sans flafla"),
}

IMPERATIVE_HINTS = (
    "fais",
    "donne",
    "montre",
    "explique",
    "reprends",
    "arrete",
    "sors",
    "produis",
)
QUALITY_HINTS = (
    "prends ton temps",
    "fais le bien",
    "fais-le bien",
    "proprement",
    "qualite",
    "complet",
    "profond",
)


def normalize_ancolie_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Return a normalized ANCOLIE packet."""

    normalized = deepcopy(packet)

    text = str(
        normalized.get("text", normalized.get("input", normalized.get("utterance", "")))
    ).strip()
    voice_features = _normalize_voice_features(normalized.get("voice_features"))

    input_type = str(normalized.get("input_type", "")).strip().lower()
    if not input_type:
        if text and voice_features:
            input_type = "hybrid"
        elif voice_features:
            input_type = "voice"
        else:
            input_type = "text"

    if input_type not in {"text", "voice", "hybrid"}:
        raise ValueError("ANCOLIE packet field 'input_type' must be text, voice, or hybrid.")

    if not text and not voice_features:
        raise ValueError("ANCOLIE packet requires non-empty 'text' or 'voice_features'.")

    mode = str(normalized.get("mode", "LIGHT")).strip().upper()
    if mode not in MODE_KEYS:
        raise ValueError("ANCOLIE packet field 'mode' must be LIGHT, FULL, or TRACE.")

    normalized["text"] = text
    normalized["input_type"] = input_type
    normalized["mode"] = mode
    normalized["voice_features"] = voice_features
    normalized["user_negative_intent"] = bool(normalized.get("user_negative_intent", False))
    normalized["user_requests_deep"] = bool(normalized.get("user_requests_deep", False))
    normalized["allow_storage"] = bool(normalized.get("allow_storage", mode != "LIGHT"))
    return normalized


class AncolieIndexer:
    """Index emotional signals into compact ORA-compatible signatures."""

    def analyze(self, packet: dict[str, Any]) -> dict[str, Any]:
        normalized = normalize_ancolie_packet(packet)
        text = normalized["text"]
        voice_features = normalized["voice_features"]

        text_scores = self._score_text_signals(text)
        voice_scores = self._score_voice_signals(voice_features)
        scores = self._blend_scores(text_scores, voice_scores, normalized["input_type"])
        top_emotions = self._select_top_emotions(scores)
        intensity = self._measure_intensity(scores, top_emotions)
        confidence = self._measure_confidence(scores, normalized)
        need = self._derive_needs(text, scores)
        friction = self._derive_friction(text, scores)
        memory = self._derive_memory(text, friction, scores)
        risk = self._derive_risk(scores, normalized["user_negative_intent"])
        route_tokens, tone_tokens, action = self._select_route_bundle(
            normalized=normalized,
            scores=scores,
            friction=friction,
            memory=memory,
            risk=risk,
        )
        route_tokens = self._apply_mode_policy(
            route_tokens=route_tokens,
            scores=scores,
            mode=normalized["mode"],
            risk=risk,
        )
        storage_recommended = self._should_store(
            allow_storage=normalized["allow_storage"],
            confidence=confidence,
            memory=memory,
            mode=normalized["mode"],
        )
        companion_mode = self._select_companion_mode(normalized["mode"], scores, confidence)
        signature = {
            "emo": "+".join(top_emotions),
            "intensity": intensity,
            "confidence": confidence,
            "need": need,
            "friction": friction,
            "route": "+".join(route_tokens),
            "tone": "+".join(tone_tokens),
            "memory": memory,
            "risk": risk,
            "action": action,
        }
        memory_record = self._build_memory_record(signature, storage_recommended)
        trace = self._build_trace(
            normalized=normalized,
            signature=signature,
            scores=scores,
            companion_mode=companion_mode,
            storage_recommended=storage_recommended,
        )

        return {
            "module": "GPV2_EXOTIQUE_ANCOLIE",
            "version": "1.0.0",
            "mode": normalized["mode"],
            "input_type": normalized["input_type"],
            "signal_strength": round(max(scores.values(), default=0.0), 3),
            "detected_states": scores,
            "companion_mode": companion_mode,
            "storage_recommended": storage_recommended,
            "memory_record": memory_record,
            "signature": signature,
            "trace": trace,
        }

    def build_rag_chunk_meta(
        self,
        doc_id: str,
        result: dict[str, Any],
        *,
        use_case: str = "general",
    ) -> dict[str, Any]:
        return build_rag_chunk_meta(doc_id, result, use_case=use_case)

    def build_log(self, result: dict[str, Any]) -> dict[str, Any]:
        return build_ancolie_log(result)

    def _score_text_signals(self, text: str) -> dict[str, float]:
        raw_text = text.strip()
        normalized_text = _normalize_text(text)
        scores = {emotion: 0.0 for emotion in EMOTION_ORDER}

        for emotion, keywords in TEXT_SIGNAL_KEYWORDS.items():
            scores[emotion] = clamp(_keyword_hits(normalized_text, keywords) * 0.22)

        if any(token in normalized_text for token in IMPERATIVE_HINTS):
            scores["focus"] = clamp(scores["focus"] + 0.14)
            scores["control"] = clamp(scores["control"] + 0.12)

        if "je veux" in normalized_text:
            scores["control"] = clamp(scores["control"] + 0.18)

        if any(token in normalized_text for token in QUALITY_HINTS):
            scores["calm"] = clamp(scores["calm"] + 0.14)
            scores["control"] = clamp(scores["control"] + 0.12)
            scores["clarity"] = clamp(scores["clarity"] + 0.10)

        if "concret" in normalized_text:
            scores["focus"] = clamp(scores["focus"] + 0.20)
            scores["clarity"] = clamp(scores["clarity"] + 0.12)

        if "vague" in normalized_text or "flou" in normalized_text:
            scores["frustr"] = clamp(scores["frustr"] + 0.22)
            scores["clarity"] = clamp(scores["clarity"] + 0.12)

        if "!" in raw_text:
            boost = min(raw_text.count("!"), 2) * 0.08
            scores["urgency"] = clamp(scores["urgency"] + boost)
            scores["frustr"] = clamp(scores["frustr"] + (boost / 2))

        if "?" in raw_text:
            scores["doubt"] = clamp(scores["doubt"] + min(raw_text.count("?"), 2) * 0.08)

        uppercase_tokens = [
            token for token in raw_text.split() if token.isupper() and len(token) > 2
        ]
        if uppercase_tokens:
            scores["urgency"] = clamp(scores["urgency"] + 0.06)
            scores["control"] = clamp(scores["control"] + 0.05)

        if "prends ton temps" in normalized_text:
            scores["calm"] = clamp(scores["calm"] + 0.16)
            scores["clarity"] = clamp(scores["clarity"] + 0.08)

        if "fais le bien" in normalized_text or "fais-le bien" in raw_text.casefold():
            scores["focus"] = clamp(scores["focus"] + 0.10)
            scores["control"] = clamp(scores["control"] + 0.10)

        return {emotion: round(score, 3) for emotion, score in scores.items()}

    def _score_voice_signals(self, voice_features: dict[str, float]) -> dict[str, float]:
        scores = {emotion: 0.0 for emotion in EMOTION_ORDER}
        if not voice_features:
            return scores

        loudness = voice_features["loudness"]
        speech_rate = voice_features["speech_rate"]
        pause_ratio = voice_features["pause_ratio"]
        pitch_variation = voice_features["pitch_variation"]
        tension = voice_features["tension"]

        scores["urgency"] = round(clamp((speech_rate * 0.45) + (tension * 0.35) + (loudness * 0.20)), 3)
        scores["frustr"] = round(clamp((loudness * 0.30) + (tension * 0.45) + (pitch_variation * 0.15)), 3)
        scores["calm"] = round(
            clamp((pause_ratio * 0.35) + ((1.0 - tension) * 0.30) + ((1.0 - loudness) * 0.15)),
            3,
        )
        scores["focus"] = round(
            clamp((speech_rate * 0.20) + ((1.0 - pause_ratio) * 0.20) + (tension * 0.10)),
            3,
        )
        scores["doubt"] = round(clamp((pause_ratio * 0.25) + (pitch_variation * 0.20)), 3)
        return scores

    def _blend_scores(
        self,
        text_scores: dict[str, float],
        voice_scores: dict[str, float],
        input_type: str,
    ) -> dict[str, float]:
        if input_type == "voice":
            return voice_scores

        if input_type == "hybrid":
            return {
                emotion: round(
                    clamp((text_scores[emotion] * 0.65) + (voice_scores[emotion] * 0.35)),
                    3,
                )
                for emotion in EMOTION_ORDER
            }

        return text_scores

    def _select_top_emotions(self, scores: dict[str, float]) -> list[str]:
        ordered = sorted(scores.items(), key=lambda item: (-item[1], EMOTION_ORDER.index(item[0])))
        strongest = ordered[0][1] if ordered else 0.0
        threshold = 0.35 if strongest >= DETECTION_MIN else 0.20
        top = [emotion for emotion, score in ordered if score >= threshold][:3]
        if not top:
            return ["clarity"]
        return top

    def _measure_intensity(self, scores: dict[str, float], top_emotions: list[str]) -> float:
        values = [scores[emotion] for emotion in top_emotions]
        if not values:
            return 0.0

        intensity = sum(values) / len(values)
        if values[0] >= 0.70:
            intensity += 0.05
        return round(clamp(intensity), 3)

    def _measure_confidence(self, scores: dict[str, float], packet: dict[str, Any]) -> float:
        strongest = max(scores.values(), default=0.0)
        signal_count = len([score for score in scores.values() if score >= 0.35])
        confidence = 0.36 + (strongest * 0.34) + (min(signal_count, 3) * 0.07)
        if packet["voice_features"] and packet["input_type"] in {"voice", "hybrid"}:
            confidence += 0.05
        if strongest < DETECTION_MIN:
            confidence -= 0.08
        return round(clamp(confidence), 3)

    def _derive_needs(self, text: str, scores: dict[str, float]) -> str:
        normalized_text = _normalize_text(text)
        needs: list[str] = []

        if "concret" in normalized_text or scores["focus"] >= ROUTE_ADJUST_MIN:
            needs.append("clarte")
            needs.append("action")

        if (
            "preuve" in normalized_text
            or "source" in normalized_text
            or scores["doubt"] >= ROUTE_ADJUST_MIN
        ):
            needs.append("preuve")
            needs.append("verification")

        if "qualite" in normalized_text or "fais le bien" in normalized_text:
            needs.append("qualite")
            needs.append("profondeur")

        if "brief" in normalized_text or "respecte" in normalized_text or scores["control"] >= 0.60:
            needs.append("respect_du_brief")

        if scores["urgency"] >= ROUTE_ADJUST_MIN:
            needs.append("rapidite")

        if scores["vision"] >= ROUTE_ADJUST_MIN:
            needs.append("strategie")
            needs.append("roadmap")

        if scores["security"] >= ROUTE_ADJUST_MIN or scores["fear"] >= ROUTE_ADJUST_MIN:
            needs.append("securite")

        if scores["fatigue"] >= ROUTE_ADJUST_MIN:
            needs.append("sobriete")

        if not needs:
            needs.append("clarte")

        return "+".join(_unique(needs))

    def _derive_friction(self, text: str, scores: dict[str, float]) -> str:
        normalized_text = _normalize_text(text)

        if "document vide" in normalized_text or "documents vides" in normalized_text:
            return "output_too_shallow"

        if "vague" in normalized_text or "flou" in normalized_text:
            return "vague_response"

        if scores["doubt"] >= ROUTE_ADJUST_MIN:
            return "uncertainty_gap"

        if "cout" in normalized_text or "budget" in normalized_text:
            return "cost_anxiety"

        if scores["fatigue"] >= ROUTE_ADJUST_MIN:
            return "context_overload"

        if scores["frustr"] >= ROUTE_ADJUST_MIN:
            return "response_misalignment"

        return "none_detected"

    def _derive_memory(self, text: str, friction: str, scores: dict[str, float]) -> str:
        normalized_text = _normalize_text(text)

        if friction == "output_too_shallow":
            return "avoid_shallow_document_generation"

        if "concret" in normalized_text or friction == "vague_response":
            return "prefer_concrete_outputs"

        if scores["doubt"] >= ROUTE_ADJUST_MIN or "preuve" in normalized_text:
            return "prefer_verified_answers"

        if scores["vision"] >= ROUTE_ADJUST_MIN:
            return "prefer_strategic_outputs"

        if "prends ton temps" in normalized_text or "qualite" in normalized_text:
            return "prefer_quality_over_speed"

        if scores["control"] >= 0.65 and "brief" in normalized_text:
            return "respect_explicit_brief_constraints"

        return "session_only"

    def _derive_risk(self, scores: dict[str, float], user_negative_intent: bool) -> str:
        if user_negative_intent or scores["anger"] >= 0.70 or scores["fear"] >= 0.75:
            return "high"

        if (
            scores["frustr"] >= 0.55
            or scores["doubt"] >= 0.55
            or scores["urgency"] >= 0.70
            or scores["control"] >= 0.75
        ):
            return "medium"

        return "low"

    def _select_route_bundle(
        self,
        *,
        normalized: dict[str, Any],
        scores: dict[str, float],
        friction: str,
        memory: str,
        risk: str,
    ) -> tuple[list[str], list[str], str]:
        if normalized["user_negative_intent"]:
            return (
                ["λ.rim", "π.pri", "μ.me", "ω.com", "τ.hal"],
                ["calme", "factuel"],
                "stop_or_deescalate",
            )

        if friction == "output_too_shallow":
            return (
                ["λ.rim", "π.pri", "ε.eco", "μ.me", "ω.com", "τ.hal"],
                ["direct", "responsable", "precis"],
                "produce_deep_structured_content_before_export",
            )

        if friction == "vague_response":
            return (
                ["λ.rim", "π.pri", "ε.eco", "μ.me", "ω.com"],
                ["direct", "pragmatique"],
                "produce_actionable_structure",
            )

        if scores["urgency"] > 0.75 and scores["urgency"] >= scores["frustr"]:
            return (
                ["ε.eco", "μ.me", "ω.com"],
                ["direct"],
                "surface_next_action",
            )

        if scores["frustr"] > 0.65:
            tones = ["calme", "direct"]
            if scores["focus"] >= 0.55 or scores["clarity"] >= 0.55:
                tones = ["direct", "pragmatique"]
            return (
                ["λ.rim", "π.pri", "ε.eco", "μ.me", "ω.com"],
                tones,
                "produce_corrective_response",
            )

        if scores["urgency"] > 0.70:
            return (
                ["ε.eco", "μ.me", "ω.com"],
                ["direct"],
                "surface_next_action",
            )

        if scores["doubt"] > 0.60:
            return (
                ["λ.rim", "π.pri", "τ.hal", "ω.com"],
                ["rassurant", "factuel"],
                "provide_verified_answer",
            )

        if scores["vision"] > 0.60:
            return (
                ["α.aur", "χ.cre", "ω.com"],
                ["strategique"],
                "produce_roadmap",
            )

        if scores["focus"] > 0.55 or scores["clarity"] > 0.55 or scores["control"] > 0.55:
            tones = ["direct", "pragmatique"]
            if memory == "prefer_quality_over_speed":
                tones = ["direct", "responsable", "precis"]
            return (
                ["λ.rim", "ε.eco", "ω.com"],
                tones,
                "produce_actionable_structure",
            )

        if scores["security"] > 0.55 or scores["fear"] > 0.55:
            return (
                ["π.pri", "τ.hal", "ω.com"],
                ["rassurant", "factuel"],
                "surface_safeguards_and_limits",
            )

        if scores["curiosity"] > 0.55:
            return (
                ["λ.rim", "χ.cre", "ω.com"],
                ["pedagogique", "ouvert"],
                "expand_with_examples",
            )

        if risk == "medium" and scores["trust"] >= 0.70:
            return (
                ["σ.son", "π.pri", "ω.com"],
                ["humain", "clair"],
                "maintain_tone",
            )

        return (
            ["σ.son", "ε.eco", "ω.com"],
            ["clair", "humain"],
            "maintain_clear_response",
        )

    def _apply_mode_policy(
        self,
        *,
        route_tokens: list[str],
        scores: dict[str, float],
        mode: str,
        risk: str,
    ) -> list[str]:
        if mode == "TRACE":
            if "τ.hal" not in route_tokens:
                route_tokens.append("τ.hal")
            return _ordered_route(route_tokens)

        if mode == "LIGHT" and risk == "low" and max(scores.values(), default=0.0) < 0.65:
            if scores["urgency"] >= 0.55 or scores["frustr"] >= 0.55:
                return ["λ.rim", "ε.eco", "μ.me", "ω.com"]
            return ["σ.son", "ε.eco"]

        return _ordered_route(route_tokens)

    def _should_store(
        self,
        *,
        allow_storage: bool,
        confidence: float,
        memory: str,
        mode: str,
    ) -> bool:
        return (
            allow_storage
            and mode != "LIGHT"
            and confidence >= STORE_MIN
            and memory != "session_only"
        )

    def _select_companion_mode(
        self,
        mode: str,
        scores: dict[str, float],
        confidence: float,
    ) -> str:
        emotional_peak = max(
            scores["frustr"],
            scores["fear"],
            scores["trust"],
            scores["anger"],
            scores["joy"],
        )
        if mode != "TRACE" and scores["urgency"] >= 0.80 and scores["urgency"] >= scores["frustr"]:
            return "FAST"

        if mode == "TRACE" or confidence >= 0.80:
            return "DEEP"

        if emotional_peak >= 0.70 and max(scores.values(), default=0.0) >= ROUTE_ADJUST_MIN:
            return "EMO"

        if mode == "FULL" or scores["doubt"] >= 0.60 or scores["vision"] >= 0.60:
            return "DEEP"

        return "FAST"

    def _build_memory_record(
        self,
        signature: dict[str, Any],
        storage_recommended: bool,
    ) -> dict[str, Any]:
        return {
            "short_mem": {
                "session_state": signature["route"],
                "last_emotion": signature["emo"].split("+")[0],
                "current_need": signature["need"],
                "response_adjustment": signature["action"],
            },
            "long_mem": {
                "stable_preference": signature["memory"] if storage_recommended else "",
                "repeated_pattern": signature["emo"] if storage_recommended else "",
                "communication_style": signature["tone"] if storage_recommended else "",
                "avoid_pattern": signature["friction"] if storage_recommended else "",
            },
        }

    def _build_trace(
        self,
        *,
        normalized: dict[str, Any],
        signature: dict[str, Any],
        scores: dict[str, float],
        companion_mode: str,
        storage_recommended: bool,
    ) -> list[str]:
        strongest = max(scores, key=scores.get) if scores else "clarity"
        uncertainty = "required" if signature["confidence"] < UNCERTAINTY_MIN else "not required"
        return [
            f"ancolie input accepted: {normalized['input_type']} / {normalized['mode']}",
            f"dominant emotional state: {strongest}",
            f"signature route selected: {signature['route']}",
            f"companion mode selected: {companion_mode}",
            f"memory policy: {'store_compressed' if storage_recommended else 'session_only'}",
            f"uncertainty flag: {uncertainty}",
        ]


def build_rag_chunk_meta(
    doc_id: str,
    result: dict[str, Any],
    *,
    use_case: str = "general",
) -> dict[str, Any]:
    """Build RAG metadata from an ANCOLIE analysis result."""

    normalized_doc_id = str(doc_id).strip()
    if not normalized_doc_id:
        raise ValueError("RAG metadata requires a non-empty 'doc_id'.")

    signature = result["signature"] if "signature" in result else result
    essence_tags = [tag for tag in signature["route"].split("+") if tag]
    emo_tags = [tag for tag in signature["emo"].split("+") if tag]
    risk = signature.get("risk", "low")

    if any(tag in emo_tags for tag in ("vision", "control", "clarity", "doubt")):
        retrieval_priority = "high"
    elif risk == "medium":
        retrieval_priority = "high"
    elif any(tag in emo_tags for tag in ("focus", "curiosity", "trust")):
        retrieval_priority = "medium"
    else:
        retrieval_priority = "low"

    return {
        "doc_id": normalized_doc_id,
        "essence_tags": essence_tags,
        "emo_tags": emo_tags,
        "use_case": str(use_case).strip() or "general",
        "risk": risk,
        "retrieval_priority": retrieval_priority,
    }


def build_ancolie_log(result: dict[str, Any]) -> dict[str, Any]:
    """Build the lightweight ANCOLIE log structure from an analysis result."""

    signature = result["signature"] if "signature" in result else result
    return {
        "timestamp": "",
        "input_type": result.get("input_type", "text"),
        "detected_emo": signature.get("emo", ""),
        "confidence": signature.get("confidence", 0.0),
        "route": signature.get("route", ""),
        "action": signature.get("action", ""),
        "stored": bool(result.get("storage_recommended", False)),
    }


def _normalize_voice_features(raw_voice_features: Any) -> dict[str, float]:
    if raw_voice_features in (None, {}):
        return {}

    if not isinstance(raw_voice_features, dict):
        raise ValueError("ANCOLIE packet field 'voice_features' must be an object.")

    normalized: dict[str, float] = {}
    for field in VOICE_FIELDS:
        raw_value = raw_voice_features.get(field, 0.0)
        try:
            normalized[field] = round(clamp(float(raw_value)), 3)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Field 'voice_features.{field}' must be numeric.") from exc
    return normalized


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text.casefold())
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.replace("'", " ")
    normalized = normalized.replace("-", " ")
    return " ".join(normalized.split())


def _keyword_hits(text: str, keywords: tuple[str, ...]) -> int:
    return sum(1 for keyword in keywords if keyword in text)


def _ordered_route(route_tokens: list[str]) -> list[str]:
    unique_tokens = _unique(route_tokens)
    return [token for token in ROUTE_ORDER if token in unique_tokens]


def _unique(values: list[str]) -> list[str]:
    ordered: list[str] = []
    for value in values:
        if value and value not in ordered:
            ordered.append(value)
    return ordered
