import subscription
from common import GlobalArgs

def main():
    print("hello")
    urls = subscription.analyze_subscription(subscription_url=GlobalArgs.subscription, help_proxy_url="http://172.28.192.1:10809")
    for url in urls:
        print(url.Hash())
        print()

if __name__ == "__main__":
    main()