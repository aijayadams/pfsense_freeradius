import requests
from re import findall
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()

class pfSenseCaller():

    LOGIN_URL = "index.php"
    USERS_URL = "pkg.php?xml=freeradius.xml"
    USERS_FORM_URL = "pkg_edit.php?xml=freeradius.xml"
    CSRF_FIELD = "__csrf_magic"

    def __init__(self, host, username, password, port=443, protocol="https"):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.base_url = "{}://{}/".format(protocol, host)

        self.session = requests.session()

    def _get_csrf(self, result):
        return findall(
            'name=\'{}\'\s*value="([^"]+)"'.format(
                self.CSRF_FIELD), result.text)[0]

    def _get_next_id(self, result):

        return findall(
            'pkg_edit.php\?xml=freeradius.xml&amp;id=([^"]+)"',
            result.text)[0]


    def api_get(self, url):
        return self.session.get(url, verify=False)

    def api_post(self, url, payload, form_url=None):
        result = self.session.get(url, verify=False)

        if form_url:
            url = "{}&id={}".format(form_url, self._get_next_id(result))
            payload['id'] = self._get_next_id(result)


            result = self.session.get(url, verify=False)
        payload[self.CSRF_FIELD] = self._get_csrf(result)

        result = self.session.post(
            url,
            data=payload,
            headers=dict(refererurl=url)
        )


    def login(self):
        self.api_post(
            self.base_url + self.LOGIN_URL,
            {
                "usernamefld": self.username,
                "passwordfld": self.password,
                "login": "Sign In"
            })

    def add_user(self, username, password):
        #pudb.set_trace()
        self.api_post(
            self.base_url + self.USERS_URL,
            {
                "varusersusername": username,
                "varuserspassword": password,
                "varuserspasswordencryption": "Cleartext-Password",
                "varusersmotpinitsecret": "",
                "varusersmotppin": "",
                "varusersmotpoffset": "0",
                "varuserswisprredirectionurl": "",
                "varuserssimultaneousconnect": "",
                "description": "",
                "varusersframedipaddress": "",
                "varuserssimultaneousconnect": "",
                "varusersframedroute": "",
                "varusersvlanid": "",
                "varusersexpiration": "",
                "varuserssessiontimeout": "",
                "varuserslogintime": "",
                "varusersmaxtotaloctets": "",
                "varusersmaxbandwidthdown": "",
                "varusersmaxbandwidthup" : "",
                "varusersacctinteriminterval": "",
                "xml": "freeradius.xml",
                "id": "",
                "varuserstopadditionaloptions" : "",
                "varuserscheckitemsadditionaloptions": "",
                "varusersreplyitemsadditionaloptions": "",
                "varusersauthmethod": "motp",
                "varuserspointoftime": "Daily",
                "varusersmaxtotaloctetstimerange": "daily",
                'submit': 'Save'
            },
            form_url=self.base_url + self.USERS_FORM_URL)

    def list_users(self):
        output = {}
        result = self.api_get(self.base_url + self.USERS_URL)
        soup = BeautifulSoup(result.text, 'html5lib')
        for row in soup.find(id="mainarea").find("tbody").find_all("tr"):
            cells = row.find_all("td")
            if cells[0].get_text() != "Add" and 'id' in row.attrs.keys():
                num_id = int(row.attrs['id'][3:])
                output[cells[0].get_text().strip()]=num_id
        return output


    def del_user_by_name(self, username):
        users = self.list_users()
        if username not in users.keys():
            print("Username '{}' not found".format(username))
            return
        del_url = "{}&act=del&id={}".format(
            self.base_url + self.USERS_URL, users[username])
        self.api_get(del_url)
