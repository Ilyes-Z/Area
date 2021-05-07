from django.views.decorators.http import require_POST
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
import requests
from django.views.decorators.csrf import csrf_exempt
from reaction.parse_utils import get_reaction_data, get_reaction_service, get_token

CREATE_REPO_URL = "https://api.github.com/user/repos"

ADD_COLLAB_URL = "https://api.github.com/repos/{}/{}/collaborators/{}"

FOLLOW_USER_URL = "https://api.github.com/user/following/{}"

def github_parser(request, area_data, reaction_index):
    if area_data["reaction"][reaction_index]["id"] == "github-create-repo":
        create_repo(request, area_data, reaction_index)
    elif area_data["reaction"][reaction_index]["id"] == "github-collaborator":
        add_colab(request, area_data, reaction_index)
    elif area_data["reaction"][reaction_index]["id"] == "github-follow-user":
        follow_user(request, area_data, reaction_index)


def follow_user(request, area_data, reaction_index):

    access_token = get_token("Github", area_data["user_id"])

    following = ""
    params = area_data["reaction"][reaction_index]["parameters"]

    for param in params:
        if 'user-to-follow' in param:
            following = param['user-to-follow']

    resp = requests.put(FOLLOW_USER_URL.format(following),
        headers= {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token {}".format(access_token),
        })
    if resp.status_code > 300:
        raise ValueError("Error when follow the user {}. Error: {}, Code : {}".format(following, resp.text, resp.status_code))
    print("Follow user {}".format(following))


def add_colab(request, area_data, reaction_index):

    collaborator_name = ""
    your_username = ""
    repository_name = ""
    params = area_data["reaction"][reaction_index]["parameters"]
    access_token = get_token("github", area_data["user_id"])

    if request["data"]["data"]["repos"]:
        repository_name = request["data"]["data"]["repos"]
        for param in params:
            if 'collaborator-name' in param:
                collaborator_name = param["collaborator-name"]
            elif 'your-username' in param:
                your_username = param["your-username"]
    else:
        for param in params:
            if 'collaborator-name' in param:
                collaborator_name = param["collaborator-name"]
            elif 'your-username' in param:
                your_username = param["your-username"]
            elif 'repository-name' in param:
                repository_name = param['repository-name']

    resp = requests.put(ADD_COLLAB_URL.format(your_username, repository_name, collaborator_name),
    headers= {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token {}".format(access_token),
        },
    json={"permission": "admin"}
    )

    if resp.status_code != 201:
        raise ValueError('Error when add {} to the repo {}. Error: {}, Code: {}'.format(collaborator_name, repository_name, resp.text, resp.status_code))

def create_repo(request, area_data, reaction_index):
    access_token = get_token("Github", area_data["user_id"])
    params = area_data["reaction"][reaction_index]["parameters"]
    repository_name = ""
    description = ""

    for param in params:
        if 'repository-name' in param:
            repository_name = param['repository-name']
        elif 'description' in param:
            description = param['description']

    print("Create repository {}".format(repository_name))

    resp = requests.post(CREATE_REPO_URL, headers={
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token {}".format(access_token),
    }, json={
        "name": repository_name,
        "description": description,
    })
    if resp.status_code != 201:
        raise ValueError("Error when create repository {}. Error : {}, Code : {}".format(repository_name, resp.text, resp.status_code))
