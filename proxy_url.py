import base64
import json
from urllib.parse import unquote

class ProxyType:
    unknown=0
    vmess=1
    trojan=2

class ProxyUrl:
    def __init__(self):
        self.name=None
        self.url=None
        self.type=ProxyType.unknown
        self.tag=None
        self.valid=False

    def Load(self):
        pass

    def ToList(self):
        return [self.name, self.url, self.tag, self.valid]

class VmessProxyUrl(ProxyUrl):
    def __init__(self):
        super().__init__()
        self.type=ProxyType.vmess

    def Load(self, url:str):
        try:
            self.tag = json.loads(base64.b64decode(url.split("://")[1]).decode("utf-8"))
            self.name=self.tag["ps"]

            host = self.tag["add"]
            port = self.tag["port"]
            id = self.tag["id"]
            aid = self.tag["aid"]
            path = self.tag["path"]
            tls = self.tag["tls"]
            net = self.tag["net"]
            type = self.tag["type"]
            self.url=f"vmess://{id}:{aid}@{host}:{port}/?path={path}&tls={tls}&net={net}&type={type}"
            self.valid=True
        except:
            self.valid=False

class TrojanProxyUrl(ProxyUrl):
    def __init__(self):
        super().__init__()
        self.type=ProxyType.trojan

    def Load(self, url:str):
        try:
            self.name = unquote(url.split("#")[1].split("\r")[0])
            self.url = url.split("#")[0]
            self.tag = url

            self.valid=True
        except:
            self.valid=False
