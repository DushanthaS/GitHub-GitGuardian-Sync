from github import Github
from loguru import logger
from GitGuardian_API.gitGuardian_users_teams import (
    get_gg_team_id,
    update_team_perimeter, get_gg_sources
)


def sync_gh_teams_to_git_guardian_perimeter(org, gh_token, gg_token):
    # Log into GitHub
    gh = Github(gh_token)
    # Connect to organization
    gh_org = gh.get_organization(org)
    # Get all teams in org
    teams = gh_org.get_teams()
    gg_sources = get_gg_sources(gg_token)

    for github_team in teams:
        print(f"Team:{github_team.name}")
        gitguardian_team_id = get_gg_team_id(gg_token, github_team.name)[0]["id"]

        repos = github_team.get_repos()
        repo_ids_to_add = []
        repo_names_to_add = []
        for repo in repos:
            print(f"Repo:{repo.name} , Repo_ID: {repo.id}")
            # Check if the repo is in the gg_sources dictionary
            if str(repo.id) in gg_sources:
                repo_id = gg_sources.get(str(repo.id))
                repo_ids_to_add.append(repo_id)
                repo_names_to_add.append(repo.name)

        if len(repo_ids_to_add):
            add_repos = update_team_perimeter(gg_token, gitguardian_team_id, repo_ids_to_add)
            logger.info(
                f"Added the repos {repo_names_to_add}  to the perimeter : {gitguardian_team_id} status : {add_repos}")
