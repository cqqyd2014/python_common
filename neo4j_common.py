import json
from neo4j import GraphDatabase
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash,jsonify
#from mosr_back_orm.orm import create_session,SystemPar,init_db,SystemCode,ProcessDetail,SystemData
bolt_conncect_string='bolt://localhost:7687'
user='neo4j'
password='Wang1980'







def getJson(cypher_sql):
        driver=GraphDatabase.driver(bolt_conncect_string, auth=(user, password))
        with driver.session() as session:
            result = session.run(cypher_sql).data()
            
            

            
            session.close()
            return jsonify(result)


def command(command_sql,do_record):
        driver=GraphDatabase.driver(bolt_conncect_string, auth=(user, password))
        with driver.session() as session:
            result=session.run(command_sql)
            records=result.records()
            do_record(records)
            

            
            session.close()
           



def getPath(cypher_sql):
        driver=GraphDatabase.driver(bolt_conncect_string, auth=(user, password))
        with driver.session() as session:
            result = session.run(cypher_sql)
            graph=result.graph()
            nodes=graph.nodes
            nodes_object=[]
            nodes_new=[]
            for node in nodes:
                node_object=buildNodes(node)
                nodes_object.append(node_object)
            #node的label可能为中文，需要转换为可以识别的类型，并给出对应列表,label不改变，将classes定义为随机生成的。c1，c2，c3
            #提取可用的颜色列表
            db_session=create_session()
            systemCodes=db_session.query(SystemCode).filter(SystemCode.code_main=='node_color').all()
            colors=[]
            for sc in systemCodes:
                colors.append(sc.code_code)
            db_session.close()
            #处理classes
            nodes_colors={}#{'企业-abc,'#666666'}
            flag=0
            for node in nodes_object:
                data=node["data"]
                _label=data["label"]
                if _label not in nodes_colors:
                        #不存在，是新的
                    nodes_colors[_label]=colors[flag%len(colors)]
                    flag+=1
                else:
                    pass
               
            relationships_object=[]
            relationships_colors={}
            
            relationships=graph.relationships
            #print(len(relationships))
            flag=0
            for r in relationships:
                #print(flag)
                flag+=1
                r_object=buildEdges(r)
                relationships_object.append(r_object)
                data=r_object['data']
                #relationship的颜色
                if data['label'] not in relationships_colors:
                    relationships_colors[data['label']]=colors[flag%len(colors)]
                    flag+=1
                #data['line-color']='#'+relationships_colors[data['label']]

            
            session.close()
            #print(len(relationships_object))
            return jsonify(elements = {"nodes": nodes_object, "edges": relationships_object,"colors":nodes_colors,"edge_colors":relationships_colors})


def createEdge(data,type):
        #CREATE (a)-[r:RELTYPE { name: a.name + b.name}] -> (b)
        temp_string=''
        start=''
        end=''
        for key,value in data.items():
                if (key=='START'):
                        start=value
                elif(key=='END'):
                        end=value
                else:
                        temp_string+=key+":\'"+value+"\',"
        temp_string="{"+temp_string[:len(temp_string)-1]+"}"
        create_string='MATCH (a),(b) WHERE a.ID = "'+start+'" AND b.ID = "'+end+'"CREATE (a)-[r:'+type+' '+temp_string+']->(b)'
        
        return create_string


def createNode(data,type,labels):
        #CREATE(n:TEST {name:'TEST-NAME', age:1})
        #print(data)
        #labels.append(type)
        labels_string=''
        for label in labels:
                labels_string+=":"+label
        labels_string+=":"+type

        
        #去除key上的双引号
        temp_string=''
        for key,value in data.items():
                temp_string+=key+":\'"+value+"\',"
        temp_string="{"+temp_string[:len(temp_string)-1]+"}"
        
        
        
        create_string='CREATE(n'+labels_string+' '+temp_string+")"
        return create_string


def buildNodes(nodeRecord):
        #print(nodeRecord)
        labels=[]
        for label in nodeRecord.labels:
                labels.append(label)
        items={}
        name=""
        for item in nodeRecord.items():
                
                items[item[0]]=item[1]
                #print(item)
                if item[0]=="显示名称":
                        name=item[1]
        #label为labels数组的多个形成的组合，用-连接
        label='-'.join(labels)
        
        data = {"id": str(nodeRecord.id), "label":label,"labels": labels,'name':name}
        data.update(items)
        #data["classes"]=labels
        #print(data)
        return {"data": data}

def buildEdges(relationRecord):
        #print(relationRecord)
        items={}
        for item in relationRecord.items():
                items[item[0]]=item[1]

        data = {"id":str(relationRecord.id),"source": str(relationRecord.start_node.id),"target": str(relationRecord.end_node.id),"label": relationRecord.type}
        data.update(items)
        return {"data": data}