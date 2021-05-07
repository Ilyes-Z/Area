# AREA - Architecture de données

## Introduction

Ce document décrit la forme sous laquelle sont stockées les données au sein de la base de données à l'aide du serveur Parse.

## Forme des données

Les services sont sauvegardées sous la formes d'objets services dont voici un exemple :

```json
{
    "spotify": {
        "name": "Spotify",
        "auth-parameter": {
            "url": "https://www.spotify.com"
        },
        "logo": "path",
        "color": {
            "green": "#1DB954",
            "white": "#FFFFFF",
            "black": "#191414"
        },
        "triggers": {
            "new-playlist": {
                "name": "Création d'une playlist",
                "parameters": {}
            },
            "new-song-in-playlist": {
                "name": "Ajout d'un son dans une playlist",
                "parameters": {
                    "playlist": "string"
                }
            }
        },
        "reactions": {
            "add-song-to-playlist": {
                "name": "Ajouter un son à une playlist",
                "parameters": {
                    "playlist-name": "string",
                    "song-list": "array"
                }
            }
        }
    
    }
}
```

------

Les couples action-réaction (AREAs) prennent quant à eux la forme suivante :

```json
[
    {
        'folder': 'folder name',
        'isOn': true,
        'trigger': {
            'service': 'spotify',
            'trigger': 'new-playlist',
            'parameters': {},
     },
    'reactions': [
        {
            'service': 'spotify',
            'reaction': 'add-song-to-playlist',
            'parameters': {
                'playlist': 'playlist name',
                'song-list': [
                    'first song',
                    'second song'
                ],
            },
        }
    ]
}
]
```