import base64
import requests

from requests_oauthlib import OAuth2Session

# See https://developer.yahoo.com/oauth2/guide/
def get_authorization_url(client_id):
    request_authorization_url = 'https://api.login.yahoo.com/oauth2/request_auth'
    redirect_uri = 'oob'
    print('Client ID: ' + client_id)
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, state = oauth.authorization_url(request_authorization_url)
    print('Authorization URL:' + authorization_url)


def get_authentication_header(client_id, client_secret):
    string_to_encode = client_id + ':' + client_secret
    byte_data = string_to_encode.encode('utf-8')
    base64_encoded_data = base64.b64encode(byte_data)
    base64_string = base64_encoded_data.decode('utf-8')
    return base64_string


def get_oauth_token(auth_header, yahoo_code):
    token_url = 'https://api.login.yahoo.com/oauth2/get_token'
    headers = {'Authorization': auth_header, 'Accept': 'application/json',
               'Content-Type': 'application/x-www-form-urlencoded'}
    json_body = {'code': yahoo_code, 'grant_type': 'authorization_code',
                 'redirect_uri': 'oob'}
    try:
        response = requests.post(token_url, headers=headers, data=json_body)
        response.raise_for_status()
        if response.status_code == 200:
            print('Successfully obtained OAuth token')
            return response.json()
        else:
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Connection error occurred: {conn_err}')
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error occurred: {timeout_err}')
    except requests.exceptions.TooManyRedirects as redirects_err:
        print(f'Too many redirects: {redirects_err}')
    except requests.exceptions.RequestException as req_err:
        print(f'An error occurred: {req_err}')



# Confluence Page: https://curryware.atlassian.net/wiki/spaces/CUR/pages/50790402/OAuth+Flow
def main():
    print ('Go to https://developer.yahoo.com/apps/ to find the client id of the '
           'application\r')
    client_id_string = input("Enter the Client ID of the application: ")
    client_secret = input('Enter the Client Secret of the application: ')
    print("\rYou should see a URL once you hit the return key that needs to be pasted "
          "into a browser")

    get_authorization_url(client_id_string)
    print('Client ID: ' + client_id_string)
    print('Client Secret: ' + client_secret)

    authorization_string = get_authentication_header(client_id_string, client_secret)
    print('\r')
    print('Need to put this authorization string in Postman if use that!')
    print('Otherwise you can enter the code that was obtained from the Yahoo page!')
    print('Authorization String: Basic ' + authorization_string)

    yahoo_code = input('Enter the code obtained from the Yahoo page: ')
    if len(yahoo_code) == 0:
        exit(0)
    else:
        oauth_token_json = get_oauth_token(authorization_string, yahoo_code)
        print(oauth_token_json)


if __name__ == "__main__":
    main()
