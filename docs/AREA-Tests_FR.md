# AREA-Tests

## Introduction

Ce document a pour objectif de définir un cadre commun concernant les tests à réaliser pour sanctionner l'état global du projet au moment d'une pull request.

## Pourquoi des tests ?

S'assurer que tout fonctionne de manière nominale avant de fusionner afin de limiter les effets de bords.

### Définitions

Nous considérerons deux types de tests :

- Les tests de **fonctionnalité** qui ont pour but de démontrer que les éléments ajoutés par la PR ont un comportement nominal qui coïncide avec les normes et documentations préalablement établies

- Les tests d'**intégration**, réalisés avant toute fusion de la branche `dev` au sein de la branche `master`, doivent attester de la bonne intégration de l'ensemble des fonctionnalités implémentées ensemble.

## Réalisation

Cette section détaille le protocole de réalisation des différents tests pré-cités.

### Tests de fonctionnalité

#### Quand ?

Les tests de fonctionnalité doivent être réalisé lors de chaque PR.

#### Qui ?

Les tests de fonctionnalités sont définis en amont par les auteurs de la PR.

#### Comment ?

Les tests de fonctionnalité peuvent-être automatiques ou manuels. Pour être considéré comme valides il doivent être réalisés également par une personne extérieure au sujet dans le cadre de la review de la PR. 

Si un  problème est rencontré lors du protocole, il doit-être mentionné sur [airtable](https://airtable.com/tblqinzbZM3pjJy9v/viwYsUlh9xbmyZZlY?blocks=hide).

### Test d'intégration

#### Quand ?

Avant de fusionner la branche `dev` au sein de la branche `master` .

#### Qui ?

Il est défini à partir du cahier des charges, incarné dans le cas de l'AREA par le [sujet](https://intra.epitech.eu/module/2020/B-YEP-500/PAR-5-1/acti-440983/project/file/B-DEV-510_area.pdf).

#### Comment ?

Les tests d'intégration peuvent-être automatiques (exemple : selenium) ou manuels. Ils doivent être réalisé par au moins 2 membres du projets quels qu'ils soient pour être considérés comme valides.

Si un problème est rencontré lors du protocole, il doit-être mentionné sur [airtable](https://airtable.com/tblqinzbZM3pjJy9v/viwYsUlh9xbmyZZlY?blocks=hide).

## Quelle trace trace ?

Une entrée au sur la table test de airtable sous la forme suivante

| Nom                      | Type de test   | Description de ce qui a été réalisé                                                                      | fichier de log (facultatif) | Testeurs       | Date       |
| ------------------------ | -------------- | -------------------------------------------------------------------------------------------------------- | --------------------------- | -------------- | ---------- |
| Authentification Spotify | fonctionnalité | connexion, récupération du token. A noter que l'url de callback ne marche pas si la page n'est pas https | <Fichier de log TU >        | Jules, Matthis | 15/02/2021 |

## Lexique

* **PR** : Pull Request

* **TU**: Test Unitaire
