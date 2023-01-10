from requests import request, exceptions
import logging
logger = logging.getLogger(__name__)


class GitHubQuery:
    GH_BASE_URL = "https://api.github.com/graphql"

    def __init__(
            self,
            github_token=None,
            query=None,
            variables=None,
            additional_headers=None
    ):
        self.github_token = github_token
        self.query = query
        self.variables = variables or dict()
        self.additional_headers = additional_headers or dict()

    @property
    def headers(self):
        default_headers = dict(
            Authorization=f"token {self.github_token}",
        )
        return {
            **default_headers,
            **self.additional_headers
        }

    def generator(self):
        while True:
            try:
                yield request(
                    'post',
                    GitHubQuery.GH_BASE_URL,
                    headers=self.headers,
                    json={"query": self.query, "variables": self.variables}
                ).json()
            except exceptions.HTTPError as http_err:
                raise http_err
            except Exception as err:
                raise err

    def iterator(self):
        pass
