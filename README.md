# GitGuardian-GitHub-Sync

This repository contains a Python script that syncs users and teams between GitGuardian and GitHub. It uses the GitHub GraphQL API and the GitGuardian API to retrieve information about users and teams, and it invites new users to GitGuardian and adds them to the appropriate teams based on their membership in GitHub.

## Requirements

- Python 3.6 or higher
- `GitHubToken` and `GitguardianToken` environment variables set with the appropriate API keys

## Usage

To use this script, simply run it using the `python` command. The script will retrieve the list of users and teams from GitHub and GitGuardian, and it will handle the synchronization process automatically.

## Configuration

The script can be configured by modifying the following variables at the top of the file:

- `ORGANIZATION`: The name of the organization on GitHub
- `GITHUB_TOKEN`: The API key for accessing the GitHub GraphQL API
- `GITGUARDIAN_TOKEN`: The API key for accessing the GitGuardian API

## Logging

The script logs all actions and errors to a file named `ORGANIZATION_gitGuardian-DATE-TIME.log`. The `ORGANIZATION` and `DATE-TIME` variables are automatically set based on the current date and time.
