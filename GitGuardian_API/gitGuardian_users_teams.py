import json
import requests

GG_API_URL = "https://api.gitguardian.com/v1"


def create_headers(token):
    return {
        "Authorization": f"Token {token}",
        'Content-Type': 'application/json'}


def create_headers2(token):
    return {
        "Authorization": f"Token {token}"}


def create_payload(data):
    return json.dumps(data)


def handle_response(response):
    if response.status_code == 204:
        return response.text
    elif response.headers["content-type"].strip().startswith("application/json"):
        try:
            return response.json()
        except Exception as ex:
            logger.error(repr(ex))


def gg_invite(token, user_email):
    url = f"{GG_API_URL}/invitations"
    headers = create_headers(token)
    payload = create_payload({"email": user_email, "role": "member"})
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def add_to_teams(token, team_id, member_id):
    url = f"{GG_API_URL}/teams/{team_id}/team_memberships"
    payload = {'member_id': member_id, 'team_permission': 'cannot_manage',
               'incident_permission': 'can_view'}
    headers = create_headers2(token)
    response = requests.request("POST", url, headers=headers, data=payload)
    return handle_response(response)


def get_gg_team_id(token, gh_team):
    url = f"{GG_API_URL}/teams?search={gh_team}"
    headers = create_headers(token)
    response = requests.request("GET", url, headers=headers)
    return handle_response(response)


def get_gg_member_id(token, gh_email):
    url = f"{GG_API_URL}/members?search={gh_email}"
    headers = create_headers(token)
    response = requests.request("GET", url, headers=headers)
    return handle_response(response)


def gg_invite_teams(token, team_id, invitation_id):
    url = f"{GG_API_URL}/teams/{team_id}/team_invitations"
    payload = {
        'invitation_id': invitation_id,
        'team_permission': 'cannot_manage',
        'incident_permission': 'can_view'}
    headers = create_headers2(token)
    response = requests.request("POST", url, headers=headers, data=payload)
    return handle_response(response)


def get_gg_invitation_id(token, user_email):
    url = f"{GG_API_URL}/invitations?search={user_email}"
    headers = create_headers(token)
    response = requests.request("GET", url, headers=headers)
    return handle_response(response)


def get_gg_user_id(token, user_email):
    url = f"{GG_API_URL}/users?search={user_email}"
    headers = create_headers(token)
    response = requests.request("GET", url, headers=headers)
    return handle_response(response)


def gg_update_member(token, member_id):
    url = f"{GG_API_URL}/members/{member_id}"

    payload = {
        'role': 'member'}
    headers = create_headers2(token)
    response = requests.request("PATCH", url, headers=headers, data=payload)
    print(response)
    return handle_response(response)


def get_gg_sources(token):
    url = f"{GG_API_URL}/sources"
    headers = create_headers(token)
    response = requests.request("GET", url, headers=headers)
    # Initial request to get the first page of results
    sources = response.json()

    # Get the cursor for the next page of results
    link_header = response.headers.get('link')
    cursor = re.search("cursor=([^>]+)", link_header).group(1) if link_header else None
    l_next = re.search("next", link_header).group(0)
    # Loop through pages of results while a cursor is returned
    # pdb.set_trace()
    while l_next == "next":
        # Make the next request with the cursor
        next_response_url = f"{GG_API_URL}/sources??cursor={cursor}"
        next_response = requests.request("GET", next_response_url, headers=headers)
        sources.extend(next_response.json())
        link_header = next_response.headers.get('link')

        try:
            l_next = re.search("next", link_header).group(0)
            cursor = re.search("cursor=([^>]+)", link_header).group(1) if link_header else None
        except AttributeError:
            break
    gh_gg_dict = {i["external_id"]: i["id"] for i in sources}
    return gh_gg_dict


def update_team_perimeter(token, team_id, repo_id):
    url = f"{GG_API_URL}/teams/{team_id}/sources"
    payload = {"sources_to_add": repo_id}
    headers = create_headers(token)
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    handle_response(response)
    return response.status_code
