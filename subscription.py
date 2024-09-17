import requests
import base64
import proxy_url

def AnalyzeSubscription(subscription_url:str, help_proxy_url: str=None):
        sub_urls=[]

        try:
            response = requests.get(
                        subscription_url,
                        verify=False,
                        proxies={"http": help_proxy_url, "https": help_proxy_url} if help_proxy_url is not None else None,
                    )
            
            if response.status_code == 200:
                    print("get http request successful...")
                    url_list = [url for url in base64.b64decode(response.text).decode("utf-8").split("\n") if len(url)>0]
                    for url in url_list:
                        current_url=None
                        if "vmess" in url:
                            current_url=proxy_url.VmessProxyUrl()
                        else:
                            current_url=proxy_url.TrojanProxyUrl()
                        current_url.Load(url)
                        if current_url.valid:
                             sub_urls.append(current_url)
                    
            else:
                print(f"Failed to retrieve {subscription_url}: Status code {response.status_code}")
            return sub_urls
        except Exception as ex:
            print(f"meet exception while analyze subscription: {ex}")
            return []