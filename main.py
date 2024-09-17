import subscription
import global_args

def main():
    print("hello")
    urls = subscription.analyze_subscription(subscription_url=global_args.subscription, help_proxy_url="http://172.28.192.1:10809")
    for url in urls:
        print(url.ToList())
        print()

if __name__ == "__main__":
    main()