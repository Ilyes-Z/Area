# AREA-Tests

## Introduction

The purpose of this document is to define a common framework concerning the tests to be performed to sanction the overall status of the project at the time of a pull request.

## Why testing?

To ensure that everything works nominally before merging in order to limit edge effects.

## Definitions

We will consider two types of tests:

- Functionality** tests, which aim to demonstrate that the elements added by the RP have a nominal behaviour that coincides with the previously established norms and documentation.

- Integration** tests, carried out before any merger of the `dev` branch into the `master` branch, must attest to the proper integration of all the functionalities implemented together.

## Implementation

This section details the protocol for carrying out the various tests mentioned above.

### Functionality tests

#### When?

Functionality tests must be performed at each PR.

#### Who?

Functionality tests are defined upstream by the authors of the PR.

#### How?

Functionality tests can be automatic or manual. In order to be considered valid they must also be carried out by a person outside the subject within the framework of the RP review. 

If a problem is encountered during the protocol, it should be mentioned on [airtable](https://airtable.com/tblqinzbZM3pjJy9v/viwYsUlh9xbmyZZlY?blocks=hide).

### Integration test

#### When?

Before merging the `dev` branch into the `master` branch.

#### Who?

It is defined from the specifications, embodied in the case of the AREA by the [subject](https://intra.epitech.eu/module/2020/B-YEP-500/PAR-5-1/acti-440983/project/file/B-DEV-510_area.pdf).

#### How ?

Integration tests can be automatic (example : selenium) or manual. They must be performed by at least 2 members of the project, whoever they are, to be considered valid.

If a problem is encountered during the protocol, it must be mentioned on [airtable](https://airtable.com/tblqinzbZM3pjJy9v/viwYsUlh9xbmyZZlY?blocks=hide).

## What trace?

An entry on the airtable test table in the following form

| Name | Type of test | Description of what was done | Log file (optional) | Testers | Date |
| ------------------------ | -------------- | -------------------------------------------------------------------------------------------------------- | --------------------------- | -------------- | ---------- |
| Spotify authentication | functionality | login, token retrieval. Note that the callback url doesn't work if the page is not https | <TU log file > | Jules, Matthis | 15/02/2021 |

## Lexicon

* **PR**: Pull Request

* **UT**: Unit Test
