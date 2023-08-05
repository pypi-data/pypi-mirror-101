import os
import sys
import json
from datetime import date,datetime
import pandas as pd
import numpy as np
import logging


LOG_FORMAT="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
#logging.basicConfig(filename='./CHGraph.log', level=logging.INFO, format=LOG_FORMAT)
logging.basicConfig(filename='./CHGraph.log', level=logging.WARNING, format=LOG_FORMAT)
logger = logging.getLogger('CHGraph')


def tostr(obj):
    if type(obj) == list:
        return str(obj)
    elif type(obj) == np.ndarray:
        return np.array2string(obj, separator=',', threshold=1000000000, max_line_width=1000000000)


class CHGraph(object):

    def __init__(self, client):
        self.client = client
        logger.info('CHGraph Start')
        client.execute('create database if not exists graph_cfg_2')        
        client.execute('create table if not exists graph_cfg_2.name2cfg_2 (graph_create_date Date,graph_name String,graph_status UInt32,graph_cfg String) engine = MergeTree(graph_create_date, (graph_name), 8192);')

    #############################################
    #################### graph-wise operation
    #############################################
    # graph_name: graph name as string 
    # graph_cfg: graph cfg as json string
    def register_graph(self, graph_name, graph_cfg):        
        sql = "select * from graph_cfg_2.name2cfg_2 where graph_name=\'"+graph_name+"\' and graph_status=1"
        res = self.client.execute(sql)
        if len(res) > 0:
            logger.warning("graph name ["+graph_name+"] already exists")
            return "graph name ["+graph_name+"] already exists"
        sql = "insert into graph_cfg_2.name2cfg_2 (*) values (\'" + str(date.today()) + "\',\'" + graph_name + "\',1,\'" + graph_cfg + "\');"
        self.client.execute(sql)
        logger.info("register graph ["+graph_name+"] done")
        return "register graph ["+graph_name+"] done"


    def delete_graph(self, graph_name):
        sql = "select * from graph_cfg.name2cfg where graph_name=\'"+graph_name+"\' and graph_status=1"
        res = self.client.execute(sql)
        if len(res) == 0:
            logger.warning("graph name ["+graph_name+"] does not exist")
            return "graph name ["+graph_name+"] does not exist"
        sql_update = "alter table graph_cfg.name2cfg update graph_status=0 WHERE graph_name=\'"+graph_name+"\' and graph_status=1"
        self.client.execute(sql_update)
        logger.info("delete graph ["+graph_name+"] done")
        return "delete graph ["+graph_name+"] done"
        
        
    def show_graph(self):
        sql = "select graph_name from graph_cfg.name2cfg where graph_status=1"
        res = self.client.query_dataframe(sql)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            logger.info(res)
        return res

    def use_graph(self, graph_name):
        sql = "select * from graph_cfg.name2cfg where graph_name=\'" + graph_name + "\' and graph_status=1"
        res = self.client.execute(sql)
        if len(res) == 0:
            logger.warning("graph name [" + graph_name + "] does not exist")
            return
        else:
            self.graph_name = graph_name
            self.graph_cfg = json.loads(res[0][3])
            logger.info("use graph [" + graph_name + "] done")

    def describe_graph(self, graph_name):
        sql = "select * from graph_cfg.name2cfg where graph_name=\'"+graph_name+"\' and graph_status=1"
        res = self.client.execute(sql)
        if len(res) == 0:
            logger.warning("graph name ["+graph_name+"] does not exist")
            return "graph name ["+graph_name+"] does not exist"
        else:
            graph_cfg = json.loads(res[0][3])
            logger.info(graph_cfg)
            return graph_cfg

    def summary_graph(self, graph_name):
        sql = "select * from graph_cfg.name2cfg where graph_name=\'"+graph_name+"\' and graph_status=1"
        res = self.client.execute(sql)
        if len(res) == 0:
            logger.warning("graph name ["+graph_name+"] does not exist")
            return None
        graph_cfg = json.loads(res[0][3])
        edge_count = {}
        for name in graph_cfg['edges']:
            info = graph_cfg['edges'][name]
            sql = "select count(*) from "+info['db']+"."+info['table']
            res = self.client.execute(sql)
            logger.info("count of edge ["+name+"]: "+str(res[0][0]))
            edge_count[name] = res[0][0]
        vertex_count = {}
        for name in graph_cfg['vertexes']:
            info = graph_cfg['vertexes'][name]
            sql = "select count(*) from "+info['db']+"."+info['table']
            res = self.client.execute(sql)
            logger.info("count of vertex ["+name+"]: "+str(res[0][0]))
            vertex_count[name] = res[0][0]
        return (edge_count, vertex_count)


    #############################################
    #################### vertex/edge-wise operation: insert
    #############################################
    def insert_edge(self, edge_name, edge_schema, edge_data):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        if edge_info["src"] not in edge_schema or edge_info["dst"] not in edge_schema:
            logger.warning("require src field and dst field of edge")
            return "require src field and dst field of edge"

        sql = "insert into " + db_table + " (" + ",".join(edge_schema) + ") values " + ",".join([str(line) for line in edge_data])
        self.client.execute(sql)
        return "edge inserted success"


    def insert_vertex(self, vertex_name, vertex_schema, vertex_data): 
        
        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return "invalid vertex: " + vertex_name

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        if vertex_info["id"] not in vertex_schema:
            logger.warning("require id field of vertex")
            return "require id field of vertex"

        sql = "insert into " + db_table + " (" + ",".join(vertex_schema) + ") values " + ",".join([str(line) for line in vertex_data])
        self.client.execute(sql)
        return "vertex inserted success"


    #############################################
    #################### vertex/edge-wise operation: search
    #############################################
    ## one_hop return edges
    ## one_hop does not require type(src) == type(dst)
    def one_hop(self,
                start_vertex_list,
                direction,
                edge_name,
                edge_con_list, 
                target_field_list,
                end_vertex_con_list=None):
        
        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]

        db_table = edge_info["db"] + "." + edge_info["table"]

        if direction == "forward":
            start_vertex_list_con = edge_info["src"] + " in " + tostr(start_vertex_list)
        elif direction == "backward":
            start_vertex_list_con = edge_info["dst"] + " in " + tostr(start_vertex_list)
        elif direction == "bidirectional":
            start_vertex_list_con = "(" + edge_info["src"] + " in " + tostr(start_vertex_list) + " or " + edge_info["dst"] + " in " + tostr(start_vertex_list) + ")"
        else:
            logger.warning("invalid direction")
            return "invalid direction"
        #print(start_vertex_list_con)

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " and " + " and ".join(edge_con_list)
        #print(edge_con_list_con)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(edge_info["fields"])
        elif type(target_field_list) == list and len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)
        elif type(target_field_list) == str and target_field_list == "src":
            target_field_list_con = "DISTINCT " + edge_info["src"]
        elif type(target_field_list) == str and target_field_list == "dst":
            target_field_list_con = "DISTINCT " + edge_info["dst"]

        sql = "select " + target_field_list_con + " from " + db_table + " where " + \
                  start_vertex_list_con + edge_con_list_con
        logger.info("sql: "+sql)
        #res = self.client.execute(sql)
        res = self.client.query_dataframe(sql)

        return res

    
    ## multi_hop return edges
    ## multi_hop requires type(src) == type(dst)
    def multi_hop(self,
                  step,
                  start_vertex_list,
                  direction,
                  edge_name,
                  edge_con_list, 
                  target_field_list,
                  only_last_step,
                  plus_last_vertexes=False,
                  end_vertex_con_list=None):

        multi_res = []
        
        multi_step_start_vertex_list = start_vertex_list

        for i in range(step):

            res = self.one_hop(multi_step_start_vertex_list,
                               direction,
                               edge_name,
                               edge_con_list,
                               target_field_list)

            if res.shape[0] == 0:
                logger.warning("multi-hop terminates at "+str(i+1))
                break
            
            multi_res.append(res)
            
            if i == step - 1 and not plus_last_vertexes:
                continue

            # TODO: may have performance issue
            edge_info = self.graph_cfg["edges"][edge_name]
            if direction == "forward":
                multi_step_start_vertex_list = np.unique(res[edge_info['dst']].values)
            elif direction == "backward":
                multi_step_start_vertex_list = np.unique(res[edge_info['src']].values)
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return
            else:
                logger.warning("invalid direction")
                return "invalid direction"

        if only_last_step:
            if plus_last_vertexes:
                return (multi_res[-1], multi_step_start_vertex_list)
            else:
                return multi_res[-1]
        else:
            return multi_res


    # multi_hop_common_vertexes return common vertexes
    def multi_hop_common_vertexes(self,
                                  step,
                                  start_vertex_list,
                                  direction,
                                  edge_name,
                                  edge_con_list):
        
        end_set_list = []
        for i in range(len(start_vertex_list)):
            (res, vertex) = self.multi_hop(step, 
                                           [start_vertex_list[i]], 
                                           direction,
                                           edge_name,
                                           edge_con_list,
                                           [],
                                           True, 
                                           True)
            if direction == "forward":
                end_set_list.append(set(vertex))
            elif direction == "backward":
                end_set_list.append(set(vertex))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return
            else:
                logger.warning("invalid direction")
                return
        
        intersect = end_set_list[0]
        for i in range(1, len(end_set_list)):
            intersect &= end_set_list[i]

        return list(intersect)
        

    ## one_hop_multi_edge return edges
    ## one_hop_multi_edge does not require type(src) == type(dst)
    def one_hop_multi_edge(self,
                           start_vertex_list,
                           direction,
                           edge_name_list,
                           edge_con_list_list,
                           target_field_list,
                           end_vertex_con_list=None):
        
        res_list = []

        for edge_name in edge_name_list:

            if edge_name not in self.graph_cfg["edges"]:
                logger.warning("invalid edge: " + edge_name)
                return "invalid edge: " + edge_name
            
        for i in range(len(edge_name_list)):

            edge_name = edge_name_list[i]
            edge_con_list = edge_con_list_list[i]

            res = self.one_hop(start_vertex_list, direction, edge_name, edge_con_list, target_field_list)

            res_list.append(res)

        return res_list


    ## multi_hop_multi_edge return edges
    ## multi_hop_multi_edge requires type(src) == type(dst)
    def multi_hop_multi_edge(self,
                             step,
                             start_vertex_list,
                             direction,
                             edge_name_list,
                             edge_con_list_list,
                             target_field_list,
                             only_last_step,
                             plus_last_vertexes=False):

        multi_res = []

        multi_step_start_vertex_list = start_vertex_list

        for i in range(step):

            res = self.one_hop_multi_edge(multi_step_start_vertex_list,
                                          direction,
                                          edge_name_list,
                                          edge_con_list_list,
                                          target_field_list)

            multi_res.append(res)

            #for item in multi_res:
            #    print(item)

            if sum([res_elem.shape[0] for res_elem in res]) == 0:
                logger.warning("multi-hop terminates at " + str(i + 1))
                multi_step_start_vertex_list = []
                break

            if i == step - 1 and not plus_last_vertexes:
                continue

            # TODO: may have performance issue
            if direction == "forward":
                tmp_list = []
                for ii in range(len(edge_name_list)):
                    if res[ii].shape[0] == 0:
                        continue
                    edge_name = edge_name_list[ii]
                    edge_info = self.graph_cfg["edges"][edge_name]
                    tmp_list.append(res[ii][edge_info['dst']].values)
                multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
            elif direction == "backward":
                tmp_list = []
                for ii in range(len(edge_name_list)):
                    if res[ii].shape[0] == 0:
                        continue
                    edge_name = edge_name_list[ii]
                    edge_info = self.graph_cfg["edges"][edge_name]
                    tmp_list.append(res[ii][edge_info['src']].values)
                multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return "bidirectional not implemented"
            else:
                logger.warning("invalid direction")
                return "invalid direction"

        if only_last_step:
            if plus_last_vertexes:
                return (multi_res[-1], multi_step_start_vertex_list)
            else:
                return multi_res[-1]
        else:
            return multi_res


    # multi_hop_multi_edge_common_vertexes return common vertexes
    def multi_hop_multi_edge_common_vertexes(self,
                                             step,
                                             start_vertex_list,
                                             direction,
                                             edge_name_list,
                                             edge_con_list_list):
        
        end_set_list = []
        for i in range(len(start_vertex_list)):
            (res, vertex) = self.multi_hop_multi_edge(step, 
                                                      [start_vertex_list[i]], 
                                                      direction,
                                                      edge_name_list,
                                                      edge_con_list_list,
                                                      [],
                                                      True,
                                                      True)
            if direction == "forward":
                end_set_list.append(set(vertex))
            elif direction == "backward":
                end_set_list.append(set(vertex))
            elif direction == "bidirectional":
                logger.warning("bidirectional not implemented")
                return "bidirectional not implemented"
            else:
                logger.warning("invalid direction")
                return "invalid direction"
        
        intersect = end_set_list[0]
        for i in range(1, len(end_set_list)):
            intersect &= end_set_list[i]

        return list(intersect)
        

    # match_edge returns edges which satisfy constraints
    def match_edge(self,
                   edge_name,
                   edge_con_list,
                   target_field_list,
                   data_type="list"):
        
        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(edge_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select " + target_field_list_con + " from " + db_table + edge_con_list_con
        logger.info("sql: "+sql)
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql)

        return res 


    # match_vertex returns vertexes which satisfy constraints
    def match_vertex(self,
                     vertex_name,
                     vertex_con_list,
                     target_field_list,
                     data_type="list"):
        
        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return "invalid vertex: " + vertex_name

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        vertex_con_list_con = ""
        if vertex_con_list is not None and len(vertex_con_list) > 0:
            vertex_con_list_con = " where " + " and ".join(vertex_con_list)

        target_field_list_con = vertex_info["id"]
        if target_field_list is None:
            target_field_list_con += "," + ",".join(vertex_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select " + target_field_list_con + " from " + db_table + vertex_con_list_con
        logger.info("sql: "+sql)
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql)

        return res 

    # def find_path_multi_edge(self,
    #                          start_vertex_list,
    #                          end_vertex_list,
    #                          edge_name_list,
    #                          edge_con_list_list,
    #                          target_field_list,
    #                          step_limit):
    #     if step_limit > 2:
    #         logger.warning("finding path longer than 2 not implemented")
    #         res2 = self.find_path_multi_edge_s2(start_vertex_list,
    #                                             end_vertex_list,
    #                                             edge_name_list,
    #                                             edge_con_list_list,
    #                                             target_field_list)
    #
    #         res1 = self.find_path_multi_edge_s1(start_vertex_list,
    #                                             end_vertex_list,
    #                                             edge_name_list,
    #                                             edge_con_list_list,
    #                                             target_field_list)
    #         return [res1, res2]
    #
    #     if step_limit > 1:
    #         res2 = self.find_path_multi_edge_s2(start_vertex_list,
    #                                             end_vertex_list,
    #                                             edge_name_list,
    #                                             edge_con_list_list,
    #                                             target_field_list)
    #
    #         res1 = self.find_path_multi_edge_s1(start_vertex_list,
    #                                             end_vertex_list,
    #                                             edge_name_list,
    #                                             edge_con_list_list,
    #                                             target_field_list)
    #         return [res1, res2]
    #
    #     elif step_limit > 0:
    #         res1 = self.find_path_multi_edge_s1(start_vertex_list,
    #                                             end_vertex_list,
    #                                             edge_name_list,
    #                                             edge_con_list_list,
    #                                             target_field_list)
    #         return [res1]
    #
    # def find_path_multi_edge_s1(self,
    #                             start_vertex_list,
    #                             end_vertex_list,
    #                             edge_name_list,
    #                             edge_con_list_list,
    #                             target_field_list):
    #
    #     res_list = []
    #
    #     for i in range(len(edge_name_list)):
    #         edge_name = edge_name_list[i]
    #         edge_con_list = edge_con_list_list[i]
    #         edge_info = self.graph_cfg["edges"][edge_name]
    #         start_vertex_list_con = edge_info["src"] + " in " + tostr(start_vertex_list)
    #         end_vertex_list_con = edge_info["dst"] + " in " + tostr(end_vertex_list)
    #         edge_con_list.append(start_vertex_list_con)
    #         edge_con_list.append(end_vertex_list_con)
    #         res = self.match_edge(edge_name, edge_con_list, target_field_list, data_type="df")
    #         res_list.append(res)
    #
    #     return res_list
    #
    # def find_path_multi_edge_s2(self,
    #                             start_vertex_list,
    #                             end_vertex_list,
    #                             edge_name_list,
    #                             edge_con_list_list,
    #                             target_field_list):
    #
    #     (f_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
    #                                                       edge_name_list, edge_con_list_list,
    #                                                       target_field_list, True, True)
    #
    #     (b_edges, b_vertices) = self.multi_hop_multi_edge(1, end_vertex_list, "backward",
    #                                                       edge_name_list, edge_con_list_list,
    #                                                       target_field_list, True, True)
    #
    #     transit_vertices = np.intersect1d(f_vertices, b_vertices, assume_unique=True)
    #     f_edges_final = []
    #     for df in f_edges:
    #         if type(df) == list:
    #            if len(df) != 0:
    #                df = pd.DataFrame(df)
    #                f_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
    #            else:
    #                f_edges_final.append(pd.DataFrame([]))
    #     b_edges_final = []
    #     for df in b_edges:
    #         if type(df) == list:
    #            if len(df) != 0:
    #                df = pd.DataFrame(df)
    #                b_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])
    #            else:
    #                b_edges_final.append(pd.DataFrame([]))
    #
    #     return [f_edges_final, b_edges_final]

    def find_path_multi_edge(self,
                             start_vertex_list,
                             end_vertex_list,
                             edge_name_list,
                             edge_con_list_list,
                             target_field_list,
                             step_limit):

        if step_limit > 3:
            # logger.warning("finding path longer than 2 not implemented")

            res4 = self.find_path_multi_edge_s4(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res3 = self.find_path_multi_edge_s3(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                 end_vertex_list,
                                                 edge_name_list,
                                                 edge_con_list_list,
                                                 target_field_list)
            
            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                 end_vertex_list,
                                                 edge_name_list,
                                                 edge_con_list_list,
                                                 target_field_list)
            
            return [res1, res2, res3, res4]

        if step_limit > 2:
            res3 = self.find_path_multi_edge_s3(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            # logger.warning("finding path longer than 2 not implemented")
            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                 end_vertex_list,
                                                 edge_name_list,
                                                 edge_con_list_list,
                                                 target_field_list)
 
            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                 end_vertex_list,
                                                 edge_name_list,
                                                 edge_con_list_list,
                                                 target_field_list)
            return [res1, res2, res3]

        if step_limit > 1:
            res2 = self.find_path_multi_edge_s2(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)

            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            return [res1, res2]

        if step_limit > 0:
            res1 = self.find_path_multi_edge_s1(start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                target_field_list)
            return [res1]

    # return path of length 1 (list of df)
    def find_path_multi_edge_s1(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        res_list = []

        for i in range(len(edge_name_list)):
            edge_name = edge_name_list[i]
            edge_con_list = edge_con_list_list[i]
            edge_info = self.graph_cfg["edges"][edge_name]
            start_vertex_list_con = edge_info["src"] + " in " + tostr(start_vertex_list)
            end_vertex_list_con = edge_info["dst"] + " in " + tostr(end_vertex_list)
            edge_con_list.append(start_vertex_list_con)
            edge_con_list.append(end_vertex_list_con)
            res = self.match_edge(edge_name, edge_con_list, target_field_list, data_type="df")
            res_list.append(res)

        return res_list

        # return path of length 2 (list of list of df)

    def find_path_multi_edge_s2(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):


        (f_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                          edge_name_list, edge_con_list_list,
                                                          target_field_list, True, True)

        (b_edges, b_vertices) = self.multi_hop_multi_edge(1, end_vertex_list, "backward",
                                                          edge_name_list, edge_con_list_list,
                                                          target_field_list, True, True)

        transit_vertices = np.intersect1d(f_vertices, b_vertices, assume_unique=True)

        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])]*len(edge_name_list), [pd.DataFrame([])]*len(edge_name_list)]

        f_edges_final = []
        for df in f_edges:
            if len(df) != 0:
                f_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
            else:
                f_edges_final.append(pd.DataFrame([]))
        b_edges_final = []
        for df in b_edges:
            if len(df) != 0:
                b_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])
            else:
                b_edges_final.append(pd.DataFrame([]))
        return [f_edges_final, b_edges_final]


    def find_path_multi_edge_s3(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        # f_vertices is ndarray  & f_edges is list of dataframe
        (first_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                              edge_name_list, edge_con_list_list,
                                                              target_field_list, True, True)
        # f_edges_final, b_edges_final is list of datdaframe
        [second_edges, third_edges_final] = self.find_path_multi_edge_s2(f_vertices.tolist(), end_vertex_list,
                                                                         edge_name_list,
                                                                         edge_con_list_list, target_field_list)

        # for  backward
        if second_edges == "":
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        tmp_list = []
        for ii in range(len(edge_name_list)):
            if second_edges[ii].shape[0] == 0:
                continue
            edge_name = edge_name_list[ii]
            edge_info = self.graph_cfg["edges"][edge_name]
            tmp_list.append(second_edges[ii][edge_info['src']].values)
        if tmp_list==[]:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list)]
        multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        transit_vertices = np.intersect1d(f_vertices, multi_step_start_vertex_list, assume_unique=True)
        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        first_edges_final = []
        for df in first_edges:
            if df.empty:
                first_edges_final.append(pd.DataFrame([]))
                continue
            first_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
        second_edges_final = []
        for df in second_edges:
            if df.empty:
                second_edges_final.append(pd.DataFrame([]))
                continue
            second_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])

        return [first_edges_final, second_edges_final, third_edges_final]


    def find_path_multi_edge_s4(self,
                                start_vertex_list,
                                end_vertex_list,
                                edge_name_list,
                                edge_con_list_list,
                                target_field_list):

        # f_vertices is ndarray  & f_edges is list of dataframe
        (first_edges, f_vertices) = self.multi_hop_multi_edge(1, start_vertex_list, "forward",
                                                              edge_name_list, edge_con_list_list,
                                                              target_field_list, True, True)
        # f_edges_final, b_edges_final is list of datdaframe
        [second_edges, third_edges_final, fourth_edges_final] = self.find_path_multi_edge_s3(f_vertices.tolist(),
                                                                                             end_vertex_list,
                                                                                             edge_name_list,
                                                                                             edge_con_list_list,
                                                                                             target_field_list)
        if second_edges == "":
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),[pd.DataFrame([])] * len(edge_name_list)]
        tmp_list = []
        for ii in range(len(edge_name_list)):
            if second_edges[ii].shape[0] == 0:
                continue
            edge_name = edge_name_list[ii]
            edge_info = self.graph_cfg["edges"][edge_name]
            tmp_list.append(second_edges[ii][edge_info['src']].values)
        if tmp_list==[]:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),
                    [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list)]
        multi_step_start_vertex_list = np.unique(np.concatenate(tmp_list))
        transit_vertices = np.intersect1d(f_vertices, multi_step_start_vertex_list, assume_unique=True)
        if len(transit_vertices) == 0:
            return [[pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list), [pd.DataFrame([])] * len(edge_name_list),[pd.DataFrame([])] * len(edge_name_list)]
        first_edges_final = []
        for df in first_edges:
            if df.empty:
                first_edges_final.append(pd.DataFrame([]))
                continue
            first_edges_final.append(df[df.iloc[:, 1].isin(transit_vertices)])
        second_edges_final = []
        for df in second_edges:
            if df.empty:
                second_edges_final.append(pd.DataFrame([]))
                continue
            second_edges_final.append(df[df.iloc[:, 0].isin(transit_vertices)])

        return [first_edges_final, second_edges_final, third_edges_final, fourth_edges_final]




        #############################################
        #################### subgraph
        #############################################

        # subgraph_name is recommended to be unique (ex. plus timestamp)

    def create_subgraph(self, subgraph_name):

        self.client.execute("create database if not exists " + subgraph_name)
        try:
            for name in self.graph_cfg["edges"]:
                info = self.graph_cfg["edges"][name]
                new_name = subgraph_name + "." + info['table']
                old_name = info['db'] + "." + info['table']
                self.client.execute("create table " + new_name + " as " + old_name)
            for name in self.graph_cfg["vertexes"]:
                info = self.graph_cfg["vertexes"][name]
                new_name = subgraph_name + "." + info['table']
                old_name = info['db'] + "." + info['table']
                self.client.execute("create table " + new_name + " as " + old_name)
        except Exception as e:
            print(e)
            return "subgraph is already exist or something wrong"
        import copy
        subgraph_cfg = copy.deepcopy(self.graph_cfg)
        for name in subgraph_cfg["edges"]:
            subgraph_cfg["edges"][name]["db"] = subgraph_name
        for name in subgraph_cfg["vertexes"]:
            subgraph_cfg["vertexes"][name]["db"] = subgraph_name
        subgraph_cfg["subgraph"] = self.graph_name
        return self.register_graph(subgraph_name, json.dumps(subgraph_cfg))

    def update_subgraph_by_multi_hop_multi_edge(self,
                                                subgraph_name,
                                                step,
                                                start_vertex_list,
                                                direction,
                                                edge_name_list,
                                                edge_con_list_list):

        multi_res = self.multi_hop_multi_edge(step, start_vertex_list, direction,
                                              edge_name_list, edge_con_list_list, None, False, False)


        try:
            for single_res in multi_res:
                for i in range(len(edge_name_list)):
                    if single_res[i].shape[0] == 0:
                        continue
                    edge_info = self.graph_cfg["edges"][edge_name_list[i]]
                    db_table = subgraph_name + "." + edge_info["table"]
                    target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + ",".join(
                        edge_info["fields"])
                    # TODO: list hurts performance and increases memory cost
                    # datetime64[ns] patch
                    # col_list = [list(single_res[i][col].values) for col in single_res[i].columns]
                    col_list = [list(pd.to_datetime(single_res[i][col])) if str(
                        single_res[i][col].dtype) == "datetime64[ns]" else list(single_res[i][col].values) for col in
                                single_res[i].columns]
                    self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values", col_list,
                                        columnar=True)

                    src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                    src_db_table_new = subgraph_name + "." + src_info["table"]
                    src_db_table_old = src_info["db"] + "." + src_info["table"]
                    src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                    self.client.execute(
                        "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                        src_info["id"] + " in " + tostr(col_list[0]))
                    dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                    dst_db_table_new = subgraph_name + "." + dst_info["table"]
                    dst_db_table_old = dst_info["db"] + "." + dst_info["table"]
                    dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                    self.client.execute(
                        "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                        dst_info["id"] + " in " + tostr(col_list[1]))
            return "The subgraph is update success"
        except Exception as e:
            print(e)
            return "The subgraph is update failed"
       

    def update_subgraph_by_match_edge(self,
                                      subgraph_name,
                                      edge_name,
                                      edge_con_list):

        res = self.match_edge(edge_name, edge_con_list, None, data_type='df')
        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = subgraph_name + "." + edge_info["table"]
        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + ",".join(edge_info["fields"])
        # TODO: list hurts performance and increases memory cost
        col_list = [list(pd.to_datetime(res[col])) if str(res[col].dtype) == "datetime64[ns]" else list(res[col].values) for col in res.columns]
        try:
            self.client.execute("insert into "+db_table+" ("+target_field_list_con+") values", col_list, columnar=True)

            src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
            src_db_table_new = subgraph_name + "." + src_info["table"]
            src_db_table_old = src_info["db"] + "." + src_info["table"]
            src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
            self.client.execute(
                "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                src_info["id"] + " in " + tostr(col_list[0]))
            dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
            dst_db_table_new = subgraph_name + "." + dst_info["table"]
            dst_db_table_old = dst_info["db"] + "." + dst_info["table"]
            dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
            self.client.execute(
                "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                dst_info["id"] + " in " + tostr(col_list[1]))

            return "The subgraph update success"
        except Exception as e:
            print(e)
            return "The subgraph update failed"

    def update_subgraph_by_find_path_multi_edge(self,
                                                subgraph_name,
                                                start_vertex_list,
                                                end_vertex_list,
                                                edge_name_list,
                                                edge_con_list_list,
                                                step_limit):

        res = self.find_path_multi_edge(start_vertex_list, end_vertex_list,
                                        edge_name_list, edge_con_list_list,
                                        None, step_limit)

        for i in range(len(res)):
            if i == 0:  # path of length 1
                for k in range(len(edge_name_list)):
                    if res[i][k].shape[0] == 0:
                        continue
                    edge_info = self.graph_cfg["edges"][edge_name_list[k]]
                    db_table = subgraph_name + "." + edge_info["table"]
                    target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + ",".join(
                        edge_info["fields"])
                    # TODO: list hurts performance and increases memory cost
                    # datetime64[ns] patch
                    # col_list = [list(res[i][k][col].values) for col in res[i][k].columns]
                    col_list = [
                        list(pd.to_datetime(res[i][k][col])) if str(res[i][k][col].dtype) == "datetime64[ns]" else list(
                            res[i][k][col].values) for col in res[i][k].columns]
                    self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values", col_list,
                                        columnar=True)
                    src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                    src_db_table_new = subgraph_name + "." + src_info["table"]
                    src_db_table_old = src_info["db"] + "." + src_info["table"]
                    src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                    self.client.execute(
                        "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                        src_info["id"] + " in " + tostr(col_list[0]))
                    dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                    dst_db_table_new = subgraph_name + "." + dst_info["table"]
                    dst_db_table_old = dst_info["db"] + "." + dst_info["table"]
                    dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                    self.client.execute(
                        "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                        dst_info["id"] + " in " + tostr(col_list[1]))

            else:  # path of length >=2
                for j in range(len(res[i])):
                    for k in range(len(edge_name_list)):
                        if res[i][j][k].shape[0] == 0:
                            continue
                        edge_info = self.graph_cfg["edges"][edge_name_list[k]]
                        db_table = subgraph_name + "." + edge_info["table"]
                        target_field_list_con = edge_info["src"] + "," + edge_info["dst"] + "," + ",".join(
                            edge_info["fields"])
                        # TODO: list hurts performance and increases memory cost
                        # datetime64[ns] patch
                        # col_list = [list(res[i][j][k][col].values) for col in res[i][j][k].columns]
                        col_list = [list(pd.to_datetime(res[i][j][k][col])) if str(
                            res[i][j][k][col].dtype) == "datetime64[ns]" else list(res[i][j][k][col].values) for col in
                                    res[i][j][k].columns]
                        self.client.execute("insert into " + db_table + " (" + target_field_list_con + ") values",
                                            col_list, columnar=True)
                        src_info = self.graph_cfg["vertexes"][edge_info["src_type"]]
                        src_db_table_new = subgraph_name + "." + src_info["table"]
                        src_db_table_old = src_info["db"] + "." + src_info["table"]
                        src_target_field_list_con = src_info["id"] + "," + ",".join(src_info["fields"])
                        self.client.execute(
                            "insert into " + src_db_table_new + " (" + src_target_field_list_con + ") select " + src_target_field_list_con + " from " + src_db_table_old + " where " +
                            src_info["id"] + " in " + tostr(col_list[0]))
                        dst_info = self.graph_cfg["vertexes"][edge_info["dst_type"]]
                        dst_db_table_new = subgraph_name + "." + dst_info["table"]
                        dst_db_table_old = dst_info["db"] + "." + dst_info["table"]
                        dst_target_field_list_con = dst_info["id"] + "," + ",".join(dst_info["fields"])
                        self.client.execute(
                            "insert into " + dst_db_table_new + " (" + dst_target_field_list_con + ") select " + dst_target_field_list_con + " from " + dst_db_table_old + " where " +
                            dst_info["id"] + " in " + tostr(col_list[1]))

    def destroy_subgraph(self, subgraph_name):

        graph_name = self.graph_name
        self.use_graph(subgraph_name)
        if "subgraph" not in self.graph_cfg or self.graph_cfg["subgraph"] != graph_name:
            logger.warning("not subgraph or graph-subgraph unmatched")
            self.use_graph(graph_name)
            return "not subgraph or graph-subgraph unmatched"
        self.use_graph(graph_name)

        self.delete_graph(subgraph_name)
        self.client.execute("drop database if exists " + subgraph_name)
        return "destroy subgraph success"

    #############################################
    #################### vertex/edge-wise operation: metric
    #############################################
    ## metric_indegree returns indegree of vertices (df)
    ## vertices without in-edge will be ignored
    def metric_indegree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by indegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["dst"] + ", count(*) as indegree from " + db_table + " group by " + edge_info[
            "dst"] + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## metric_outdegree returns outdegree of vertices (df)
    ## vertices without out-edge will be ignored
    def metric_outdegree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return "invalid edge: " + edge_name

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by outdegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["src"] + ", count(*) as outdegree from " + db_table + " group by " + edge_info[
            "src"] + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## metric_degree returns degree of vertices (df)
    ## vertices without edge will be ignored
    def metric_degree(self, edge_name, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by degree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql_o = "select " + edge_info["src"] + " as vid, count(*) as degree from " + db_table + " group by " + \
                edge_info["src"]
        sql_i = "select " + edge_info["dst"] + " as vid, count(*) as degree from " + db_table + " group by " + \
                edge_info["dst"]
        sql = "select vid, sum(degree) as degree from (" + sql_o + " union all " + sql_i + ") group by vid" + qualifier
        logger.info("sql: " + sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    ## TODO
    ## metric_pagerank returns pagerank of vertices
    ## vertices without edge will be ignored
    def metric_pagerank(self, edge_name, d=0.85, num_iter=10, if_sort=False, topk=-1):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        qualifier = ""
        if if_sort:
            qualifier += " order by outdegree desc"
        if topk > 0:
            qualifier += " limit " + str(topk)

        sql = "select " + edge_info["src"] + "," + edge_info["dst"] + ",outdegree from (select " + edge_info[
            "src"] + ",count(*) as outdegree from " + db_table + " group by " + edge_info[
                  "src"] + ") as table_od join " + db_table + " using " + edge_info["src"] + qualifier
        print(sql)
        res = self.client.query_dataframe(sql)
        return res.to_dict()

    def vertex_match_property(self, vertex_id_list, vertex_name, vertex_con_list, target_field_list, data_type="list"):
        propertys = self.graph_cfg["vertexes"]
        table_property = propertys[vertex_name]
        db_table = table_property["db"] + "." + table_property["table"]
        target_field_list_con = table_property["id"]
        if target_field_list is None or len(target_field_list) == 0:
            target_field_list_con += "," + ",".join(table_property["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)
        vertex_con_list_con = " where " + table_property["id"] + " in " + tostr(vertex_id_list)
        if vertex_con_list is not None and len(vertex_con_list) > 0:
            vertex_con_list_con += " and " + " and ".join(vertex_con_list)
        sql = "select DISTINCT " + target_field_list_con + " from " + db_table + vertex_con_list_con
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql).values.tolist()
        return res

    def edge_match_property(self, start_vertex_list, end_vertex_list, edge_name, edge_con_list, target_field_list,
                            data_type="list"):
        propertys = self.graph_cfg["edges"]
        table_property = propertys[edge_name]
        db_table = table_property["db"] + "." + table_property["table"]
        target_field_list_con = table_property["src"] + "," + table_property["dst"]
        if target_field_list is None or len(target_field_list)==0:
            target_field_list_con += "," + ",".join(table_property["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)
        edge_con_list_con = " where " + table_property["src"] + " in " + tostr(start_vertex_list) + " and " \
                            + table_property["dst"] + " in " + tostr(end_vertex_list)
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con += " and " + " and ".join(edge_con_list)
        sql = "select DISTINCT " + target_field_list_con + " from " + db_table + edge_con_list_con
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql).values.tolist()
        return res

    # query_vertex returns distinct vertexes which satisfy constraints (df)
    def query_vertexes(self,
                     vertex_name,
                     vertex_con_list,
                     target_field_list,
                     data_type="list"):

        if vertex_name not in self.graph_cfg["vertexes"]:
            logger.warning("invalid vertex: " + vertex_name)
            return

        vertex_info = self.graph_cfg["vertexes"][vertex_name]
        db_table = vertex_info["db"] + "." + vertex_info["table"]

        vertex_con_list_con = ""
        if vertex_con_list is not None and len(vertex_con_list) > 0:
            vertex_con_list_con = " where " + " and ".join(vertex_con_list)

        target_field_list_con = vertex_info["id"]
        if target_field_list is None or len(target_field_list) == 0:
            target_field_list_con += "," + ",".join(vertex_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select distinct " + target_field_list_con + " from " + db_table + vertex_con_list_con
        logger.info("sql: " + sql)
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql).values.tolist()

        return res

    # query_edge returns distinct edges which satisfy constraints (df)
    def query_edges(self,
                   edge_name,
                   edge_con_list,
                   target_field_list,
                   data_type="list"):

        if edge_name not in self.graph_cfg["edges"]:
            logger.warning("invalid edge: " + edge_name)
            return

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        target_field_list_con = edge_info["src"] + "," + edge_info["dst"]
        if target_field_list is None or len(target_field_list) == 0:
            target_field_list_con += "," + ",".join(edge_info["fields"])
        elif len(target_field_list) > 0:
            target_field_list_con += "," + ",".join(target_field_list)

        sql = "select distinct " + target_field_list_con + " from " + db_table + edge_con_list_con
        logger.info("sql: " + sql)
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql).values.tolist()

        return res

    # def time_static_subgraph(self, subgraph_name, edge_name, edge_con_list, time_dimention='Day', data_type='list'):
    #
    #     graph_name = self.graph_name
    #     self.use_graph(subgraph_name)
    #     if "subgraph" not in self.graph_cfg or self.graph_cfg["subgraph"] != graph_name:
    #         logger.warning("not subgraph or graph-subgraph unmatched")
    #         self.use_graph(graph_name)
    #         return
    #     self.use_graph(subgraph_name)
    #     edge_info = self.graph_cfg["edges"][edge_name]['db'] + "." + self.graph_cfg["edges"][edge_name]['table']
    #     edge_con_list_con = ""
    #     if edge_con_list is not None and len(edge_con_list) > 0:
    #         edge_con_list_con = " where " + " and ".join(edge_con_list)
    #     sub_sql = "select distinct * from " + edge_info + edge_con_list_con
    #     sql = "select A.record_date, count() from " + "(" + sub_sql + ")" + " as A GROUP BY A.record_date"
    #     if time_dimention == 'Minute':
    #         sql = "select toStartOfMinute(A.record_time) as Minute,count() from " + "(" + sub_sql + ")" + " as A GROUP BY Minute"
    #     elif time_dimention == 'Hour':
    #         sql = "select toStartOfHour(A.record_time) as Hour, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Hour"
    #     elif time_dimention == 'Day':
    #         sql = "select formatDateTime(A.record_time,'%F') as Day, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Day"
    #     elif time_dimention == 'Month':
    #         sql = "select toStartOfMonth(A.record_time) as Month, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Month"
    #     elif time_dimention == 'Year':
    #         sql = "select formatDateTime(A.record_time,'%Y') as Year, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Year"
    #     # sql1 = "select formatDateTime(record_time,'%Y') as Year,toStartOfMonth(record_time),toStartOfDay(record_time),toStartOfHour(record_time),toStartOfMinute(record_time),record_time from  sub_anti_money_laundry2.accounts limit 10"
    #
    #     if data_type == "list":
    #         res = self.client.execute(sql)
    #     elif data_type == "df":
    #         res = self.client.query_dataframe(sql)
    #
    #     return res

    def count_edge_by_time(self, edge_name, edge_con_list, time_field, time_dimention='Day', data_type='df'):

        edge_info = self.graph_cfg["edges"][edge_name]
        db_table = edge_info["db"] + "." + edge_info["table"]

        edge_con_list_con = ""
        if edge_con_list is not None and len(edge_con_list) > 0:
            edge_con_list_con = " where " + " and ".join(edge_con_list)

        sub_sql = "select distinct * from " + db_table + edge_con_list_con
        sql = "select A." + time_field + ", count() from " + "(" + sub_sql + ")" + " as A GROUP BY A." + time_field
        if time_dimention == 'Minute':
            sql = "select toStartOfMinute(A." + time_field + ") as Minute, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Minute"
        elif time_dimention == 'Hour':
            sql = "select toStartOfHour(A." + time_field + ") as Hour, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Hour"
        elif time_dimention == 'Day':
            sql = "select formatDateTime(A." + time_field + ",'%F') as Day, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Day"
        elif time_dimention == 'Month':
            sql = "select toStartOfMonth(A." + time_field + ") as Month, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Month"
        elif time_dimention == 'Year':
            sql = "select formatDateTime(A." + time_field + ",'%Y') as Year, count() from " + "(" + sub_sql + ")" + " as A GROUP BY Year"
        # sql1 = "select formatDateTime(record_time,'%Y') as Year,toStartOfMonth(record_time),toStartOfDay(record_time),toStartOfHour(record_time),toStartOfMinute(record_time),record_time from  sub_anti_money_laundry2.accounts limit 10"

        print(sql)
        if data_type == "list":
            res = self.client.execute(sql)
        elif data_type == "df":
            res = self.client.query_dataframe(sql).values.tolist()

        return res











