# WHITE PAPER - ORA CORE NEROFLUX

Version 1.0 - Avril 2026
Repository: `TwinsProductionAI/ora-core-neroflux`
Status: public technical white paper

## Resume executif

Neroflux est un module de regulation deterministe pour ORA Core OS. Il aide un orchestrateur a choisir une route de traitement, une cadence, un niveau de verification et une limite de fanout selon le contexte de la demande.

Le module ne genere pas la reponse finale. Il produit une recommandation de routage lisible par machine afin de reduire les activations inutiles, les boucles, les couts et les derives de contexte.

## Probleme vise

Un systeme LLM modulaire peut devenir instable lorsque trop de modules sont actives, lorsque le retrieval interroge trop de sources, ou lorsqu'une demande risquee est traitee sans verification suffisante. Neroflux fournit une couche simple de regulation pour limiter ces problemes.

## Fonctionnement

Neroflux recoit un etat structure contenant des signaux comme l'intention, la densite de contexte, l'urgence, le niveau de risque, la sensibilite client et le besoin de verification.

Il retourne notamment:

- une route dominante;
- une cadence de traitement;
- des poids de modules;
- des actions de stabilisation;
- une trace compacte.

## Integration

Dans ORA Core RAG, Neroflux peut reduire le `top_k`, limiter le fanout et exiger une verification lorsque le risque augmente.

Dans ORA Core Runtime, il peut servir de module testable pour comparer les decisions de routage entre versions.

Avec HGOV et H-NERONS, il ne remplace pas la gouvernance. Il signale simplement quand ces modules doivent etre priorises.

## Limites

Neroflux ne garantit pas la verite finale et ne remplace pas les politiques de securite. Sa qualite depend des signaux d'entree, des ponderations et des tests de regression.

## Roadmap

1. Stabiliser les schemas d'entree et de sortie.
2. Ajouter des exemples publics.
3. Ajouter des tests de regression.
4. Connecter au RAG Governor.
5. Mesurer l'impact sur tokens, latence et coherence.

## Conclusion

Neroflux est une couche de controle de flux pour ORA Core OS. Sa valeur vient de sa capacite a rendre les decisions de routage plus previsibles, plus sobres et plus auditables.
