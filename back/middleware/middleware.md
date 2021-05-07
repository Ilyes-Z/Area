
# AREA API

__Description__:

This documentation is in order to indicate the route that we can found in middleware API.

## Indices

* [Area Routes](#area-routes)

  * [GET User area LIst](#1-get-user-area-list)
  * [POST create AREA Github](#2-post-create-area-github)
  * [POST create AREA Spotify](#3-post-create-area-spotify)
  * [PUT Update AREA](#4-put-update-area)
  * [Post create AREA Discord](#5-post-create-area-discord)

* [Auth Routes](#auth-routes)

  * [Delete user](#1-delete-user)
  * [Failed Login User](#2-failed-login-user)
  * [Login User](#3-login-user)
  * [Register User](#4-register-user)
  * [Register user with same credentials](#5-register-user-with-same-credentials)

* [Services Routes](#services-routes)

  * [GET Service Github](#1-get-service-github)
  * [GET Service Spotify](#2-get-service-spotify)
  * [GET Service error](#3-get-service-error)
  * [GET Service list](#4-get-service-list)


--------


## Area Routes



### 1. GET User area LIst


__Description__:

This route return AREA List given in url parameters.

__Test__:
* Route return status code 200
* Route return valid body
* Route return valid information about Spotify/Github AREA


***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/area
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***More example Requests/Responses:***


##### I. Example Request: User area LIst


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Authorization | Bearer r:5997f258bb022c2e92c4518c3f7fb378 |  |



##### I. Example Response: User area LIst
```js
[
    {
        "objectId": "tzlezZB4dk",
        "trigger": "spotify-create-playlist",
        "reactions": [
            "spotify-add-song"
        ]
    },
    {
        "objectId": "GZCkUV6Zqw",
        "trigger": "github-create-repo",
        "reactions": [
            "github-collaborator"
        ]
    }
]
```


***Status Code:*** 200

<br>



### 2. POST create AREA Github


This route is for create AREA in our backend with Github service.


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: https://api.localhost/area/
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "services": {
        "trigger": "bIGSDNTH0u",
        "reaction": "bIGSDNTH0u"
    },
    "trigger": {
        "id": "github-create-repo"
    },
    "reaction": {
        "id": "github-collaborator",
        "Song List": [
            "Basilarc",
            "UltimMilo"
        ]
    }
}
```



### 3. POST create AREA Spotify


This route is for create AREA in our backend.


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: https://api.localhost/area/
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "services": {
        "trigger": "pXJSDNBC0q",
        "reaction": "pXJSDNBC0q"
    },
    "trigger": {
        "id": "spotify-create-playlist"
    },
    "reaction": {
        "id": "spotify-add-song",
        "Song List": [
            "Back in Black",
            "Sweet Home Alabama"
        ]
    }
}
```



### 4. PUT Update AREA


__Description__:

This route update an area.


***Endpoint:***

```bash
Method: PUT
Type: RAW
URL: https://api.localhost/area/z1CKS4HP8T/
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "is_actif": true
}
```



### 5. Post create AREA Discord



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: https://api.localhost/area/
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "services": {
        "trigger": "PvAPuOIELm",
        "reaction": "pXJSDNBC0q"
    },
    "trigger": {
        "id": "discord-new-server"
    },
    "reaction": {
        "id": "spotify-add-song",
        "Song List": [
            "Back in Black",
            "Sweet Home Alabama"
        ]
    }
}
```



## Auth Routes



### 1. Delete user



***Endpoint:***

```bash
Method: DELETE
Type: 
URL: https://api.localhost/auth/delete
```



### 2. Failed Login User


__Description__:

This route is for login user with bad credentials.

__Test__:
* Route return status code 404
* Route return valid body
* Route return information about connection tentative


***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/auth/login
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| username | Drijux |  |
| password | supe |  |



### 3. Login User


__Description__:

This route is for login user.

__Test__:
* Route return status code 200
* Route return valid body
* Route return valid information User connected


***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/auth/login
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| username | Drijux |  |
| password | super |  |



### 4. Register User


__Description__:

This route is for register user with post method and body request.

__Test__:
* Route return status code 201
* Route return valid body
* Route return valid information about user registration


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: https://api.localhost/auth/register
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "email": "client@test.com",
    "username": "client",
    "password": "super"
}
```



### 5. Register user with same credentials


__Description__:

This route is for register user with post method and body request.

__Test__:
* Route return status code 400
* Route return valid body


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: https://api.localhost/auth/register
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
    "email": "client@test.com",
    "username": "client",
    "password": "super"
}
```



## Services Routes
__Route__: GET /service/<str:service_name>/

__Description__:
This route take a service name in his url as string.

__Error__:
* 404: Service not found in database

__Expected__:
Result of this call is return under the from json.



### 1. GET Service Github


__Description__:

This route return information about service given in url parameters.

__Test__:
* Route return status code 200
* Route return valid body
* Route return valid information about Spotify Service



***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/service/github
```



***More example Requests/Responses:***


##### I. Example Request: Service Github



##### I. Example Response: Service Github
```js
{
    "objectId": "bIGSDNTH0u",
    "name": "Github",
    "logo": "path",
    "auth_parameter": {
        "url": "https://github.com/login/oauth/authorize?client_id=f7b2e94083c54e0fe14e&scope=repo,user&state=<session_token>"
    },
    "color": {
        "white": "#FFFFFF",
        "black": "#191414"
    },
    "triggers": [
        {
            "name": "Create repo",
            "id": "github-create-repo",
            "parameters": []
        }
    ],
    "reactions": [
        {
            "name": "Add collaborator",
            "id": "github-collaborator",
            "parameters": [
                {
                    "name": "collaborator List",
                    "type": "array"
                }
            ]
        }
    ]
}
```


***Status Code:*** 200

<br>



### 2. GET Service Spotify


__Description__:

This route return information about service given in url parameters.

__Test__:
* Route return status code 200
* Route return valid body
* Route return valid information about Github Service


***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/service/spotify
```



***More example Requests/Responses:***


##### I. Example Request: Service Spotify



##### I. Example Response: Service Spotify
```js
{
    "objectId": "pXJSDNBC0q",
    "name": "Spotify",
    "logo": "path",
    "auth_parameter": {
        "url": "https://accounts.spotify.com/authorize?response_type=code&client_id=66f7de80cbcd46bb8dfb0e756702feb7&scope=user-read-private,user-read-email&redirect_uri=http://localhost:8083/service/spotify/callback&state=<session_token>"
    },
    "color": {
        "green": "#1D8954",
        "white": "#FFFFFF",
        "black": "#191414"
    },
    "triggers": [
        {
            "name": "Create playlist",
            "id": "spotify-create-playlist",
            "parameters": []
        }
    ],
    "reactions": [
        {
            "name": "Add Song",
            "id": "spotify-add-song",
            "parameters": [
                {
                    "name": "Song List",
                    "type": "array"
                }
            ]
        }
    ]
}
```


***Status Code:*** 200

<br>



### 3. GET Service error


__Description__:

This route have to return an error on service not implemented in backend.

__Tests__:
* Route return status code 404 not found


***Endpoint:***

```bash
Method: GET
Type: 
URL: https://api.localhost/service/doest_exist/
```



***More example Requests/Responses:***


##### I. Example Request: Exemple Error



##### I. Example Response: Exemple Error
```js
Service not found
```


***Status Code:*** 404

<br>



### 4. GET Service list


__Description__:

This route return information about service list.
If user token is given in Header as Bearer token, this route return list of service where user is not connected 

__Test__:
* Route return status code 200
* Route return valid body
* Route return valid information about Service


***Endpoint:***

```bash
Method: GET
Type: 
URL: http://api.localhost/services
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| auth | true |  |



---
[Back to top](#area-api)
> Made with &#9829; by [thedevsaddam](https://github.com/thedevsaddam) | Generated at: 2021-03-02 16:39:14 by [docgen](https://github.com/thedevsaddam/docgen)
