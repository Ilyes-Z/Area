# AREA-devops

## Introduction

Ce document est une documentation concernant la partie devops du projet AREA.

## Utilisation

Pour lancer l'infrastructure complète, assurez-vous d'avoir docker et docker-compose d'installé sur votre machine et en cours d'exécution.

Ceci étant dit, ouvrez un terminal et exécutez les commandes suivantes :

`export AREA_HOST=example.test`

*Export une variable d'environnement contenant l'adresse sur laquelle vous souhaitez accéder aux différents éléments (exemple : localhost pour une utilisation en local)*

`docker-compose up --build`

*Patienter un petit peu et... vous y êtes. Vous venez de déployer votre propre AREA sur votre machine.*

## L'architecture

### Schéma explicatif

![ <Insérer image ici>]()

### Description

#### App web

###### Routes

<u>Accès interne :</u> 

* adresse : `front`, port : `80`

<u>Accès externe :</u>

* adresse : `https://www.${AREA_HOST}` 

* adresse : `https://${AREA_HOST}`

* adresse : `https://${AREA_HOST}:8081`

###### Framework / outil

* React - Js + Material UI

###### Description

Conteneur ayant pour objectif de servir la page web pour le projet présent (AREA)

#### App Mobile

###### Routes

Aucune, l'application est installée à part

###### Framework / outil

#### Flutter

###### Description

Application mobile pour le présent projet (AREA)

#### Parse

###### Routes

<u>Accès interne :</u> 

* adresse : `parse-server`,  port : `1337`

<u>Accès externe :</u>

* adresse : `https://api.${AREA_HOST}/parse`

* adresse : `https://${AREA_HOST}:8080/parse`

###### Framework / outil

Parse Platform

###### Description

Backend pour application.

#### Middleware

###### Routes

<u>Accès interne :</u>

* adresse : `middleware`, port : `6060`

<u>Accès externe :</u>

* adresse : `https://api.${AREA_HOST}/`

* adresse : `https://${AREA_HOST}:8080/parse`

###### Framework / outil

Python - Django

###### Description

Sert à contrôler les informations qui circulent par Parse. Il fait également office de porte d'entrée entre les fronts et le reste de sinfrastructures

#### Poll

###### Routes

<u>Accès interne :</u>

- adresse : `poll`, port : `6060`

<u>Accès externe :</u>

Aucun, il n'est accessible que de l'intérieur

###### Framework / outil

Go

###### Description

Permet la mise en place de services custom ou demandant un polling régulier tel les flux rss ou encore certaines actions liées à la météo

#### Trigger

###### Routes

<u>Accès interne :</u>

* adresse : `trigger`, port : `6060`

<u>Accès externe :</u>

* adresse : `https://api.${AREA_HOST}/hooks`

* adresse : `https://${AREA_HOST}:8080/hooks`

###### Framework / outil

Python - Django

###### Description

Centraliser les requêtes en provenance du serveur de polling ou de services externe (webhooks). Il applique un premier traitement aux requêtes avant.

#### Réaction

###### Routes

<u>Accès interne :</u>

* adresse : `reaction`, port : `6060`

<u>Accès externe :</u>

Aucun, ce conteneur n'a pas vocation à effectuer des requêtes sortantes

###### Framework / outil

Python - Django

###### Description

Serveur ayant vocation à réagir selon les requêtes captées 

#### Serveur mail (SMTP - sortant)

###### Routes

<u>Accès interne :</u>

* adresse : `smtp-server`, port : `25`

<u>Accès externe :</u>

Aucun

###### Framework / outil

smtp par namshi

###### Description

Serveur mail smtp simple
