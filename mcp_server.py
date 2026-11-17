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
            try:
                req = json.loads(line)
            except json.JSONDecodeError as exc:
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}}), flush=True)
                continue
            if not isinstance(req, dict) or req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str):
                print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "Invalid Request"}}), flush=True)
                continue
            # JSON-RPC notifications never receive a response or execute request-only tools.
            if "id" not in req:
                continue
            if req["method"] == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {
                    "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
                    "serverInfo": {"name": 'openclaw-genpark-lead-nexus', "version": "1.0.0"}
                }}), flush=True)
                continue
            if req["method"] == "ping":
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": {}}), flush=True)
                continue
            if req["method"] not in ("tools/list", "tools/call"):
                print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": "Method not found"}}), flush=True)
                continue
            if req["method"] == "tools/call":
                params = req.get("params")
                if not isinstance(params, dict) or not isinstance(params.get("arguments", {}), dict) or params.get("name") not in ('calculate_pagerank_influence', 'predict_adamic_adar_links', 'evaluate_champion_mobility'):
                    print(json.dumps({"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": "Unknown tool or invalid arguments"}}), flush=True)
                    continue
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id") if isinstance(req, dict) else None, "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
