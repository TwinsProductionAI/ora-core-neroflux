# GPV2_EXOTIQUE_ANCOLIE Module Specification

Version: `1.0.0`
Status: working canon

## Definition

`GPV2_EXOTIQUE_ANCOLIE` is the emotional signal indexer and cognitive-affective
router of the GPV2 Exotique layer. Its role is to analyze written or vocal
signals, compress them into compact emotional signatures, and reuse those
signatures to adapt tone, routing, memory, and RAG metadata without inflating
the active context window.

ANCOLIE does not diagnose the user. It infers only actionable signal patterns
from text or voice and keeps uncertainty explicit when confidence is low.

## Core Role

ANCOLIE exists to:

- detect dominant emotional state;
- reduce token pressure through compact signatures;
- improve long-memory precision with selective storage;
- adapt frontend tone without exposing backend internals;
- reduce misunderstanding and relational friction;
- support ORA Companion modes;
- enrich RAG chunks with reusable emotional and essence tags.

## Position in ORA

The canonical position of ANCOLIE inside ORA is:

```text
USER_INPUT
-> γ.gpl{m=parse}
-> λ.rim{d=2}
-> ANCOLIE{m=emo_index}
-> σ.son{e=adapt}
-> α.aur{r=contextual}
-> π.pri{s=1}
-> ε.eco{c=low}
-> ω.com{out=human}
-> τ.hal{t=lite}
```

ANCOLIE sits between request understanding, human adaptation, memory shaping,
and final response delivery.

## Essences

ANCOLIE primarily coordinates these ORA essences:

| Essence | Function in ANCOLIE |
| --- | --- |
| `λ.rim` | Clarify the signal and reduce ambiguity. |
| `π.pri` | Validate emotional coherence and safety. |
| `ε.eco` | Compress affective context and reduce token cost. |
| `σ.son` | Adapt business and human tone. |
| `α.aur` | Balance risk, value, and strategic impact. |
| `τ.hal` | Trace uncertainty when confidence is limited. |
| `μ.me` | Cut unproductive emotional loops. |
| `γ.gpl` | Translate human input into backend structure. |
| `χ.cre` | Support roadmap or ideation outputs when ambition dominates. |
| `ω.com` | Deliver clean frontend output. |

## Emotional Alphabet

ANCOLIE recognizes the following primary compact states:

- `joy`
- `focus`
- `urgency`
- `fear`
- `frustr`
- `trust`
- `doubt`
- `fatigue`
- `pride`
- `calm`
- `anger`
- `curiosity`
- `vision`
- `control`
- `security`
- `clarity`

The implementation can emit one to three dominant states inside the same
signature, ordered by strength.

## Signature Contract

The canonical ANCOLIE signature is:

```text
ANCOLIE_SIG{
  emo="";
  intensity=0.00;
  confidence=0.00;
  need="";
  friction="";
  route="";
  tone="";
  memory="";
  risk="";
  action="";
}
```

## Inputs

The deterministic implementation accepts:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `text` | string | conditional | Main textual signal. |
| `input` | string | conditional | Alias for `text`. |
| `utterance` | string | conditional | Alias for `text`. |
| `input_type` | string | no | `text`, `voice`, or `hybrid`. |
| `mode` | string | no | `LIGHT`, `FULL`, or `TRACE`. |
| `user_negative_intent` | boolean | no | Force de-escalation route. |
| `user_requests_deep` | boolean | no | Hints deeper companion behavior. |
| `allow_storage` | boolean | no | Allow selective long-memory suggestion. |
| `voice_features` | object | conditional | Optional vocal metrics. |

At least one textual field or `voice_features` must be present.

## Voice Features

When voice data is available, ANCOLIE reads:

| Field | Type | Meaning |
| --- | --- | --- |
| `loudness` | number | Relative amplitude, normalized `0.0..1.0`. |
| `speech_rate` | number | Relative speaking speed. |
| `pause_ratio` | number | Fraction of pauses in the sample. |
| `pitch_variation` | number | Vocal variation. |
| `tension` | number | Estimated vocal tension. |

Vocal routing follows a simplified policy:

- `SOFT`: low escalation, normal routing;
- `NEUTRAL`: standard priority;
- `FORTE`: elevated priority and fast-path handling.

## Modes

ANCOLIE exposes three deterministic modes:

### LIGHT

```text
ANCOLIE_MODE_LIGHT{
  detect=basic;
  store=false;
  route=σ.son+ε.eco;
}
```

### FULL

```text
ANCOLIE_MODE_FULL{
  detect=deep;
  store=selective;
  route=λ.rim+σ.son+α.aur+π.pri;
}
```

### TRACE

```text
ANCOLIE_MODE_TRACE{
  detect=deep;
  output=signature_visible;
  audit=τ.hal;
}
```

## Detection Rules

Text detection uses:

- imperative verbs;
- punctuation intensity;
- repeated correction cues;
- lexical intensity;
- explicit frustration;
- implicit needs;
- strategy or action orientation.

Voice detection uses:

- loudness;
- speech rate;
- pause ratio;
- pitch variation;
- tension.

## Priority Rules

The implementation follows these deterministic route priorities:

1. `user_negative_intent=true` -> `stop_or_deescalate`
2. `frustration>0.65` -> `λ.rim+π.pri+ε.eco+μ.me`
3. `urgency>0.70` -> `ε.eco+μ.me+ω.com`
4. `doubt>0.60` -> `λ.rim+π.pri+τ.hal`
5. `vision>0.60` -> `α.aur+χ.cre+ω.com`
6. `trust>0.70` -> maintain tone

This is intentionally deterministic and not probabilistic.

## Standard Route Bundles

| Dominant state | Route | Tone | Output bias |
| --- | --- | --- | --- |
| `urgency` | `ε.eco+μ.me+ω.com` | `direct` | `next_action` |
| `frustr` | `λ.rim+π.pri+ε.eco+μ.me` | `calme+direct` | `corrective_response` |
| `vision` | `α.aur+χ.cre+ω.com` | `strategique` | `roadmap` |
| `doubt` | `λ.rim+π.pri+τ.hal` | `rassurant+factuel` | `verified_answer` |

The implementation also refines the route for:

- `focus`, `clarity`, `control` -> actionable structure;
- `security`, `fear` -> safeguards and explicit limits;
- `curiosity` -> examples and guided expansion.

## Memory Policy

ANCOLIE writes only compressed and durable patterns.

### Short Memory

```text
ANCOLIE_SHORT_MEM{
  session_state="";
  last_emotion="";
  current_need="";
  response_adjustment="";
}
```

### Long Memory

```text
ANCOLIE_LONG_MEM{
  stable_preference="";
  repeated_pattern="";
  communication_style="";
  avoid_pattern="";
}
```

Selective storage is recommended only when:

- confidence is high enough;
- a reusable preference is explicit;
- mode is not `LIGHT`;
- memory directive is not `session_only`.

ANCOLIE must never store:

- useless transient emotions;
- intimate details not needed for the task;
- unverified interpretation;
- definitive psychological judgment.

## RAG Integration

ANCOLIE can derive compact document metadata:

```text
RAG_CHUNK_META{
  doc_id="";
  essence_tags=[];
  emo_tags=[];
  use_case="";
  risk="";
  retrieval_priority="";
}
```

The helper `build_rag_chunk_meta()` converts a deterministic ANCOLIE result into
this metadata shape.

## ORA Companion Integration

ANCOLIE maps naturally to the three Companion modes:

| Companion mode | Canonical route | Usage |
| --- | --- | --- |
| `FAST` | `λ.rim+ε.eco+μ.me` | Short, direct, low-overhead handling. |
| `DEEP` | `λ.rim+π.pri+α.aur+σ.son+τ.hal` | Strategic, verified, or reflective handling. |
| `EMO` | `ANCOLIE+σ.son+π.pri+ω.com` | High relational or affective load. |

The implementation derives `companion_mode` from signal intensity, confidence,
and explicit mode selection.

## Frontend Policy

By default ANCOLIE stays backend-only. Frontend is allowed to expose:

- clear response;
- tone adjustment;
- respectful reformulation;
- useful next action.

Frontend must not expose by default:

- explicit emotional diagnosis;
- invasive psychological reading;
- overinterpretation;
- full internal signature dump.

## Safety and Governance

ANCOLIE is governed by `PRIMORDIA`.

Forbidden behavior:

- overinterpretation;
- medical diagnosis;
- manipulation;
- emotional exploitation.

Required behavior:

- uncertainty when confidence is low;
- compressed storage only when justified;
- no false claim about the real internal state of the user.

## Thresholds

Recommended thresholds implemented in this repository:

```text
ANCOLIE_THRESHOLDS{
  detection_min=0.45;
  store_min=0.75;
  route_adjust_min=0.55;
  trace_min=0.70;
  uncertainty_if_confidence_below=0.50;
}
```

## Lightweight Log Format

The helper `build_ancolie_log()` emits:

```text
ANCOLIE_LOG{
  timestamp="";
  input_type="text|voice";
  detected_emo="";
  confidence=0.00;
  route="";
  action="";
  stored=false;
}
```

## Minimal Example

```python
from gpv2_neroflux import AncolieIndexer

indexer = AncolieIndexer()

result = indexer.analyze({
    "text": "Je veux que ce soit concret, arrete les trucs vagues.",
    "mode": "FULL",
})

print(result["signature"]["emo"])
print(result["signature"]["route"])
print(result["signature"]["action"])
```

## Example Result Shape

For the deeper corrective example:

```text
ANCOLIE_SIG{
  emo="frustr+control+clarity";
  intensity=0.81;
  confidence=0.91;
  need="qualite+profondeur+respect_du_brief";
  friction="output_too_shallow";
  route="λ.rim+π.pri+ε.eco+μ.me+ω.com+τ.hal";
  tone="direct+responsable+precis";
  memory="avoid_shallow_document_generation";
  risk="medium";
  action="produce_deep_structured_content_before_export";
}
```

## Non-Goals

- ANCOLIE is not a therapist.
- It is not a truth engine.
- It is not a medical or psychological diagnostic system.
- It does not replace user-provided intent with speculative affect.

## Final Principle

ANCOLIE must never manipulate. Its job is to:

- clarify;
- adapt;
- protect;
- reduce friction;
- improve understanding.

Its value is not magical emotion reading. Its value is turning human signals
into compact, testable, reusable routing data for ORA.
