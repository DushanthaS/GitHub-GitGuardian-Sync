import os
import datetime
from loguru import logger
from GitGuardian_API.gitGuardian_users_teams import (
    get_gg_member_id,
    get_gg_team_id,
    gg_invite,
    gg_invite_teams,
    add_to_teams,
    gg_update_member,
)
from Github_GQL.github_users_and_teams_gql import GetGitUsers, GetGithubTeams

ORGANIZATION = "AcostaEnterprise"
GITHUB_TOKEN = os.environ["GithubToken"]
GITGUARDIAN_TOKEN = os.environ["GitguardianToken"]

now = datetime.datetime.now()
date_time = now.strftime("%m-%d-%Y-%H-%M")
logger.add("{}_gitGuardian-{}.log".format(ORGANIZATION, date_time), format="{time} : {level} : {message}")


def sync_gh_users_to_git_guardian(org, gh_token, gg_token):
    github_users = GetGitUsers(org, gh_token)
    for user in github_users.iterator():
        try:
            github_user_email = user["node"]["samlIdentity"]["nameId"]
            github_user_name = user["node"]["user"]["login"]
            # github_user_email = "test333@test.com"
            # github_user_name = "DushanthaS"
            github_teams = GetGithubTeams(org, gh_token, github_user_name).iterator()
            gg_invite_response = gg_invite(gg_token, github_user_email)
            if gg_invite_response.status_code == 201:
                invite = gg_invite_response.json()
                invite_user_to_teams(gg_token, invite["id"], github_teams, github_user_name)
            elif gg_invite_response.status_code == 200:
                gg_member_id = get_gg_member_id(gg_token, github_user_email)[0]["id"]
                update_member = gg_update_member(gg_token, gg_member_id)
                add_user_to_teams(gg_token, gg_member_id, github_teams, github_user_name)
            elif gg_invite_response.status_code == 409:
                logger.warning("Data Conflict")
            else:
                logger.exception("Error occurred")

        except Exception as e:
            logger.exception("Error occurred: {}".format(e))


def invite_user_to_teams(gg_token, invite_id, github_teams, github_user_name):
    for github_team in github_teams:
        gitguardian_team_id = get_gg_team_id(gg_token, github_team)[0]["id"]
        invite_response = gg_invite_teams(gg_token, gitguardian_team_id, invite_id)
        logger.info("Invited GitHub user {}  to gitGuardian team : {}".format(github_user_name, invite_response))

def add_user_to_teams(gg_token, member_id, github_teams, github_user_name):
    for github_team in github_teams:
        gitguardian_team_id = get_gg_team_id(gg_token, github_team)[0]["id"]
        add_member_response = add_to_teams(gg_token, gitguardian_team_id, member_id)
        logger.info("added the GitHub user {}  to gitGuardian team : {}".format(github_user_name, add_member_response))

sync_gh_users_to_git_guardian(ORGANIZATION, GITHUB_TOKEN, GITGUARDIAN_TOKEN)