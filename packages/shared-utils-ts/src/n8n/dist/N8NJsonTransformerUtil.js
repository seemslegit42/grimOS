"use strict";
exports.__esModule = true;
exports.n8nJsonTransformer = exports.transformFromN8nJson = exports.transformToN8nJson = void 0;
/**
 * Transforms React Flow nodes and edges to n8n workflow JSON.
 */
exports.transformToN8nJson = function (flowNodes, flowEdges, workflowName, workflowIsActive) {
    if (workflowName === void 0) { workflowName = 'My Spell'; }
    if (workflowIsActive === void 0) { workflowIsActive = true; }
    var n8nNodes = flowNodes.map(function (flowNode) {
        var data = flowNode.data, position = flowNode.position, id = flowNode.id;
        return {
            id: id,
            name: data.label || data.n8nNodeType || 'Unnamed Rune',
            type: data.n8nNodeType || 'n8n-nodes-base.unknown',
            typeVersion: 1,
            position: [position.x, position.y],
            parameters: data.parameters || {}
        };
    });
    var n8nConnections = {};
    flowEdges.forEach(function (edge) {
        var sourceHandle = edge.sourceHandle || 'main'; // Default n8n output port
        var targetHandle = edge.targetHandle || 'main'; // Default n8n input port
        if (!n8nConnections[edge.source]) {
            n8nConnections[edge.source] = {};
        }
        if (!n8nConnections[edge.source][sourceHandle]) {
            n8nConnections[edge.source][sourceHandle] = [];
        }
        n8nConnections[edge.source][sourceHandle].push({
            node: edge.target,
            input: targetHandle
        });
    });
    return {
        name: workflowName,
        nodes: n8nNodes,
        connections: n8nConnections,
        active: workflowIsActive,
        settings: {}
    };
};
/**
 * Transforms n8n workflow JSON to React Flow nodes and edges.
 */
exports.transformFromN8nJson = function (n8nWorkflow) {
    var flowNodes = n8nWorkflow.nodes.map(function (n8nNode) {
        return {
            id: n8nNode.id,
            type: 'GrimOSRuneNode',
            position: { x: n8nNode.position[0], y: n8nNode.position[1] },
            data: {
                label: n8nNode.name,
                n8nNodeType: n8nNode.type,
                parameters: n8nNode.parameters
            }
        };
    });
    var flowEdges = [];
    Object.entries(n8nWorkflow.connections).forEach(function (_a) {
        var sourceNodeId = _a[0], connectionEntry = _a[1];
        Object.entries(connectionEntry).forEach(function (_a) {
            var outputPortName = _a[0], targets = _a[1];
            targets.forEach(function (target, index) {
                var edgeId = "edge-" + sourceNodeId + "-" + outputPortName + "-" + target.node + "-" + target.input + "-" + index;
                flowEdges.push({
                    id: edgeId,
                    source: sourceNodeId,
                    target: target.node,
                    sourceHandle: outputPortName,
                    targetHandle: target.input,
                    type: 'GrimOSConnectionLine'
                });
            });
        });
    });
    return {
        flowNodes: flowNodes,
        flowEdges: flowEdges
    };
};
exports.n8nJsonTransformer = {
    transformToN8nJson: exports.transformToN8nJson,
    transformFromN8nJson: exports.transformFromN8nJson
};
