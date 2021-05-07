# AREA Reaction

This document gathers all the information related to the Reactions on the Area project.


## List of reactions and their parameters

### Adding a playlist to a **Spotify** account
* Name of the playlist (type: **String**)

### Adding music to a playlist **Spotify**
* List of musics to add (type: **Array**)
* Name of the playlist (type: **String**)

### Adding music to your favorite tracks on **Spotify**.
* Name of the music (type: **String**)

### Possibility to follow an artist on **Spotify**.
* Artist name (type:**String**)

### Creating a repo on **Github**
* Name of the repo (type: **String**)
* Description of the repo (type: **String**)

### Adding a collaborator to a repo **Github**
* Name of the collaborator (type: **String**)
* Name of the repo owner (type: **String**)
* Name of the repo (type: **String**)

### Ability to track an account on **Github**
* Name of the account to follow (type: **String**)

### Possibility to subscribe to a channel on **Twitch**.
* Name of the account to follow (type: **String**)
* Name of the account to follow (type: **String**)

### Possibility to send a **Email**.
* Destination email address (type: **String**)
* Message of the email (type: **String**)

### Possibility to send a **Sms**.
* Recipient number (type: **String**)
* Message of the sms (type: **String**)



## Reaction dependency
Reactions are natively independent, however, two reactions can be associated with one action:

* The reaction adding a music to a playlist with the action create a Spotify playlist
* The reaction adding a collaborator to a repo with the action create a repo on Github