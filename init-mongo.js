db = db.getSiblingDB('test');
db.createCollection("_User");
db.createCollection("_Session");
db.createCollection("_SCHEMA");
db.createCollection("Service");
db.createCollection("Area");

try {
    schema = db.getCollection("_SCHEMA");
    schema.insertMany([
        {
            _id: '_User',
            objectId: 'string',
            updatedAt: 'date',
            createdAt: 'date',
            username: 'string',
            email: 'string',
            emailVerified: 'boolean',
            authData: 'object',
            first_name: 'string',
            last_name: 'string',
            auth_service: 'object',
            _metadata: {
                fields_options: {
                    auth_service: {
                        required: false,
                        defaultValue: {
                            SMS: {
                                connected: true,
                                auth_required: false
                            },
                            Email: {
                                connected: true,
                                auth_required: false
                            }
                        }
                    }
                }
            }
        },
        {
            _id: '_Role',
            objectId: 'string',
            updatedAt: 'date',
            createdAt: 'date',
            name: 'string',
            users: 'relation<_User>',
            roles: 'relation<_Role>'
        },
        {
            _id: 'Service',
            name: 'string',
            logo: 'string',
            auth_parameter: "object",
            color: 'object',
            triggers: 'array',
            reactions: 'array'
        },
        {
            _id: 'Area',
            user_id: 'string',
            services: 'object',
            is_actif: 'boolean',
            trigger: 'object',
            reaction: 'array',
            _metadata: {
                fields_options: {
                    is_actif: {
                        required: false,
                        defaultValue: false
                    }
                }
            }
        },
        {
            _id: '_Session',
            objectId: 'string',
            updatedAt: 'date',
            createdAt: 'date',
            restricted: 'boolean',
            user: '*_User',
            installationId: 'string',
            sessionToken: 'string',
            expiresAt: 'date',
            createdWith: 'object'
        }
    ]);
} catch (err) {
    print(err);
}

try {
    service = db.getCollection("Service");
    service.insertMany([
        {
            _id: 'pXJSDNBC0q',
            name: 'Spotify',
            logo: 'path',
            auth_parameter: {
                url: "https://accounts.spotify.com/authorize?response_type=code&client_id=<clientID>&scope=user-read-private,user-follow-read,user-read-email,playlist-modify-public,playlist-modify-private,user-read-currently-playing,user-follow-modify,user-library-modify&redirect_uri=<hostname>service/spotify/callback&state=<session_token>"
            },
            color: {
                green: "#1D8954",
                white: "#FFFFFF",
                black: "#191414"
            },
            triggers: [
                {
                    name: "Create playlist",
                    id: "spotify-create-playlist",
                    desc: "The creation of a playlist on the user account triggers the reaction",
                    parameters: []
                },
                {
                    name: "Current track",
                    id: "spotify-current-track",
                    desc: "Listening to music defined by the user when creating the AREA triggers the reaction",
                    parameters: [
                        {
                            id: "track-title",
                            name: "Track title",
                            type: "string"
                        },
                        {
                            id: "artists-track",
                            name: "Artists track",
                            type: "string"
                        }
                    ]
                },
                {
                    name: "User follow new artist",
                    id: "spotify-follow-artist",
                    desc: "Following a new artist triggers action",
                    parameters: []
                },
            ],
            reactions: [
                {
                    name: "Add Song",
                    id: "spotify-add-song",
                    desc: "Adds the list of music to a playlist defined when creating the AREA",
                    parameters: [
                        {
                            id: "song-list",
                            name: "Song List",
                            type: "array"
                        },
                        {
                            id: "playlist",
                            name: "Playlist",
                            type: "string",
                            not_required: [
                                "spotify-create-playlist"
                            ]
                        }
                    ]
                },
                {
                    name: "Create Playlist",
                    id: "spotify-create-playlist",
                    desc: "Create a playlist defined during the creation of the AREA",
                    parameters: [
                        {
                            name: "Playlist Name",
                            id: "playlist-name",
                            type: "string"
                        }
                    ]
                },
                {
                    name: "Like Song",
                    id: "spotify-like-song",
                    desc: "Like the list of music defined when creating the AREA",
                    parameters: [
                        {
                            name: "Song Name",
                            id: "song-name",
                            type: "string"
                        }
                    ]
                },
                {
                    name: "Follow Artist",
                    id: "spotify-follow-artist",
                    parameters: [
                        {
                            name: "Artist Name",
                            id: "artist-name",
                            type: "string"
                        }
                    ]
                }
            ]
        },
        {
            _id: 'bIGSDNTH0u',
            name: 'Github',
            logo: 'path',
            auth_parameter: {
                url: "https://github.com/login/oauth/authorize?client_id=<clientID>&scope=repo,user&redirect_uri=https://api.area-revenge.ninja/service/github/callback&state=<session_token>"
            },
            color: {
                white: "#FFFFFF",
                black: "#191414"
            },
            triggers: [
                {
                    name: "Create Repository",
                    id: "github-create-repo",
                    desc: "The creation of a deposit on the user's account triggers the reaction",
                    parameters: []
                },
                {
                    name: "Add Collaborators",
                    id: "github-add-collab",
                    desc: "Adding an employee to a repository defined during the creation of the AREA triggers the reaction",
                    parameters: [
                        {
                            name: "Repository Name",
                            id: 'repo-name',
                            type: "sring"
                        },
                        {
                            name: "Owner Name",
                            id: 'owner-name',
                            type: 'string'
                        },
                    ]
                },
                {
                    name: "New Invitations",
                    id: "github-new-invits",
                    desc: "Sending a new invitation to a repository belonging to the user triggers the reaction",
                    parameters: [
                        {
                            name: "Repository Name",
                            id: 'repo-name',
                            type: "sring"
                        },
                        {
                            name: "Owner Name",
                            id: 'owner-name',
                            type: 'string'
                        },
                    ]
                }
            ],
            reactions: [
                {
                    name: "Add collaborator",
                    id: "github-collaborator",
                    desc: "Adds the list of employees in the repository defined when creating the AREA",
                    parameters: [
                        {
                            name: "Collaborator Name",
                            id: 'collaborator-name',
                            type: "sring"
                        },
                        {
                            name: "Your Username",
                            id: 'your-username',
                            type: 'string'
                        },
                        {
                            name: "Repository name",
                            id: 'repository-name',
                            type: 'string',
                            not_required: [
                                "github-create-repo"
                            ]
                        }
                    ]
                },
                {
                    name: "Create Repository",
                    id: "github-create-repo",
                    desc: "Create a repository with its name defined when creating the AREA",
                    parameters: [
                        {
                            id: "repository-name",
                            name: "Repository name",
                            type: "string",
                        },
                        {
                            id: "description",
                            name: "Description",
                            type: "string"
                        }
                    ]
                },
                {
                    name: "Follow User",
                    id: 'github-follow-user',
                    desc: "Follows a user defined during the creation of the AREA",
                    parameters: [
                        {
                            id: 'user-to-follow',
                            name: 'User To Follow',
                            type: "string"
                        }
                    ]
                }
            ]
        },
        {
            _id: 'PvAPuOIELm',
            name: 'Discord',
            logo: 'path',
            auth_parameter: {
                url: "https://discord.com/api/oauth2/authorize?client_id=<clientID>&redirect_uri=<hostname>service%2Fdiscord%2Fcallback&response_type=code&scope=identify%20email%20connections%20messages.read%20rpc.notifications.read&state=<session_token>"
            },
            color: {
                color: "#7289da"
            },
            triggers: [
                {
                    name: "Discord new server",
                    id: "discord-new-server",
                    desc: "The creation of a server on discord by the connected user triggers the reaction",
                    parameters: []
                }
            ],
            reactions: [
            ]
        },
        {
            _id: 'AreZuOXhdA',
            name: 'Azure',
            logo: 'path',
            auth_parameter: {
                url: "https://login.microsoftonline.com/common/oauth2/v2.0/authorize?response_type=code&client_id=<clientID></clientID>&redirect_uri=<hostname>service%2Fazure%2Fcallback&scope=email+openid+offline_access&state=<session_token>"
            },
            color: {
                color: "#f0ffff"
            },
            triggers: [
                {
                    name: "Outlook incomming action",
                    id: "outlook-incomming-action",
                    parameters: []
                }
            ],
            reactions: [
            ]
        },
        {
            _id: 'BsUIQasnQU',
            name: 'Stackoverflow',
            logo: 'path',
            auth_parameter: {
                url: "https://stackoverflow.com/oauth?client_id=<clientID></clientID>&scope=read_inbox&redirect_uri=https://api.area-revenge.ninja/service/stackoverflow/callback&state=<session_token>"
            },
            color: {
                color: "#ffffff"
            },
            triggers: [
                {
                    name: "Change Name",
                    id: "stackoverflow-change-name",
                    parameters: []
                }
            ],
            reactions: [
            ]
        },
        {
            _id: 'trWdCHTHIu',
            name: 'Twitch',
            logo: 'path',
            auth_parameter: {
                url: "https://id.twitch.tv/oauth2/authorize?client_id=<clientID></clientID>&redirect_uri=<hostname>service/twitch/callback&response_type=code&scope=user:read:email user:edit user:edit:follows user:read:blocked_users user:read:broadcast&state=<session_token>"
            },
            color: {
                white: "#FFFFFF",
                black: "#191414"
            },
            triggers: [
                {
                    name: "Actif stream of user",
                    id: "twitch-stream-actif",
                    desc: "As soon as a streamer defined during the creation of the AREA is online, triggers the reaction",
                    parameters: [
                        {
                            id: "streamer-list",
                            name: "Streamer list",
                            type: "array"
                        }
                    ]
                },
                {
                    name: "Number of follower of user",
                    id: "twitch-follower-user",
                    desc: "As soon as a streamer reaches a level of fans defined during the creation of the AREA, triggers the reaction",
                    parameters: [
                        {
                            id: "streamer-list",
                            name: "Streamer list",
                            type: "array"
                        },
                        {
                            id: "modulo-number",
                            name: "fan counter",
                            type: "number"
                        }
                    ]
                },
                {
                    name: "Top games",
                    id: "twitch-top-games",
                    desc: "As soon as in the top 30 stream, the title contains a word defined in the creation of AREA, triggers the reaction",
                    parameters: [
                        {
                            id: "title-contain",
                            name: "Title contain",
                            type: "string"
                        }
                    ]
                }
            ],
            reactions: [
                {
                    name: "Follow User",
                    id: "twitch-follow-user",
                    desc: "Follows a user defined during the creation of the AREA",
                    parameters: [
                        {
                          name: "User To Follow",
                          id: 'user-to-follow',
                          type: "string"
                        },
                        {
                            name: 'Your Username',
                            id: 'your-username',
                            type: "string",
                        }
                    ]
                }
            ]
        },
        {
            _id: 'meMLaAOiMl',
            name: 'Email',
            logo: 'path',
            auth_parameter: {},
            color: {
                blue: "#0000FF"
            },
            triggers: [],
            reactions: [
                {
                    name: "Send email",
                    id: "email-send",
                    desc: "Sends an email with the message and and the recipient defined when creating the AREA",
                    parameters: [
                        {
                            id: "message",
                            name: "Message",
                            type: "string",
                        },
                        {
                            id: "receiver",
                            name: "Receiver",
                            type: "string"
                        }
                    ]
                }
            ]
        },
        {
            _id: 'AzsemFGsmP',
            name: 'SMS',
            logo: 'path',
            auth_parameter: {},
            color: {
                blue: "#0000FF"
            },
            triggers: [],
            reactions: [
                {
                    name: 'Send Sms',
                    id: 'sms-send',
                    desc: "Sends a message to the number defined when creating the AREA",
                    parameters: [
                        {
                            id: 'message',
                            name: "Message",
                            type: 'string',
                        },
                        {
                            id: 'number',
                            name: "number",
                            type: 'string'
                        }
                    ]
                }
            ]
        }
    ]);
} catch (err) {
    print(err);
}

try {
    user = db.getCollection("_User");
    user.insertMany([
        {
            _id: 'ULYfqkWJzo',
            username: 'Drijux',
            _hashed_password: '$2b$10$erhAa2YPFSTZMhEL0wi95.XHS4.H/Zb/CROcnOITEwXBPQuXOWJVS',
            _wperm: [
                'ULYfqkWJzo'
            ],
            _rperm: [
                '*',
                'ULYfqkWJzo'
            ],
            _acl: {
                ULYfqkWJzo: {
                    w: true,
                    r: true
                },
                '*': {
                    r: true
                }
            },
            auth_service: {
                SMS: {
                    connected: true,
                    auth_required: false
                },
                Email: {
                    connected: true,
                    auth_required: false
                }
            },
            _created_at: ISODate('2021-02-06T01:33:36.641Z'),
            _updated_at: ISODate('2021-02-06T01:33:36.641Z')
        }
    ]);
} catch (err) {
    print(err);
}


try {
    session = db.getCollection("_Session");
    session.insertMany([
        {
            _id: 'g5SyyvNfrn',
            _session_token: 'r:5997f258bb022c2e92c4518c3f7fb378',
            _p_user: '_User$ULYfqkWJzo',
            createdWith: {
                action: 'login',
                authProvider: 'password'
            },
            restricted: false,
            expiresAt: ISODate('2022-02-15T11:02:22.963Z'),
            _created_at: ISODate('2021-02-15T11:02:22.964Z'),
            _updated_at: ISODate('2021-02-15T11:02:22.964Z')
        }
    ]);
} catch (err) {
    print(err);
}