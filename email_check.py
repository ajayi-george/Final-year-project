import requests


def validate(email):
    api_key = 'YtCeYFU2.qaVsq1BBzUZjW9oDfk2scCFlC6crOXKw' # Generated in your User Profile it shows at the top in a green bar once
    team_slug = "georgeajakadrex" # when you sign up you have a team, its in the URL then use that
    email_address = email # the test email


    response = requests.post(
        "https://app.mailvalidation.io/a/" + team_slug + "/validate/api/validate/",
        json={'email': email_address},
        headers={
                'content-type': 'application/json',
                 'accept': 'application/json',
                'Authorization': 'Api-Key ' + api_key,
                 },
    )

    valid = response.json()['is_valid']
    if valid:
        res="Valid"
    else:
        res="Invalid"
    return res


