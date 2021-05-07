# AREA - Data architecture

## Introduction

This document explains which form take datas stored in Parse handled mongo database.

## Form of data

Services are saved as service objects, for example :

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

The action-reaction pairs (AREAs) take the following form:

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
