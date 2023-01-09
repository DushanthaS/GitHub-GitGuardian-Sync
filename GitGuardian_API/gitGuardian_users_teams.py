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
