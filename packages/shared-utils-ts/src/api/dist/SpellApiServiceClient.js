"use strict";
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
exports.__esModule = true;
exports.createSpellApiServiceClient = void 0;
/**
 * SpellApiServiceClient factory
 * Creates a client for interacting with the grimOS backend Spellbook API.
 * @param baseUrl Base URL for the API
 * @returns SpellApiService client instance
 */
exports.createSpellApiServiceClient = function (baseUrl) {
    if (baseUrl === void 0) { baseUrl = 'http://localhost:8000/api/v1'; }
    return {
        /**
         * Fetches a specific spell from the backend.
         * @param spell_id The ID of the spell to fetch.
         * @returns A Promise resolving to the SpellData.
         * @throws Error if the fetch operation fails.
         */
        fetchSpellFromBackend: function (spell_id) {
            return __awaiter(this, void 0, Promise, function () {
                var response, errorData;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, fetch(baseUrl + "/spells/" + spell_id)];
                        case 1:
                            response = _a.sent();
                            if (!!response.ok) return [3 /*break*/, 3];
                            return [4 /*yield*/, response.json()["catch"](function () { return ({ detail: 'Network response was not ok and failed to parse error JSON.' }); })];
                        case 2:
                            errorData = _a.sent();
                            throw new Error(errorData.detail || "Failed to fetch spell " + spell_id + ". Status: " + response.status);
                        case 3: return [2 /*return*/, response.json()];
                    }
                });
            });
        },
        /**
         * Saves a spell (either new or existing) to the backend.
         * The backend should handle creation (if id is null or not found) or update.
         * @param spellData The complete spell data to save.
         * @returns A Promise resolving to the saved SpellData (which might include a new ID or updated timestamps).
         * @throws Error if the save operation fails.
         */
        saveSpellToBackend: function (spellData) {
            return __awaiter(this, void 0, Promise, function () {
                var url, method, response, errorData;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0:
                            url = spellData.id ? baseUrl + "/spells/" + spellData.id : baseUrl + "/spells/";
                            method = spellData.id ? 'PUT' : 'POST';
                            return [4 /*yield*/, fetch(url, {
                                    method: method,
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify(spellData)
                                })];
                        case 1:
                            response = _a.sent();
                            if (!!response.ok) return [3 /*break*/, 3];
                            return [4 /*yield*/, response.json()["catch"](function () { return ({ detail: 'Network response was not ok and failed to parse error JSON.' }); })];
                        case 2:
                            errorData = _a.sent();
                            throw new Error(errorData.detail || "Failed to save spell. Status: " + response.status);
                        case 3: return [2 /*return*/, response.json()];
                    }
                });
            });
        },
        /**
         * Fetches all spells, potentially with pagination or filtering in the future.
         * @returns A Promise resolving to an array of SpellData.
         * @throws Error if the fetch operation fails.
         */
        fetchAllSpells: function () {
            return __awaiter(this, void 0, Promise, function () {
                var response, errorData;
                return __generator(this, function (_a) {
                    switch (_a.label) {
                        case 0: return [4 /*yield*/, fetch(baseUrl + "/spells/")];
                        case 1:
                            response = _a.sent();
                            if (!!response.ok) return [3 /*break*/, 3];
                            return [4 /*yield*/, response.json()["catch"](function () { return ({ detail: 'Network response was not ok and failed to parse error JSON.' }); })];
                        case 2:
                            errorData = _a.sent();
                            throw new Error(errorData.detail || "Failed to fetch all spells. Status: " + response.status);
                        case 3: return [2 /*return*/, response.json()];
                    }
                });
            });
        }
    };
};
