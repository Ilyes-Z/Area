# AREA

### Introduction

The goal of this project is to create a service which allow link between multiples API in order to build action reaction couple like IFTTT or Zapier.

This document aim to provide a documentation about our AREA project.

## Usage

First of all, make sure you have [docker](https://docs.docker.com/get-docker/) with [Idocker-compose](https://docs.docker.com/compose/install/) (version 3) installed on your computer.

When it's done you'll have to define the address where you'll want to find your own AREA service. To achieve this goal you'll have to open a terminal and define `AREA_HOST` env variable.<u>Unix example :</u> `export AREA_HOST=example.test` or `export AREA_HOST=localhost` <u>N.B. :</u> Please keep in mind that some functionalities can be disable for local usage

Then run `docker-compose up --build`, wait a bit and... Congratulation, you've just lauched your own AREA service !

## Architecture

Project architecture looks as follow. If you need more information about architecture :  take a look at devops documentation [here](https://github.com/EpitechIT2020/B-YEP-500-PAR-5-1-area-matthis.cusin/blob/dev/docs/AREA-devops.md) (in French).

![](https://github.com/EpitechIT2020/B-YEP-500-PAR-5-1-area-matthis.cusin/blob/master/archi_2021.png)

## Routes

As described in above section, we use multiple services, accessible using specifics routes. You'll find below links to their respective documentations.

* [Parse](https://parseplatform.org/) routes are reachables at address : `https://$AREA_HOST/parse` ([documentation](https://docs.parseplatform.org/rest/guide/))

* Server routes are reachables at address : `https://$AREA_HOST/` (documentation)

* Trigger routes are reachables at address : `https://$AREA_HOST/` (documentation)

## Other Documentations

You will find more documentation in the following folders (often both in french and english):

* back/reaction
* docs
* front/app
* front/web
