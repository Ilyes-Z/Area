# AREA  Reaction

Ce document regroupe toutes les informations relatives aux Réactions sur le projet Area.


## Liste des réactions et leurs parametres

### Ajout d'une playlist à un compte **Spotify**
* Nom de la playlist (type: **String**)

### Ajout de musiques à une playlist **Spotify**
* Liste des musiques à ajouter (type: **Array**)
* Nom de la playlist (type: **String**)

### Ajout d'une musique à la liste de ses titres préférés sur **Spotify**
* Nom de la musique (type: **String**)

### Possibilité de suivre un artiste sur **Spotify**
* Nom de l'artiste (type:**String**)

### Création d'un repo sur **Github**
* Nom du repo (type: **String**)
* Description du repo (type: **String**)

### Ajout d'un collaborateur à un repo **Github**
* Nom du collaborateur (type: **String**)
* Nom du propriétaire du repo (type: **String**)
* Nom du repo (type: **String**)

### Possibilité de suivre un compte sur **Github**
* Nom du compte à suivre (type: **String**)

### Possibilité de s'abonner à une chaine sur **Twitch**
* Nom du compte à suivre (type: **String**)
* Nom du compte voulant suivre (type: **String**)

### Possibilité d'envoyé un **Email**
* Adresse email de destination (type: **String**)
* Message de l'email (type: **String**)

### Possibilité d'envoyé un **Sms**
* Numéro du destinataire (type: **String**)
* Message du sms (type: **String**)



## Dépendance des réactions
Les réactions sont nativement indépendantes, cepandant, deux réactions peuvent être associés à une action:

* La réaction ajout d'une musique à une playlist avec l'action créer une playlist Spotify
*  La réaction ajout d'un collaborateur à un repo avec l'action créer un  repo sur Github

