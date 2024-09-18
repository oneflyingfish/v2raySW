import subscription
from common import GlobalArgs
from proxy_url import ProxyUrl

def main():
    print("hello")
    urls = subscription.AnalyzeSubscription(subscription_url=GlobalArgs.subscription, help_proxy_url="http://172.28.192.1:10809") # type: list[ProxyUrl]
    for url in urls:
        print(url.name, ", ", url.GetLatency(GlobalArgs.start_test_port))
        print()

if __name__ == "__main__":
    main()