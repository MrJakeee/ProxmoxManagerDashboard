import httpx
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProxmoxManager:
    def __init__(self, username, password, realm):
        self.base_url = "https://192.168.0.160:8006/api2/json"
        self.user = username
        self.password = password
        self.realm = realm

        self.username_proxmox = None
        self.ticket = None
        self.csrf_token = None
        self.headers = {}
        self.cookies = {}

        self.client = None

    def __str__(self):
        return f"Host: {self.base_url}, User: {self.user}, Realm: {self.realm}"

    async def login(self):
        "URL for obtaining Token and CSRFPreventionToken"
        url_acces = f"{self.base_url}/access/ticket"
        username_full = f"{self.user}@{self.realm}"
        payload = {"username": username_full, "password": self.password}

        async with httpx.AsyncClient(verify=False) as client:
            try:
                response = await client.post(url_acces, data=payload)
                if response.status_code != 200:
                    print(f"Error login: {response.status_code}")
                    return False

                data = response.json()["data"]
                self.username_proxmox = data["username"]
                self.ticket = data["ticket"]
                self.csrf_token = data["CSRFPreventionToken"]

                self.cookies = {"PVEAuthCookie": self.ticket}
                self.headers = {"CSRFPreventionToken": self.csrf_token}

                self.client = httpx.AsyncClient(
                    verify=False,
                    base_url=self.base_url,
                    cookies=self.cookies,
                    headers=self.headers,
                )
                return True
            except httpx.HTTPError as e:
                print(f"Error de conexión o HTTP: {e}")
                return False
            except Exception as e:
                print(f"Error login: {e}")
                return False

    async def getVMExistents(self):
        endpoint = "/cluster/resources?type=vm"

        try:
            response = await self.client.get(endpoint)

            if response.status_code == 200:
                data = response.json()["data"]

                return data

            else:
                print(f"Error al obtener recursos: {response.status_code}")
                return None
        except httpx.HTTPError as e:
            print(f"Error HTTP {e}")
            return None

    def getUser(self):
        return self.username_proxmox

    async def getStatusProxmox(self):
        endpointstatus = "/nodes/me/status"

        try:
            response = await self.client.get(endpointstatus)

            if response.status_code == 200:
                data = response.json()["data"]

                return data
            else:
                print(f"error: {response.status_code}")
        except Exception as e:
            print(f"Error HTTP: {e}")

    async def getStorageTotal(self):
        endpointstorage = "/nodes/me/storage"

        try:
            response = await self.client.get(endpointstorage)

            if response.status_code == 200:
                data_storage = response.json()["data"]
                return data_storage
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

    async def getAllVMS(self):
        endpointstorage = "/nodes/me/qemu"

        try:
            response = await self.client.get(endpointstorage)

            if response.status_code == 200:
                data_storage = response.json().get("data", [])
                return data_storage
            else:
                print(f"Error to obtain data VMS: {response.status_code}")
        except Exception as e:
            print(f"Error VMS: {e}")
