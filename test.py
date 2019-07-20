from neo4j_common import command





command("CALL algo.unionFind.stream('top1000', 'KNOWS', {weightProperty:'weight', defaultValue:0.0, threshold:100.0,concurrency:1}) YIELD nodeId,setId RETURN nodeId,algo.asNode(nodeId).显示名称 AS user, setId")

