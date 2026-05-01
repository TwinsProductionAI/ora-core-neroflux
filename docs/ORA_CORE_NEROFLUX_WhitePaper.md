# WHITE PAPER - ORA CORE NEROFLUX

Version 1.1 - Avril 2026
Repository: `TwinsProductionAI/ora-core-neroflux`
Status: public technical white paper

## Resume executif

Neroflux est un module deterministe de regulation pour ORA Core OS. Il aide un orchestrateur a choisir une route de traitement, une cadence, un niveau de verification et une limite de fanout selon le contexte de la demande.

Le module ne genere pas la reponse finale. Il produit une recommandation de routage lisible par machine afin de reduire les activations inutiles, les boucles, les couts et les derives de contexte.

La version 1.1 clarifie le role exact de Neroflux: ce n'est pas un module narratif, ni un module de verite, ni un agent autonome. C'est une couche de decision technique entre l'etat d'une demande et les modules qui doivent etre actives.

## 1. Probleme vise

Un systeme LLM modulaire peut devenir instable lorsque:

- trop de modules sont actives pour une demande simple;
- une demande factuelle est traitee sans verification suffisante;
- une demande creative ignore les limites de coherence;
- le retrieval interroge trop de sources;
- le systeme depense trop de tokens pour un gain faible;
- les changements de version modifient le comportement sans trace.

Neroflux fournit une couche de regulation pour limiter ces problemes. Il ne cherche pas a remplacer les autres modules. Il aide a choisir dans quel ordre et avec quelle intensite ils doivent intervenir.

## 2. Definition

Neroflux est un routeur deterministe. Il recoit un etat structure et retourne une decision de routage.

Entrees possibles:

- intention de la demande;
- densite du contexte;
- niveau de risque;
- urgence;
- besoin de verification;
- sensibilite client;
- risque de permission;
- nombre de modules ou d'agents disponibles;
- budget de tokens ou de latence.

Sorties attendues:

- route dominante;
- cadence de traitement;
- poids des routes ou modules;
- limite de fanout;
- actions de stabilisation;
- trace compacte.

## 3. Architecture logique

```text
Structured request state
  -> normalize signals
  -> score routing pressure
  -> select dominant route
  -> choose processing pace
  -> apply fanout limits
  -> emit routing trace
```

Le resultat doit etre transmis a un orchestrateur, un runtime ou un RAG Governor. Neroflux ne doit pas emettre seul une reponse utilisateur finale.

## 4. Routes de traitement

Neroflux peut orienter le systeme vers plusieurs routes:

### Route simple

Pour les demandes a faible risque qui demandent une reponse directe.

### Route analytique

Pour les demandes qui exigent clarification, decomposition ou raisonnement structure.

### Route creative

Pour les demandes d'ideation, de design, de narration ou de production conceptuelle.

### Route factuelle

Pour les demandes contenant des faits verifiables, des dates, des chiffres, des normes ou des informations susceptibles d'evoluer.

### Route RAG

Pour les demandes qui exigent un contexte source-backed ou un acces a un corpus documentaire.

### Route degradee

Pour les cas ou les donnees sont insuffisantes, contradictoires ou trop sensibles pour permettre une reponse affirmative.

## 5. Cadence de traitement

La cadence indique comment le systeme doit avancer:

- `fast`: faible risque, faible densite;
- `normal`: demande standard;
- `slow`: raisonnement complexe;
- `verified`: claims factuels ou enjeux importants;
- `minimal`: boucle detectee ou faible valeur de continuation;
- `degraded`: manque d'information ou conflit non resolu.

Cette cadence evite deux erreurs: surtraiter une demande simple ou sous-traiter une demande risquee.

## 6. Integration avec ORA Core RAG

Dans ORA Core RAG, Neroflux peut limiter le nombre de sources, reduire `top_k`, exiger une route client valide ou imposer une verification supplementaire.

Exemple logique:

```text
risk_level=high + client_sensitivity=high
  -> reduce top_k
  -> require route gate
  -> require verification
  -> increase audit trace
```

Cette integration permet au RAG de rester local, borne et plus facile a auditer.

## 7. Integration avec HGOV et H-NERONS

Neroflux ne remplace pas la gouvernance epistemique. Lorsque le risque augmente, il doit renforcer le recours aux modules specialises.

Principe d'autorite:

```text
Neroflux routes.
HGOV governs risk.
H-NERONS qualifies factual claims.
The final response is bounded by the selected governance path.
```

Ainsi, Neroflux n'est pas l'arbitre de la verite. Il signale quand les arbitres doivent intervenir.

## 8. Integration avec ORA Core Runtime

Dans le runtime, Neroflux peut devenir un composant testable:

- entree JSON;
- sortie JSON;
- schema public;
- tests unitaires;
- tests de regression;
- comparaison entre versions.

Le determinisme est important. Une meme entree doit produire une decision stable, sauf changement explicite de version ou de configuration.

## 9. Aletheia

Aletheia est le module associe a la reflection post-update. Il compare un etat avant/apres et produit une synthese de changement.

Usages possibles:

- documenter une mise a jour;
- comparer deux versions de module;
- detecter une variation de comportement;
- produire une note de stabilite;
- aider a la decision de release.

Aletheia ne doit pas etre traitee comme une preuve de performance. C'est un outil de documentation comportementale.

## 10. Artefacts recommandes

Une implementation propre de Neroflux devrait produire:

```json
{
  "dominant_route": "verified",
  "pace": "slow",
  "fanout_limit": 3,
  "module_weights": {
    "hgov": 0.9,
    "h_nerons": 0.8,
    "rag": 0.7,
    "creative": 0.2
  },
  "actions": ["require_sources", "bound_assertiveness"],
  "trace": "high risk factual request with source requirement"
}
```

Ce format n'est pas une specification finale. Il sert de reference lisible pour les futures versions.

## 11. Cas d'usage

Neroflux peut etre utilise pour:

- reduire les boucles de raisonnement;
- choisir entre reponse courte, analyse ou verification;
- limiter le nombre de sources interrogees;
- ajuster la densite de sortie;
- prioriser les modules de gouvernance;
- comparer des decisions de routage entre versions;
- optimiser tokens, latence et lisibilite.

## 12. Limites

Neroflux ne garantit pas une meilleure reponse par lui-meme. Sa qualite depend:

- des signaux d'entree;
- des ponderations;
- des tests;
- de la qualite des modules appeles;
- de l'integration avec RAG, HGOV et H-NERONS.

Il ne doit pas etre presente comme une autorite finale. C'est une couche d'aide a la decision.

## 13. Roadmap

1. Stabiliser les schemas d'entree et de sortie.
2. Ajouter des exemples publics pour routes simple, analytique, creative, factuelle et RAG.
3. Ajouter des tests de regression.
4. Connecter Neroflux au RAG Governor.
5. Ajouter une sortie d'audit lisible par humain.
6. Mesurer l'impact sur tokens, latence et coherence.
7. Documenter les changements de ponderation par version.

## Conclusion

Neroflux est une couche de controle de routage pour ORA Core OS. Sa valeur vient de sa capacite a rendre les decisions de traitement plus previsibles, plus sobres et plus auditables.

La version 1.1 fixe son positionnement: Neroflux ne produit pas la reponse, ne verifie pas seul les faits et ne remplace pas la gouvernance. Il selectionne le chemin de traitement le plus defendable selon l'etat de la demande.
