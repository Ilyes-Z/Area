eviter# AREA 2021 - Gitflow

## Introduction

The purpose of this document is to define clear rules regarding the use of <u>Github</u> as part of the AREA project.

The AREA is a project to create a service to link various APIs in an action-reaction context such as [IFTTT](https://ifttt.com/) or [Zapier](https://zapier.com/). 

## The Branches

This section deals with branch naming conventions, pull request policy and issue policy.

### Organization

The organization of the different branches follows the following model.

emermaid
graph LR
subgraph master
    A --> B --> C
end
subgraph dev
    E --> F --> G --> H
end
subgraph functionality 1
    I --> J --> K --> F
end
B --> E
E --> I
G --> C
```

A demonstrable production version can be found on the **master** branch.

Consequently, the **dev** branch serves as a buffer between the branches used to develop new features (see [naming convention](Naming) below).

> Documentation

### Naming

The branches used for feature development must follow the following model.

> <large concerned party>/<functionality>

examples :<u>examples :</u>. 

front/login

`devops/init`

**N.B. :** It is possible to add sub-categories in suffix (ex: front/page/login)

### Pull Requests (PR)

Any functionality developed must be the subject of a PR in order to be integrated within the **dev** branch.

The author of the PR is required to assign a reviewer to any person impacted in any way by the PR as well as the project manager.

The author of the PR is required to merge his PR by performing a "squash" (*squash and merge* on github) then to delete the corresponding branch (except the **dev** branch).

> Attention : Any PR not validated and without any remark for at least 72h will be considered as accepted.

> Caution: No merge from dev to master must be done without the project manager's approval.

### The Issues

If a bug is found, you can open a Github issue and assign the person who added the feature previously. If you are not sure who to assign, feel free to ask.

Then fill in a message describing the bug you have identified. Be as precise as possible.

> Caution: Watch the exits you open, you may be contacted again by the person you have assigned.

> Caution: Any issue left unanswered (not accepted) for more than 48 hours must be reported to the project manager. 

> Warning: Any issue that has not been answered by its creator for more than 72 hours will be considered abandoned and will be classified as not being pursued.

## The Commits

Every commit consists of at least one line that fits the form. It is written in English.
A commit takes the form :

> [<Action>] <Description>

examples:<u>examples:</u>

[ADD] Login page

[UPDATE] Config traefik`

> Caution: Try to limit the length of your commits. In this respect, think about committing regularly. The maximum length of a commit is left to the discretion of the different project participants.
