"""
Model Context Protocol (MCP) Server for NeuroOps Duo.
Complies with Anthropic MCP specifications.
Exposes tools to GitLab Duo Agent Platform for DevSecOps automation.
"""
import sys
import json
import logging
from typing import Dict, Any, List

from mcp_server.tools import (
    tool_get_carbon_metrics,
    tool_find_greenest_gcp_region,
    tool_run_mutation_verification,
    tool_deploy_google_cloud_run,
    tool_query_cloud_monitoring_telemetry,
    tool_execute_canary_rollback,
    tool_generate_slsa_provenance
)

# Registry of MCP tools
TOOL_REGISTRY = {
    "get_carbon_metrics": tool_get_carbon_metrics,
    "find_greenest_gcp_region": tool_find_greenest_gcp_region,
    "run_mutation_verification": tool_run_mutation_verification,
    "deploy_google_cloud_run": tool_deploy_google_cloud_run,
    "query_cloud_monitoring_telemetry": tool_query_cloud_monitoring_telemetry,
    "execute_canary_rollback": tool_execute_canary_rollback,
    "generate_slsa_provenance": tool_generate_slsa_provenance
}

def list_tools() -> List[Dict[str, Any]]:
    """Returns the list of MCP tool schemas for GitLab Duo Agent discovery."""
    return [
        {
            "name": "get_carbon_metrics",
            "description": "Calculates ISO/IEC 21031 SCI carbon footprint metrics for a Google Cloud region.",
            "parameters": {
                "type": "object",
                "properties": {
                    "region": {"type": "string", "description": "e.g. europe-north1, us-central1"},
                    "execution_seconds": {"type": "number", "default": 60.0}
                },
                "required": ["region"]
            }
        },
        {
            "name": "find_greenest_gcp_region",
            "description": "Determines the lowest carbon Google Cloud region based on real-time grid carbon intensity.",
            "parameters": {
                "type": "object",
                "properties": {
                    "candidates": {"type": "array", "items": {"type": "string"}}
                }
            }
        },
        {
            "name": "run_mutation_verification",
            "description": "Executes mutation testing against candidate patches to ensure zero regressions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "test_path": {"type": "string", "description": "Path to test suite"}
                },
                "required": ["test_path"]
            }
        },
        {
            "name": "deploy_google_cloud_run",
            "description": "Progressively deploys container to Google Cloud Run with canary traffic splitting.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"},
                    "region": {"type": "string"},
                    "image_tag": {"type": "string"},
                    "traffic_split_percent": {"type": "integer", "default": 100}
                },
                "required": ["service_name", "region"]
            }
        },
        {
            "name": "query_cloud_monitoring_telemetry",
            "description": "Fetches Google Cloud Monitoring telemetry to evaluate error budget and latency.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"},
                    "window_seconds": {"type": "integer", "default": 60}
                },
                "required": ["service_name"]
            }
        },
        {
            "name": "execute_canary_rollback",
            "description": "Executes immediate micro-rollback on Cloud Run if telemetry alerts are raised.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"},
                    "target_revision": {"type": "string"}
                },
                "required": ["service_name", "target_revision"]
            }
        },
        {
            "name": "generate_slsa_provenance",
            "description": "Generates cryptographically signed SLSA Level 3 provenance and SOC2 audit metadata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {"type": "string"},
                    "commit_sha": {"type": "string"},
                    "image_digest": {"type": "string"}
                },
                "required": ["service_name", "commit_sha"]
            }
        }
    ]

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatches tool call to appropriate handler."""
    if tool_name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {tool_name}"}
    handler = TOOL_REGISTRY[tool_name]
    try:
        return handler(**arguments)
    except Exception as e:
        return {"error": f"Execution error in {tool_name}: {str(e)}"}

def run_stdio_server():
    """Runs standard input/output JSON-RPC server for Anthropic MCP clients."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")
            params = req.get("params", {})

            if method == "tools/list":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list_tools()}}
            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = dispatch_tool_call(tool_name, arguments)
                response = {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(result)}]}}
            else:
                response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"MCP Server error: {e}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--list-tools":
        print(json.dumps(list_tools(), indent=2))
    else:
        run_stdio_server()
