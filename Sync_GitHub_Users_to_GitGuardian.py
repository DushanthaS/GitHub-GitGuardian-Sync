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


list_of_managers = ["M1@YOURORG.COM", "M2@YOURORG.COM", "M3@YOURORG.COM"]


def sync_gh_users_to_git_guardian(org, gh_token, gg_token):
    github_users = GetGitUsers(org, gh_token)
    for user in github_users.iterator():
        try:
            github_user_email = user["node"]["samlIdentity"]["nameId"]
            github_user_name = user["node"]["user"]["login"]
            print("user: {},email: {}".format(github_user_name, github_user_email))
            github_teams = GetGithubTeams(org, gh_token, github_user_name).iterator()
            gg_invite_response = gg_invite(gg_token, github_user_email)
            if gg_invite_response.status_code == 201:
                invite = gg_invite_response.json()
                invite_user_to_teams(gg_token, invite["id"], github_teams, github_user_name)
            elif gg_invite_response.status_code == 200 and github_user_email not in list_of_managers:
                gg_member_id = get_gg_member_id(gg_token, github_user_email)[0]["id"]
                update_member = gg_update_member(gg_token, gg_member_id)
                add_user_to_teams(gg_token, gg_member_id, github_teams, github_user_name)
            elif gg_invite_response.status_code == 409:
                logger.warning("Data Conflict")
            else:
                logger.exception("Error occurred, status: {}".format(gg_invite_response.status_code))

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