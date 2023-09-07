import dropbox
from dropbox.exceptions import AuthError
import os
from dropbox_funcs.dropbox_refresh import dropbox_refresh

#find the tokens in info.txt
def string_split(string):
    textfile = "info.txt"

    with open(textfile) as f:
        lines = f.readlines()

    for line in lines:
        if f"{string} = " in line:
            var, token = line.split(" = ")
            if "\n" in line:
                token = token[:-1] #remove \n for newline
            break
    
    return token

#I plan on having the transcript itself
#be an input for this function here
#so I can upload it on dropbox

def dropbox_upload(cloudlist, servername, date):
    #all the tokens needed that are stored in info.txt
    app_key = string_split("app_key")
    app_secret = string_split("app_secret")
    refresh_token = string_split("refresh_token")
    access_code = string_split("access_code")

    try:
        dbx = dropbox.Dropbox(app_key=app_key, app_secret=app_secret, oauth2_refresh_token=refresh_token)
    except AuthError:
        refresh_token = dropbox_refresh(app_key, app_secret, access_code)
        if refresh_token == None:
            return "Cloud save failed"
        else:
            dbx = dropbox.Dropbox(app_key=app_key, app_secret=app_secret, oauth2_refresh_token=refresh_token)

    files = dbx.files_list_folder("").entries
    for file in files:
        if file.name == servername:
            break
    else:
        dbx.files_create_folder(f"/{servername}")

    dbx.files_create_folder(f"/{servername}/{date}")

    path = f"/{servername}/{date}/"

    for file in cloudlist:
        filename = f"chat-history-{servername}-{file['channel']}-{date}.html"
        filepath = path + filename

        #this encodes in binary utf-8
        bin_transcript = file["transcript"].encode("utf-8")

        dbx.files_upload(bin_transcript, path=filepath)

    return "Saved to cloud"