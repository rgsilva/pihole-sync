import requests

from requests_toolbelt import MultipartEncoder

from config import *

class Instance:
    _session: requests.Session = None
    _token: str = None

    def __init__(self, config: InstanceConfig):
        self._config = config

    def login(self):
        session = requests.session()

        # Login
        resp = session.post(
            f"http://{self._config.endpoint}/admin/login.php",
            data={
               "pw": self._config.password,
            },
            allow_redirects=False
        )
        if resp.status_code != 302:
            raise ValueError(f"Unexpected status code {resp.status_code}")

        # Get token
        resp = session.get(
            f"http://{self._config.endpoint}/admin/index.php"
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")
        
        token = resp.text.split("<div id=\"token\" hidden>")[1].split("<")[0].strip()
        if len(token) == 0:
            raise ValueError(f"Empty token")
        
        self._session = session
        self._token = token

    def export(self) -> bytes:
        resp = self._session.post(
            f"http://{self._config.endpoint}/admin/scripts/pi-hole/php/teleporter.php",
            data={
                "token": self._token
            }
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")

        return resp.content

    def restore(self, backup: bytes):
        data = MultipartEncoder(fields={
                "token": self._token,
                "action": "in",
                "whitelist": "true",
                "regex_whitelist": "true",
                "blacklist": "true",
                "regexlist": "true",
                "adlist": "true",
                "client": "true",
                "group": "true",
                "auditlog": "true",
                "staticdhcpleases": "true",
                "localdnsrecords": "true",
                "localcnamerecords": "true",
                "flushtables": "true",
                "zip_file": ("backup.tar.gz", backup, "application/x-gzip"),
            })
        resp = self._session.post(
            f"http://{self._config.endpoint}/admin/scripts/pi-hole/php/teleporter.php",
            data=data, headers={"Content-type": data.content_type}
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")

        return resp.text.replace("<br>", "").split("\n")

    def restart(self):
        resp = self._session.post(
            f"http://{self._config.endpoint}/admin/settings.php",
            data={
                "token": self._token,
                "field": "restartdns",
            }
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")

        return resp.content

    def cleanup(self) -> bytes:
        resp = self._session.post(
            f"http://{self._config.endpoint}/admin/scripts/pi-hole/php/groups.php",
            data={
                "action": "get_domains",
                "token": self._token
            }
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")

        domains = resp.json()["data"]
        ids_to_delete = [str(item["id"]) for item in domains]

        resp = self._session.post(
            f"http://{self._config.endpoint}/admin/scripts/pi-hole/php/groups.php",
            data={
                "action": "delete_domain",
                "ids": "[%s]" % ",".join(ids_to_delete),
                "token": self._token
            }
        )
        if resp.status_code != 200:
            raise ValueError(f"Unexpected status code {resp.status_code}")
