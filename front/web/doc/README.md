# Technical documentation

### Introduction

The goal of this documentation is to describe the structure of this project and how to test it.

## Testing

To access the web platform you need to run the docker-compose command like describe in the project readme and open google chrome with this command : `google-chrome --ignore-certificate-errors --user-data-dir=\"%TEMP%\"`.

## Source structure

The src folder is composed by 3 subfolders :

* __components__ : contains all reusable components.

* __scenes__ : contains all the pages of the platform.

* __services__ : contains utility functions call by components and scenes

## Routes

Routes are defined in `src/routes.js` with the structure below :

* __name__ : alias to `path` attribute used by `getPath()` function

* __path__ : path of the route

* __component__ : reference to the scene component to display on the path

* __needAuth__ : boolean that describe if the path need an authentified user

* __authAccess__ : boolean that describe if authentified user can acces a page that does not required to be authentified

* __routes__ : array that contains path subroutes