# AREA-devops

## Introduction

This document is a documentation about the devops part of the AREA project.

## Use

To launch the complete infrastructure, make sure you have docker and docker-composer installed on your machine and running.

That being said, open a terminal and execute the following commands:

`export AREA_HOST=example.test`

*Exports an environment variable containing the address on which you want to access the different elements (example: localhost for local use)*.

`docker-compose up --build`

*Wait a little bit and... you're there. You've just deployed your own AREA on your machine.*

## The architecture

### Explanatory diagram

![ <Insert image here>]()

### Description

#### Web app

###### Roads

Internal access :</u> Internal access :</u> 

* address: `front`, port: `80`.

External access :<u> External access :</u>

* address: `https://www.${AREA_HOST}` 

* address: `https://${AREA_HOST}`

* address: `https://${AREA_HOST}:8081`

###### Framework / tool

* React - Js + Material UI

###### Description

Container to serve the web page for the present project (AREA)

#### Mobile App

###### Roads

None, the application is installed separately

###### Framework / tool

#### Flutter

###### Description

Mobile application for this project (AREA)

#### Parse

###### Roads

Internal access :</u> Internal access :</u> 

* address: `parse-server`, port: `1337`.

External access :<u> External access :</u>

* address: `https://api.${AREA_HOST}/parse`

* address: `https://${AREA_HOST}:8080/parse`.

###### Framework / tool

Parse Platform

###### Description

Backend for application.

#### Middleware

###### Roads

Internal access :</u> Internal access :</u>

* address: `middleware`, port: `6060`.

External access :<u> External access :</u>

* address: `https://api.${AREA_HOST}/`

* address: `https://${AREA_HOST}:8080/parse`.

###### Framework / tool

Python - Django

###### Description

Serves to control the information that circulates through Parse. It also acts as a gateway between the fronts and the rest of the infrastructure.

#### Poll

###### Roads

Internal access :</u> Internal access :</u>

- address: `poll`, port: `6060`.

External access :<u> External access :</u>

None, it is only accessible from the inside.

###### Framework / tool

Go

###### Description

Allows the implementation of custom services or services requiring regular polling such as rss feeds or even certain actions related to the weather.

#### Trigger

###### Roads

Internal access :</u> Internal access :</u>

* address: `trigger`, port: `6060`.

External access :<u> External access :</u>

* address: `https://api.${AREA_HOST}/hooks`

* address: `https://${AREA_HOST}:8080/hooks`

###### Framework / tool

Python - Django

###### Description

Centralize requests from the polling server or external services (webhooks). It applies a first treatment to the requests before.

#### Reaction

###### Roads

Internal access :</u> Internal access :</u>

* address: `reaction`, port: `6060`.

External access :<u> External access :</u>

None, this container is not intended to make outgoing requests.

###### Framework / tool

Python - Django

###### Description

Server with vocation to react according to the captured requests 

#### Mail server (SMTP - outgoing)

###### Roads

Internal access :</u> Internal access :</u>

* address: `smtp-server`, port: `25`.

External access :<u> External access :</u>

None

###### Framework / tool

smtp by namshi

###### Description

Simple smtp mail server
