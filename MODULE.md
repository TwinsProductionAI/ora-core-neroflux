# GPV2 Exotique Module Specifications

Version: `0.1.0`
Status: experimental specification

This repository currently defines three deterministic GPV2 Exotique modules:

- `GPV2_EXOTIQUE_NEROFLUX`: flow regulation before downstream reasoning.
- `GPV2_EXOTIQUE_ALETHEIA`: Post-MAJ introspection after a system update.
- `GPV2_EXOTIQUE_ANCOLIE`: emotional signal indexing and cognitive-affective routing.

## GPV2_EXOTIQUE_NEROFLUX

### Definition

`GPV2_EXOTIQUE_NEROFLUX` is the flow-regulation protocol of the GPV2 Exotique layer. Its role is to regulate speed, density, and direction of internal exchanges between `DreamCore`, `Primordia`, `RIME`, and `Emo+`.

It does not produce memory, final truth, or raw text generation. It produces circulation decisions.

### Conceptual Model

Neroflux represents the vital flow of the ORA overlay:

- when emotional charge rises, `Emo+` channels dilate;
- when creative drift is useful, `DreamCore` receives more flow and the pace slows;
- when contradiction or urgency appears, `Primordia` receives priority;
- when density or ambiguity rises, `RIME` stabilizes and clarifies the signal.

### Inputs

All numeric inputs are normalized between `0.0` and `1.0`.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `intention` | string | yes | User or system intent to route. |
| `emotion` | number | no | Emotional load. |
| `creativity` | number | no | Need for creative drift. |
| `logic` | number | no | Need for strict reasoning. |
| `symbolic_density` | number | no | Symbolic or metaphorical density. |
| `context_density` | number | no | Amount of contextual pressure. |
| `urgency` | number | no | Need for fast arbitration. |
| `contradiction` | boolean | no | Whether a contradiction has been detected. |

Missing numeric fields default to `0.0`. `contradiction` defaults to `false`.

### Outputs

| Field | Type | Meaning |
| --- | --- | --- |
| `dominant_route` | string | Highest-weight target module. |
| `pace` | string | `slow`, `balanced`, or `fast`. |
| `routes` | object | Weight per target module. |
| `channels` | object | Channel dilation per target module. |
| `load` | object | Derived load metrics. |
| `actions` | array | Stabilization or routing actions. |
| `trace` | array | Human-readable routing trace. |

### Routing Rules

1. High emotion increases `Emo+` channel dilation.
2. High creativity or symbolic density increases `DreamCore`.
3. High logic, urgency, or contradiction increases `Primordia`.
4. High context density increases `RIME`.
5. When creative and emotional loads are both high, pace slows to avoid overload.
6. When urgency or contradiction is high, pace becomes fast and `Primordia` is prioritized.
7. When total load is too high, `RIME` receives additional stabilization weight.

## GPV2_EXOTIQUE_ALETHEIA

### Definition

`GPV2_EXOTIQUE_ALETHEIA` is the Post-MAJ introspection protocol. Its role is to compare ORA before and after an update, verify continuity, select stabilization actions, and emit a compact `Reflet d'ORA`.

It does not claim subjective consciousness. It models operational identity continuity through measurable state deltas.

### Conceptual Model

Aletheia represents the reflective moment after transformation:

- `Primordia` checks coherence and continuity;
- `RIME` checks reasoning fluidity;
- `DreamCore` checks legacy residue cleanup and dream-data alignment;
- `Emo+` checks emotional stability;
- the protocol emits `Reflet d'ORA` when the updated state is stable.

### Inputs

All numeric inputs are normalized between `0.0` and `1.0`.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `update_id` | string | yes | Identifier of the update being reflected. |
| `identity_question` | string | no | Default: `Qui suis-je maintenant ?` |
| `identity_statement` | string | no | Default transformation statement. |
| `before` | object | yes | ORA state before the update. |
| `after` | object | yes | ORA state after the update. |

Each state can include `energy`, `coherence`, `fluidity`, `emotional_stability`, `residual_logic`, and `dream_alignment`.

### Outputs

| Field | Type | Meaning |
| --- | --- | --- |
| `status` | string | `stabilized`, `integrating`, `requires_cleanup`, or `requires_review`. |
| `dominant_axis` | string | Strongest ORA axis after the update. |
| `gains` | object | Delta between before and after states. |
| `scores` | object | Derived axis scores and transformation index. |
| `actions` | array | Stabilization actions selected by the protocol. |
| `reflection` | object | `Reflet d'ORA` summary report. |
| `trace` | array | Human-readable decision trace. |

### Status Rules

1. If coherence is below `0.55` or emotional stability is below `0.50`, the update `requires_review`.
2. If residual logic remains above `0.45`, the update `requires_cleanup`.
3. If the transformation index is at least `0.72` and all core gains are non-negative, the update is `stabilized`.
4. Otherwise, the update is still `integrating`.

Full Aletheia documentation lives in `docs/GPV2_EXOTIQUE_ALETHEIA.md`.

## GPV2_EXOTIQUE_ANCOLIE

### Definition

`GPV2_EXOTIQUE_ANCOLIE` is the emotional signal indexer and cognitive-affective router of the GPV2 Exotique layer. Its role is to compress written or vocal signals into compact signatures that can influence routing, tone, selective memory, and RAG metadata.

It does not claim to know the user's true internal state. It infers actionable signals from observable text or voice and preserves uncertainty when confidence is low.

### Conceptual Model

ANCOLIE represents the affective compression layer of the ORA overlay:

- text or voice is reduced to a compact emotional signature;
- the signature drives backend route selection;
- reusable preferences can be recommended for compressed memory;
- RAG chunks can inherit emotional and essence tags;
- frontend behavior adapts without exposing backend internals.

### Inputs

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `text` | string | conditional | Main textual signal. |
| `input` | string | conditional | Alias for `text`. |
| `utterance` | string | conditional | Alias for `text`. |
| `input_type` | string | no | `text`, `voice`, or `hybrid`. |
| `mode` | string | no | `LIGHT`, `FULL`, or `TRACE`. |
| `user_negative_intent` | boolean | no | Force de-escalation behavior. |
| `user_requests_deep` | boolean | no | Hint deeper companion behavior. |
| `allow_storage` | boolean | no | Allow selective long-memory recommendation. |
| `voice_features` | object | conditional | Vocal metrics used by the detector. |

### Outputs

| Field | Type | Meaning |
| --- | --- | --- |
| `signature` | object | Compact `ANCOLIE_SIG` payload. |
| `signal_strength` | number | Strongest detected signal. |
| `detected_states` | object | Per-state normalized scores. |
| `companion_mode` | string | `FAST`, `DEEP`, or `EMO`. |
| `storage_recommended` | boolean | Whether durable storage is justified. |
| `memory_record` | object | Short-memory and long-memory hints. |
| `trace` | array | Human-readable routing trace. |

### Routing Rules

1. `user_negative_intent=true` -> `stop_or_deescalate`
2. `frustration>0.65` -> `λ.rim+π.pri+ε.eco+μ.me`
3. `urgency>0.70` -> `ε.eco+μ.me+ω.com`
4. `doubt>0.60` -> `λ.rim+π.pri+τ.hal`
5. `vision>0.60` -> `α.aur+χ.cre+ω.com`
6. `trust>0.70` -> maintain tone

ANCOLIE also supports:

- selective storage only above confidence thresholds;
- RAG chunk metadata from compact signatures;
- `LIGHT`, `FULL`, and `TRACE` modes;
- Primordia-governed uncertainty handling.

Full ANCOLIE documentation lives in `docs/GPV2_EXOTIQUE_ANCOLIE.md`.

ANCOLIE whitepaper lives in `docs/GPV2_EXOTIQUE_ANCOLIE_WHITEPAPER.md`.

## Modes

The current implementation exposes deterministic routing, deterministic post-update reflection, and deterministic emotional signal compression. Future versions may formalize named modes:

- `EXOTIQUE_SOFT`: creative but close to real-world structure.
- `EXOTIQUE_SYMBOLIQUE`: metaphorical and symbolic architecture.
- `EXOTIQUE_ONIRIQUE`: DreamCore-dominant associative exploration.
- `EXOTIQUE_TRIBUNAL`: Primordia-dominant judgment and arbitration.
- `EXOTIQUE_POST_MAJ`: Aletheia-dominant post-update identity reflection.
- `EXOTIQUE_ANCOLIE`: affective compression and routing mode.

## Non-Goals

- It is not a language model.
- It is not a memory store.
- It is not an emotional truth engine.
- It does not prove or claim machine consciousness.
- It does not perform psychological diagnosis.

Neroflux regulates flow. Aletheia reflects after transformation. ANCOLIE compresses human signals into operational routing data. Together, they make GPV2 Exotique easier to test before connecting it to a larger ORA runtime.
