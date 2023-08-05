# ga-chgraph

## 1 介绍

该项目是图操作项目，包含：

- 图节点/边的查询操作
- 整张图的插入/删除/查询/总结/描述操作
- 图节点/边的插入操作
- 关于图的服务

## 2 图操作服务：

### 2.1 基于docker的服务化

#### 2.1.1 安装启动

需要安装docker

```
#下载源码
git clone git@w.src.corp.qihoo.net:data-platform/intell-dev/ga-chgraph.git

#构建镜像
cd ga-chgraph
docker build -t ga-chgraph:v1 .

#修改配置文件
将docker镜像中的/usr/local/lib/python3.6/site-packages/clickhouse_api_server/config/graph_config.json中的IP更换为自己的IP

#启动容器服务
docker run -it  -p 10010:10010  ga-chgraph:v1

```

至此，图操作服务已经启动

#### 2.1.2 swagger文档路径

```
此处p47708v.hulk.shbt.qihoo.net需要更换为自己的服务器地址
http://p47708v.hulk.shbt.qihoo.net:10010/doc
```


#### 2.1.3 测试

```
图节点/边的查询操作(全部为get请求)

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edges

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertices

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-db/api/v1/multi-hop-common-vertices


整张图的插入/删除/查询/总结/描述的操作

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-registration

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-deletion

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-show

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-summary/(?P<graph_name>\S*)

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-description/(?P<graph_name>\S*)

图节点/边的插入操作

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edge-insertion

url：p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertex-insertion

此处p47708v.hulk.shbt.qihoo.net需替换为您自己的机器。

```

测试数据：

```
以p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop为例：

{
  "start_vertex_list": [
    "10.73.28.115",
    "10.78.55.20"
  ],
  "edge_name_list": [
    "tcpflow",
    "flow"
  ],
  "graph_name": "cyber_plus",
  "direction": "forward",
  "edge_con_list_list": [
    [
      "downlink_length>10000",
      "protocol='http'"
    ],
    [
      "record_date='2019-04-15'"
    ]
  ],
  "target_field_list": [
    "record_time"
  ]
}  


```

返回结果：

```
{
    "result": [
        [
            [
                "10.73.28.115",
                "10.59.81.218",
                "2019-04-15 13:37:18"
            ],
            [
                "10.73.28.115",
                "117.34.15.37",
                "2019-04-15 13:41:39"
            ],
        ....
       ]
}
```

如图：

![image](./images/1.png)
