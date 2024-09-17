import json

class GlobalArgs:
    subscription="https://moji.mojieurl.com/api/v1/client/subscribe?token=de61f11571db0c99446f087a7d7395d3"
    help_proxy_url=None
    http_proxy_port=10809
    test_url = "https://www.google.com"
    cache_path = "cache"
    demo_xray_config_path="xray_bin/config.json"

def write_config_json(proxy_xray_config, output_config_path, port):
    # read json
    with open(GlobalArgs.demo_xray_config_path, "r") as f:
        data = json.load(f)

    # update data
    data["outbounds"][0] = proxy_xray_config
    data["inbounds"][0]["port"] = port - 1
    data["inbounds"][1]["port"] = port

    # write back
    with open(output_config_path, "w") as f:
        json.dump(data,f,indent=4)