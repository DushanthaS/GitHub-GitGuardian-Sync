import os
import datetime
from loguru import logger
from Sync_GitHub_Users_to_GitGuardian import sync_gh_users_to_git_guardian
from Sync_GithubTeams_GitGuardian_Perimeter import sync_gh_teams_to_git_guardian_perimeter

ORGANIZATION = "YOURORG"
GITHUB_TOKEN = os.environ["GithubToken"]
GITGUARDIAN_TOKEN = os.environ["GitguardianToken"]

now = datetime.datetime.now()
date_time = now.strftime("%m-%d-%Y-%H-%M")
logger.add("{}_gitGuardian-{}.log".format(ORGANIZATION, date_time), format="{time} : {level} : {message}")


while True:
    print("\n")
    print("Enter option 1 to Sync Github Repos for Teams with Gitguardian Perimeter.")
    print("Enter option 2 to Sync Github users to Gitguardian.")
    print("\n")
    user_input = input("Please select an option (1, 2, or 3 to exit): ")
    if not user_input:
        print("Input cannot be empty")
        continue

    if user_input == "1":
        print("Sync Github Repos for Teams with Gitguardian Perimeter")
        sync_gh_teams_to_git_guardian_perimeter(ORGANIZATION, GITHUB_TOKEN, GITGUARDIAN_TOKEN)
    elif user_input == "2":
        print("Sync Github users to Gitguardian.")
        sync_gh_users_to_git_guardian(ORGANIZATION, GITHUB_TOKEN, GITGUARDIAN_TOKEN)
    elif user_input == "3":
        print("Exiting script.")
        break
    else:
        print("Invalid input. Please try again.")
