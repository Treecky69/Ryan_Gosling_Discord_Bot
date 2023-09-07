import requests
import base64

#find the tokens in info.txt
# def string_split(string):
#     textfile = "info.txt"

#     with open(textfile) as f:
#         lines = f.readlines()

#     for line in lines:
#         if f"{string} = " in line:
#             var, token = line.split(" = ")
#             if "\n" in line:
#                 token = token[:-1] #remove \n for newline
#             break
    
#     return token

# #I plan on having the transcript itself
# #be an input for this function here
# #so I can upload it on dropbox


# #all the tokens needed that are stored in info.txt
# app_key = string_split("app_key")
# app_secret = string_split("app_secret")
# #refresh_token = string_split("refresh_token")
# access_code = string_split("access_code")

#https://stackoverflow.com/questions/71524238/how-to-create-not-expires-token-in-dropbox-api-v2

def dropbox_refresh(app_key, app_secret, access_code):
    textfile = "info.txt"

    # Encode the app key and app secret in base64
    base64authorization = base64.b64encode(f"{app_key}:{app_secret}".encode()).decode()

    # Create the payload for the POST request
    data = {
        'code': access_code,
        'grant_type': 'authorization_code'
    }

    # Define the headers for the request
    headers = {
        'Authorization': f'Basic {base64authorization}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make the POST request
    url = 'https://api.dropbox.com/oauth2/token'
    response = requests.post(url, data=data, headers=headers)

    # Process the response
    if response.status_code == 200:
        # Success, handle the response data here
        #print(response.json()["refresh_token"])
        return response.json()["refresh_token"]

        #THIS SHOULD WRITE THE NEW REFRESH TOKEN TO THE FILE
        # vswith open(textfile) as f:
        #     lines = f.readlines()
    else:
        # Handle error here
        print(f"Error: {response.status_code} - {response.text}")
        return None

# response = dropbox_refresh(app_key, app_secret, access_code)
# print(response)