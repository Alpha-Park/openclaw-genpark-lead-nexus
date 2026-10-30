# -*- coding: utf-8 -*-
import sys, json
from client import OpenClawGenParkLeadNexus

client = OpenClawGenParkLeadNexus()

TOOLS = [
    {
        "name": "calculate_pagerank_influence",
        "description": "Calculates PageRank influence centrality across enterprise account networks.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "graph": {"type": "object"},
                "damping": {"type": "number"},
                "max_iter": {"type": "integer"}
            },
            "required": ["graph"]
        }
    },
    {
        "name": "predict_adamic_adar_links",
        "description": "Predicts expansion opportunities using Adamic-Adar common neighbor index.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "graph": {"type": "object"},
                "source_node": {"type": "string"},
                "top_k": {"type": "integer"}
            },
            "required": ["graph", "source_node"]
        }
    },
    {
        "name": "evaluate_champion_mobility",
        "description": "Models conversion probability when an executive moves to a new target account.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "past_account": {"type": "string"},
                "new_account": {"type": "string"},
                "tenure_months": {"type": "number"},
                "previous_satisfaction_score": {"type": "number"}
            },
            "required": ["past_account", "new_account", "tenure_months", "previous_satisfaction_score"]
        }
    }
]

def handle_request(req):
    method = req.get("method")
    rid = req.get("id")
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    elif method == "tools/call":
        params = req.get("params", {})
        tname = params.get("name")
        args = params.get("arguments", {})
        if tname == "calculate_pagerank_influence":
            res = client.calculate_pagerank_influence(args["graph"], args.get("damping"), args.get("max_iter", 50))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "predict_adamic_adar_links":
            res = client.predict_adamic_adar_links(args["graph"], args["source_node"], args.get("top_k", 5))
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        elif tname == "evaluate_champion_mobility":
            res = client.evaluate_champion_mobility(args["past_account"], args["new_account"], args["tenure_months"], args["previous_satisfaction_score"])
            return {"jsonrpc": "2.0", "id": rid, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32600, "message": "Invalid Request"}}

def main():
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
