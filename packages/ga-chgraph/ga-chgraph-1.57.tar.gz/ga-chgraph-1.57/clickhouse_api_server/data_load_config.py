import os
import sys
import ujson
from clickhouse_driver import Client
from graph_op import CHGraph
import pandas as pd


'''

graph_dir = "./config/tcpflow_flow.cfg.json"

#graph = CHGraph(graph_dir, client)

'''


def load_config():
    print("服务所有配置开始加载")
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = os.path.split(curPath)
    sys.path.append(rootPath[0])
    sys.path.append(rootPath[0]+"/"+rootPath[1])

    clickhouse_config_dir = rootPath[0]+"/"+rootPath[1]+"/config/"+"graph_config.json"

    with open(clickhouse_config_dir, 'r') as f:
        clickhouse_config = ujson.load(f)
   
    clickhouse_ip = clickhouse_config["ip"]
    print(clickhouse_ip)
    client = Client(clickhouse_ip)
    graph = CHGraph(client)
    print("服务所有配置加载结束")
    config_params = {
        "graph": graph
    }
    #config_params = {
    # 
    #}
    return config_params
