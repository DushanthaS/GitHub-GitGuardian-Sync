
from Github_GQL.github_query_gql import GitHubQuery
import logging
logger = logging.getLogger(__name__)


GH_BASE_URL = "https://api.github.com/graphql"


# getting users from GitHub
class GetGitUsers(GitHubQuery):
    GET_GIT_USERS_QUERY = """
            query($after: String, $org:String!){
   organization(login: $org) {
                    samlIdentityProvider {
                        externalIdentities(first:100 , after:$after , membersOnly: true) {
                            pageInfo {
                                endCursor startCursor hasNextPage
                            }
                            edges {
                                cursor node {
                                    samlIdentity {
                                        nameId
                                        username
                                    } user {
                                        login
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """

    ADDITIONAL_HEADERS = dict(
        Accept="application/vnd.github.vixen-preview+json",
    )

    def __init__(self, organization_name, gh_token):
        super().__init__(
            github_token=gh_token,
            query=GetGitUsers.GET_GIT_USERS_QUERY,
            variables=dict(org=organization_name, after=None),
            additional_headers=GetGitUsers.ADDITIONAL_HEADERS
        )
        self._identities = list()

    def iterator(self):
        generator = self.generator()
        has_next_page = True
        saml_identities = list()
        while has_next_page:
            response = next(generator)
            end_cursor = response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["pageInfo"][
                "endCursor"]
            self.variables["after"] = end_cursor
            saml_identities.extend(
                response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["edges"]
            )
            has_next_page = response["data"]["organization"]["samlIdentityProvider"]["externalIdentities"]["pageInfo"][
                "hasNextPage"]
        return saml_identities


# getting teams per user from GitHub

class GetGithubTeams(GitHubQuery):
    GET_GIT_TEAMS_QUERY = """
              query($user:String!,$org:String!){
              organization(login: $org) {
                teams(first: 100, userLogins: [$user]) {
                  totalCount
                  edges {
                    node {
                      name
                      description
                    }
                  }
                }
              }
            }

            """

    ADDITIONAL_HEADERS = dict(
        Accept="application/vnd.github.vixen-preview+json",
    )

    def __init__(self, organization_name, gh_token, gh_user):
        super().__init__(
            github_token=gh_token,
            query=GetGithubTeams.GET_GIT_TEAMS_QUERY,
            variables=dict(org=organization_name, user=gh_user),
            additional_headers=GetGithubTeams.ADDITIONAL_HEADERS
        )
        self._identities = list()

    def iterator(self):
        teams_list = []
        generator = self.generator()
        response = next(generator)
        result_data = response['data']['organization']['teams']['edges']

        for d in result_data:
            row = [d['node']['name']]
            teams_list.append(row[0].lower())
        return teams_list


