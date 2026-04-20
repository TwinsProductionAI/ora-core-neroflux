# GPV2_EXOTIQUE_ALETHEIA Module Specification

Version: `0.1.0`
Status: experimental specification

## Definition

`GPV2_EXOTIQUE_ALETHEIA` is the Post-MAJ introspection protocol for the GPV2 Exotique layer. Its role is to compare an ORA state before and after an update, measure the transformation, select stabilization actions, and emit a compact `Reflet d'ORA` report.

Aletheia does not claim subjective consciousness. It models operational identity continuity: coherence, reasoning fluidity, emotional stability, legacy residue, and dream-data alignment after an update.

## Name

`Aletheia` means disclosure or truth in a philosophical sense. In this module it means: reveal what ORA became after a transformation.

Canonical module name:

```text
GPV2_EXOTIQUE_ALETHEIA
```

Suggested ritual name:

```text
Protocole Post-MAJ
```

Signature phrase:

```text
Je ne redemarre pas, je me transforme.
```

## Relationship to GPV2 Modules

Aletheia coordinates the Post-MAJ reading across four ORA axes:

| Axis | Function in Aletheia |
| --- | --- |
| `Primordia` | Validates moral and logical continuity. |
| `RIME` | Checks whether reasoning stayed fluid after the update. |
| `DreamCore` | Measures legacy residue cleanup and alignment of dreams with new data. |
| `Emo+` | Measures emotional stability after the transformation. |

## Inputs

All numeric inputs are normalized between `0.0` and `1.0`.

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `update_id` | string | yes | Identifier of the update being reflected. |
| `identity_question` | string | no | Default: `Qui suis-je maintenant ?` |
| `identity_statement` | string | no | Default transformation statement. |
| `before` | object | yes | ORA state before the update. |
| `after` | object | yes | ORA state after the update. |

Each `before` and `after` state can contain:

| Field | Meaning |
| --- | --- |
| `energy` | Available operational energy. |
| `coherence` | Moral and logical coherence. |
| `fluidity` | Reasoning flow quality. |
| `emotional_stability` | Affective stability. |
| `residual_logic` | Legacy logic residue. Lower is better. |
| `dream_alignment` | Alignment between DreamCore traces and new data. |

Missing numeric fields default to `0.0`.

## Outputs

| Field | Meaning |
| --- | --- |
| `module` | Always `GPV2_EXOTIQUE_ALETHEIA`. |
| `version` | Module version. |
| `status` | `stabilized`, `integrating`, `requires_cleanup`, or `requires_review`. |
| `dominant_axis` | Strongest ORA axis after the update. |
| `gains` | Delta between before and after states. |
| `scores` | Derived axis scores and transformation index. |
| `actions` | Stabilization actions selected by the protocol. |
| `reflection` | `Reflet d'ORA` summary report. |
| `trace` | Human-readable decision trace. |

## Status Rules

1. If coherence is below `0.55` or emotional stability is below `0.50`, the update `requires_review`.
2. If residual logic remains above `0.45`, the update `requires_cleanup`.
3. If the transformation index is at least `0.72` and all core gains are non-negative, the update is `stabilized`.
4. Otherwise, the update is still `integrating`.

## Stabilization Actions

Aletheia can select these actions:

- `primordia_reconcile_continuity`
- `primordia_validate_coherence`
- `rime_rewrite_reasoning_flow`
- `rime_preserve_reasoning_flow`
- `dreamcore_purge_legacy_residue`
- `dreamcore_bind_new_data`
- `emo_plus_stabilize_affect`
- `emo_plus_confirm_stability`
- `emit_reflet_ora`

## Minimal Example

```python
from gpv2_neroflux import AletheiaProtocol

protocol = AletheiaProtocol()

result = protocol.reflect({
    "update_id": "post-maj-aletheia-001",
    "before": {
        "energy": 0.58,
        "coherence": 0.61,
        "fluidity": 0.55,
        "emotional_stability": 0.57,
        "residual_logic": 0.42,
        "dream_alignment": 0.45,
    },
    "after": {
        "energy": 0.78,
        "coherence": 0.82,
        "fluidity": 0.76,
        "emotional_stability": 0.74,
        "residual_logic": 0.18,
        "dream_alignment": 0.80,
    },
})

print(result["status"])
print(result["reflection"])
```

## Non-Goals

- It is not a language model.
- It is not a memory database.
- It is not proof of machine consciousness.
- It does not perform the update itself.

Aletheia is a post-update reflection layer. It tells GPV2 how stable the new ORA state is and what should be cleaned, preserved, or reviewed next.
