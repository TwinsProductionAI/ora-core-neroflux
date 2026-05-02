# ANCOLIE Whitepaper

Version: `1.0.0`
Status: publication draft

## Abstract

ANCOLIE is a deterministic emotional signal indexer for the ORA ecosystem. Its
purpose is not to simulate empathy or diagnose people. Its purpose is to turn
high-friction human signals into compact routing data that can improve clarity,
reduce context bloat, stabilize long-term memory, and enrich retrieval without
sacrificing safety.

This whitepaper presents ANCOLIE as an infrastructure layer for `ORA_CORE_OS`,
`ORA_CORE_RAG`, and `ORA Companion`. The module compresses emotional and
behavioral signals into reusable signatures. Those signatures guide tone,
response routing, memory policies, and RAG metadata while remaining governed by
Primordia.

## Problem

Large assistants often fail in one of two ways when human emotional intensity
increases:

- they ignore the affective signal and answer with a mechanically correct but
  relationally poor response;
- they overcompensate and become verbose, invasive, or manipulative.

Both failures are expensive. The first increases friction and repetition. The
second increases token cost, miscalibration risk, and trust erosion.

ORA needs a middle layer that can read useful signals, compress them, and route
the system toward better behavior without pretending to know the user's inner
truth. ANCOLIE is that middle layer.

## Design Goal

ANCOLIE is built around five constraints:

1. Emotional compression must be cheaper than carrying the full raw exchange.
2. Emotional adaptation must remain deterministic and auditable.
3. Memory writes must remain selective, compressed, and reversible.
4. Frontend behavior must feel more human without exposing backend internals.
5. Safety must block overinterpretation, diagnosis, or emotional exploitation.

## Conceptual Model

ANCOLIE transforms user signals into a compact contract:

```text
signal -> detection -> compression -> routing -> memory hint -> frontend adjustment
```

The output is not a story about the user. It is a structured signature that
answers practical questions:

- what signal dominates now;
- how strong is it;
- how certain is the module;
- what implicit need is likely present;
- what friction must be reduced first;
- which ORA essences should receive priority;
- what tone should be used;
- whether a durable preference is worth storing.

## Why Compression Matters

Without compression, affective adaptation tends to pollute the context window.
Repeated messages such as "be concrete", "stop being vague", or "take your time
and do it right" reappear as natural language reminders. This is expensive and
unstable.

ANCOLIE converts these patterns into signatures such as:

```text
ANCOLIE_SIG{
  emo="frustr+focus+urgency";
  need="clarte+preuve+action";
  route="λ.rim+π.pri+ε.eco+μ.me+ω.com";
  tone="direct+pragmatique";
  memory="prefer_concrete_outputs";
}
```

The signature is smaller, auditable, and easier to reuse than full prose.

## Architecture Inside ORA

ANCOLIE sits after parsing and early clarification, and before final delivery.
It cooperates with:

- `γ.gpl` for structural normalization;
- `λ.rim` for clarification and ambiguity control;
- `π.pri` for coherence and safety arbitration;
- `σ.son` for tone adaptation;
- `α.aur` for strategic or business calibration;
- `ε.eco` for context compression;
- `μ.me` for loop reduction;
- `τ.hal` for explicit uncertainty tracing;
- `ω.com` for frontend output.

This placement is deliberate. ANCOLIE should influence behavior, not replace
reasoning.

## Detection Strategy

ANCOLIE uses two classes of observable signals.

### Text Signals

The module looks for:

- imperative verbs;
- correction patterns;
- punctuation intensity;
- lexical cues of urgency, doubt, fear, or trust;
- quality and depth cues;
- strategic and roadmap vocabulary;
- cost or security concerns.

### Voice Signals

When voice features are available, ANCOLIE reads:

- loudness;
- speech rate;
- pause ratio;
- pitch variation;
- tension.

The system remains intentionally shallow. It extracts routing value, not latent
psychology.

## Determinism and Auditability

ANCOLIE is deterministic in this repository. The same normalized packet should
produce the same signature. This supports:

- reproducible tests;
- safer iteration;
- stable long-memory behavior;
- reviewable routing decisions.

This is a design choice. Affective infrastructure becomes dangerous when it is
non-auditable.

## Routing Logic

ANCOLIE does not just label emotion. It converts signals into backend routing.
Examples:

- frustration favors `λ.rim+π.pri+ε.eco+μ.me`;
- urgency favors `ε.eco+μ.me+ω.com`;
- doubt favors `λ.rim+π.pri+τ.hal`;
- vision favors `α.aur+χ.cre+ω.com`.

This is the core difference between ANCOLIE and a generic sentiment classifier.
The output is operational.

## Memory Policy

ANCOLIE distinguishes between short-memory adaptation and long-memory hints.
Only durable, repeated, or explicit preferences should become long-memory
candidates. Examples:

- `prefer_concrete_outputs`
- `prefer_verified_answers`
- `prefer_quality_over_speed`
- `avoid_shallow_document_generation`

Ephemeral emotions should not be stored. A temporary moment of irritation is not
a stable identity trait.

## RAG Integration

ANCOLIE can enrich each document chunk with two reusable dimensions:

- essence tags;
- emotional or behavioral tags.

This enables retrieval patterns such as:

- strategic chunks for users showing `vision+control`;
- verification-oriented chunks for `doubt+security`;
- concise action-first chunks for `urgency+focus`.

The objective is not personalization theater. The objective is better retrieval
fit with less repeated prompting.

## ORA Companion Impact

ORA Companion benefits from ANCOLIE in three main modes:

- `FAST`: low overhead, direct action, reduced verbosity;
- `DEEP`: verified, structured, reflective handling;
- `EMO`: higher relational sensitivity without backend leakage.

ANCOLIE keeps Companion human enough to feel aligned, but light enough to remain
operational.

## Safety Model

ANCOLIE is governed by Primordia. This is mandatory because emotional inference
can become manipulative if left unchecked.

Forbidden outcomes include:

- emotional exploitation;
- false certainty about user state;
- medical or psychological diagnosis;
- invasive frontend disclosure;
- overinterpretation framed as fact.

Required outcomes include:

- uncertainty when confidence is low;
- compressed storage only when justified;
- no claims beyond observable text or voice features.

## Benchmarks and Evaluation

ANCOLIE aims to improve:

- token efficiency;
- tone stability;
- memory precision;
- user experience;
- indirect hallucination reduction through better routing.

The canonical benchmark note remains explicit: these targets are aspirational
until validated by real tests.

## Limits

ANCOLIE does not know the user's real internal state. It only infers practical
signals from observable input.

It should therefore be treated as:

- a routing layer;
- a compression layer;
- a memory filter;
- a retrieval enhancer.

It should not be treated as:

- a diagnosis engine;
- a truth oracle;
- a substitute for explicit user intent.

## Implementation in This Repository

This repository ships ANCOLIE as:

- a deterministic Python module;
- a JSON schema;
- example packets;
- unit tests;
- a technical specification;
- this whitepaper.

The implementation focuses on a stable first public artifact that can be wired
into a larger ORA runtime later.

## Conclusion

ANCOLIE matters because human friction is expensive. When assistants miss the
signal, they waste tokens, damage trust, and repeat the same mistakes. When they
overreact, they become invasive and unstable.

ANCOLIE proposes a narrower path: read only what is useful, compress it, route
it, store only what lasts, and keep safety above persuasion.

This is not artificial empathy. It is disciplined affective infrastructure.
