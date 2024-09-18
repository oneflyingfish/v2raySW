import json
from proxy_url import ProxyUrl
import subprocess

class GlobalArgs:
    subscription="https://moji.mojieurl.com/api/v1/client/subscribe?token=de61f11571db0c99446f087a7d7395d3"
    help_proxy_url=None
    http_proxy_port=10909

    test_url = "https://www.google.com"
    cache_path = "cache"
    xray_path = "xray_bin/xray"
    demo_xray_config_path="xray_bin/config.json"
    start_test_port = 61200

    run_process=None
    current_proxy=None
    xray_config_path="config.json"

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

def run_xray_config(proxy: ProxyUrl):
    if GlobalArgs.run_process is not None:
        GlobalArgs.run_process.kill()
        GlobalArgs.run_process=None
        current_proxy=None

    current_proxy=proxy
    write_config_json(current_proxy.GetXrayConfig(),GlobalArgs.xray_config_path,GlobalArgs.http_proxy_port)
    GlobalArgs.run_process = subprocess.Popen("{} run -c {}> /dev/null 2>&1 &".format(GlobalArgs.xray_path, GlobalArgs.xray_config_path), shell=True)
    if GlobalArgs.run_process.stderr:
        print(GlobalArgs.run_process.stderr)
        GlobalArgs.run_process.kill()
        GlobalArgs.run_process=None
        current_proxy=None
        return False
    return True
    
