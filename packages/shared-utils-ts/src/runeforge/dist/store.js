"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
exports.__esModule = true;
exports.initialSpellMetadata = exports.createRuneForgeStore = void 0;
var reactflow_1 = require("reactflow");
var zustand_1 = require("zustand");
var N8NJsonTransformerUtil_1 = require("../n8n/N8NJsonTransformerUtil");
/**
 * Create a RuneForge store
 * @param config Optional configuration for customizing the store behavior
 * @returns A Zustand store with RuneForge state and actions
 */
exports.createRuneForgeStore = function (_a) {
    var _b = _a === void 0 ? {} : _a, 
    // Optional API client for backend communication
    _c = _b.apiClient, 
    // Optional API client for backend communication
    apiClient = _c === void 0 ? null : _c, 
    // Debug mode for logging store actions
    _d = _b.debug, 
    // Debug mode for logging store actions
    debug = _d === void 0 ? false : _d;
    return zustand_1.create(function (set, get) { return ({
        // Initial state
        available_runes: [],
        spellMetadata: {
            id: null,
            name: 'New Spell',
            description: '',
            isPublic: false,
            isTemplate: false
        },
        current_spell_id: null,
        current_spell_name: 'New Spell',
        flow_nodes: [],
        flow_edges: [],
        selected_node_id: null,
        is_loading_spell: false,
        is_saving_spell: false,
        canvas_error: null,
        // Actions
        setSpellMetadata: function (metadata) {
            if (debug)
                console.log('[RuneForgeStore] setSpellMetadata', metadata);
            set({ spellMetadata: metadata });
        },
        setSpellData: function (data) {
            if (debug)
                console.log('[RuneForgeStore] setSpellData', data);
            set({
                current_spell_id: data.id,
                current_spell_name: data.name,
                flow_nodes: data.nodes,
                flow_edges: data.edges,
                selected_node_id: null,
                canvas_error: null
            });
        },
        addFlowNode: function (node) {
            if (debug)
                console.log('[RuneForgeStore] addFlowNode', node);
            set(function (state) { return ({
                flow_nodes: __spreadArrays(state.flow_nodes, [node])
            }); });
        },
        deleteFlowNode: function (nodeId) {
            if (debug)
                console.log('[RuneForgeStore] deleteFlowNode', nodeId);
            set(function (state) { return ({
                flow_nodes: state.flow_nodes.filter(function (node) { return node.id !== nodeId; }),
                selected_node_id: state.selected_node_id === nodeId ? null : state.selected_node_id
            }); });
        },
        updateFlowNodePosition: function (nodeId, position) {
            if (debug)
                console.log('[RuneForgeStore] updateFlowNodePosition', nodeId, position);
            set(function (state) { return ({
                flow_nodes: state.flow_nodes.map(function (node) {
                    return node.id === nodeId ? __assign(__assign({}, node), { position: position }) : node;
                })
            }); });
        },
        updateRuneParameters: function (nodeId, parameters) {
            if (debug)
                console.log('[RuneForgeStore] updateRuneParameters', nodeId, parameters);
            set(function (state) { return ({
                flow_nodes: state.flow_nodes.map(function (node) {
                    return node.id === nodeId ? __assign(__assign({}, node), { data: __assign(__assign({}, node.data), { parameters: parameters }) }) : node;
                })
            }); });
        },
        addFlowEdge: function (edgeParams) {
            if (debug)
                console.log('[RuneForgeStore] addFlowEdge', edgeParams);
            set(function (state) { return ({
                flow_edges: __spreadArrays(state.flow_edges, [edgeParams])
            }); });
        },
        deleteFlowEdge: function (edgeId) {
            if (debug)
                console.log('[RuneForgeStore] deleteFlowEdge', edgeId);
            set(function (state) { return ({
                flow_edges: state.flow_edges.filter(function (edge) { return edge.id !== edgeId; })
            }); });
        },
        setSelectedNodeId: function (nodeId) {
            if (debug)
                console.log('[RuneForgeStore] setSelectedNodeId', nodeId);
            set({ selected_node_id: nodeId });
        },
        setAvailableRunesList: function (runes) {
            if (debug)
                console.log('[RuneForgeStore] setAvailableRunesList', runes);
            set({ available_runes: runes });
        },
        // Async actions that use apiClient if provided
        initiateLoadSpell: function (spellId) { return __awaiter(void 0, void 0, void 0, function () {
            var spellData, _a, flowNodes, flowEdges, error_1, errorMessage;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (debug)
                            console.log('[RuneForgeStore] initiateLoadSpell', spellId);
                        set({ is_loading_spell: true, canvas_error: null });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 6, 7, 8]);
                        if (!(apiClient && apiClient.fetchSpellFromBackend)) return [3 /*break*/, 3];
                        return [4 /*yield*/, apiClient.fetchSpellFromBackend(spellId)];
                    case 2:
                        spellData = _b.sent();
                        if (spellData && spellData.workflow_json) {
                            _a = N8NJsonTransformerUtil_1.transformFromN8nJson(spellData.workflow_json), flowNodes = _a.flowNodes, flowEdges = _a.flowEdges;
                            get().setSpellData({
                                id: spellData.id || null,
                                name: spellData.name || 'Untitled Spell',
                                nodes: flowNodes,
                                edges: flowEdges
                            });
                            get().setSpellMetadata({
                                id: spellData.id,
                                name: spellData.name,
                                description: spellData.description,
                                isPublic: spellData.isPublic,
                                isTemplate: spellData.isTemplate
                            });
                        }
                        else {
                            throw new Error('Invalid spell data received');
                        }
                        return [3 /*break*/, 5];
                    case 3:
                        console.warn('No API client provided for loading spells');
                        // Simulate API delay for testing
                        return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve, 500); })];
                    case 4:
                        // Simulate API delay for testing
                        _b.sent();
                        _b.label = 5;
                    case 5: return [3 /*break*/, 8];
                    case 6:
                        error_1 = _b.sent();
                        errorMessage = error_1 instanceof Error ? error_1.message : 'Unknown error loading spell';
                        console.error('[RuneForgeStore] Error loading spell:', errorMessage);
                        set({ canvas_error: errorMessage });
                        return [3 /*break*/, 8];
                    case 7:
                        set({ is_loading_spell: false });
                        return [7 /*endfinally*/];
                    case 8: return [2 /*return*/];
                }
            });
        }); },
        initiateSaveCurrentSpell: function () { return __awaiter(void 0, void 0, void 0, function () {
            var _a, current_spell_id, current_spell_name, flow_nodes, flow_edges, spellMetadata, workflowJson, spellData, savedSpell, error_2, errorMessage;
            return __generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (debug)
                            console.log('[RuneForgeStore] initiateSaveCurrentSpell');
                        set({ is_saving_spell: true, canvas_error: null });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 6, 7, 8]);
                        _a = get(), current_spell_id = _a.current_spell_id, current_spell_name = _a.current_spell_name, flow_nodes = _a.flow_nodes, flow_edges = _a.flow_edges, spellMetadata = _a.spellMetadata;
                        workflowJson = N8NJsonTransformerUtil_1.transformToN8nJson(flow_nodes, flow_edges, current_spell_name, true // isActive
                        );
                        if (!(apiClient && apiClient.saveSpellToBackend)) return [3 /*break*/, 3];
                        spellData = __assign(__assign({}, spellMetadata), { id: current_spell_id, name: current_spell_name, workflow_json: workflowJson });
                        return [4 /*yield*/, apiClient.saveSpellToBackend(spellData)];
                    case 2:
                        savedSpell = _b.sent();
                        if (savedSpell && savedSpell.id) {
                            // Update with the returned ID if it's a new spell
                            if (!current_spell_id) {
                                set({ current_spell_id: savedSpell.id });
                            }
                            get().setSpellMetadata({
                                id: savedSpell.id,
                                name: savedSpell.name,
                                description: savedSpell.description,
                                isPublic: savedSpell.isPublic,
                                isTemplate: savedSpell.isTemplate
                            });
                        }
                        return [3 /*break*/, 5];
                    case 3:
                        console.warn('No API client provided for saving spells');
                        // Simulate API delay for testing
                        return [4 /*yield*/, new Promise(function (resolve) { return setTimeout(resolve, 500); })];
                    case 4:
                        // Simulate API delay for testing
                        _b.sent();
                        _b.label = 5;
                    case 5: return [3 /*break*/, 8];
                    case 6:
                        error_2 = _b.sent();
                        errorMessage = error_2 instanceof Error ? error_2.message : 'Unknown error saving spell';
                        console.error('[RuneForgeStore] Error saving spell:', errorMessage);
                        set({ canvas_error: errorMessage });
                        return [3 /*break*/, 8];
                    case 7:
                        set({ is_saving_spell: false });
                        return [7 /*endfinally*/];
                    case 8: return [2 /*return*/];
                }
            });
        }); },
        // React Flow handlers
        onNodesChange: function (changes) {
            set(function (state) { return ({
                flow_nodes: reactflow_1.applyNodeChanges(changes, state.flow_nodes)
            }); });
        },
        onEdgesChange: function (changes) {
            set(function (state) { return ({
                flow_edges: reactflow_1.applyEdgeChanges(changes, state.flow_edges)
            }); });
        },
        onConnect: function (connection) {
            set(function (state) { return ({
                flow_edges: __spreadArrays(state.flow_edges, [connection])
            }); });
        }
    }); });
};
// Export an initial spell metadata object for convenience
exports.initialSpellMetadata = {
    id: null,
    name: 'New Spell',
    description: '',
    isPublic: false,
    isTemplate: false
};
