import { __assign } from "tslib";
import { flattenRelevantPaths, parseQuickTrace, } from 'app/utils/performance/quickTrace/utils';
function hexCharFor(x) {
    x = x % 16;
    if (x < 10) {
        return String(x);
    }
    return String.fromCharCode('a'.charCodeAt(0) + x - 10);
}
function generateId(prefix, _a) {
    var generation = _a.generation, offset = _a.offset;
    var s = "" + hexCharFor(generation) + hexCharFor(offset);
    return prefix + ":" + Array(7).join(s);
}
function generateEventId(_a) {
    var generation = _a.generation, offset = _a.offset;
    return generateId('e', { generation: generation, offset: offset });
}
function generateSpanId(_a) {
    var generation = _a.generation, offset = _a.offset;
    return generateId('s', { generation: generation, offset: offset });
}
function generateTransactionName(_a) {
    var generation = _a.generation, offset = _a.offset;
    return "transaction-" + generation + "-" + offset;
}
function generateProjectSlug(_a) {
    var generation = _a.generation, offset = _a.offset;
    var c = hexCharFor(generation);
    return "project-" + c.toUpperCase() + "-" + offset;
}
function computePosition(index) {
    index += 1;
    var generation = Math.floor(Math.log2(index));
    var offset = index - Math.pow(2, generation);
    return { generation: generation, offset: offset };
}
function generateTransactionLite(_a) {
    var generation = _a.generation, offset = _a.offset;
    var position = { generation: generation, offset: offset };
    var parentPosition = {
        generation: generation - 1,
        offset: Math.floor(offset / 2),
    };
    return {
        event_id: generateEventId(position),
        generation: generation,
        span_id: generateSpanId(position),
        transaction: generateTransactionName(position),
        'transaction.duration': 0,
        project_id: generation,
        project_slug: generateProjectSlug(position),
        parent_event_id: generation <= 0 ? null : generateEventId(parentPosition),
        parent_span_id: generation <= 0 ? null : generateSpanId(parentPosition),
        errors: [],
    };
}
function generateTransaction(opts) {
    var index = opts.index, _a = opts.depth, depth = _a === void 0 ? -1 : _a;
    var _b = computePosition(index), generation = _b.generation, offset = _b.offset;
    return __assign(__assign({}, generateTransactionLite({ generation: generation, offset: offset })), { errors: [], children: Array(depth <= 0 || generation >= depth - 1 ? 0 : 2)
            .fill(null)
            .map(function (_, i) {
            return generateTransaction({
                index: 2 * index + i + 1,
                depth: depth,
            });
        }), 
        /**
         * These timestamps aren't used in tests here, just adding them to pass
         * the type checking.
         */
        'transaction.duration': 0 });
}
function generateTrace(depth) {
    if (depth === void 0) { depth = 1; }
    if (depth < 1) {
        throw new Error('Minimum depth is 1!');
    }
    return generateTransaction({
        depth: depth,
        index: 0,
    });
}
function generateEventSelector(position, eventType) {
    return { id: generateEventId(position), type: eventType };
}
describe('Quick Trace Utils', function () {
    describe('flattenRelevantPaths', function () {
        it('flattens trace without the expected event', function () {
            var trace = generateTrace(1);
            var current = { id: 'you cant find me' };
            expect(function () { return flattenRelevantPaths(current, trace); }).toThrow('No relevant path exists!');
        });
        it('flattens a single transaction trace', function () {
            var trace = generateTrace(1);
            var current = generateEventSelector({ generation: 0, offset: 0 }, 'transaction');
            var relevantPath = flattenRelevantPaths(current, trace);
            expect(relevantPath).toMatchObject([
                generateTransactionLite({ generation: 0, offset: 0 }),
            ]);
        });
        it('flattens trace from the leaf', function () {
            var trace = generateTrace(3);
            var current = generateEventSelector({ generation: 2, offset: 3 }, 'transaction');
            var relevantPath = flattenRelevantPaths(current, trace);
            expect(relevantPath).toMatchObject([
                generateTransactionLite({ generation: 0, offset: 0 }),
                generateTransactionLite({ generation: 1, offset: 1 }),
                generateTransactionLite({ generation: 2, offset: 3 }),
            ]);
        });
        it('flattens trace from the middle', function () {
            var trace = generateTrace(3);
            var current = generateEventSelector({ generation: 1, offset: 1 }, 'transaction');
            var relevantPath = flattenRelevantPaths(current, trace);
            expect(relevantPath).toMatchObject([
                generateTransactionLite({ generation: 0, offset: 0 }),
                generateTransactionLite({ generation: 1, offset: 1 }),
                generateTransactionLite({ generation: 2, offset: 2 }),
                generateTransactionLite({ generation: 2, offset: 3 }),
            ]);
        });
        it('flattens trace from the root', function () {
            var trace = generateTrace(3);
            var current = generateEventSelector({ generation: 0, offset: 0 }, 'transaction');
            var relevantPath = flattenRelevantPaths(current, trace);
            expect(relevantPath).toMatchObject([
                generateTransactionLite({ generation: 0, offset: 0 }),
                generateTransactionLite({ generation: 1, offset: 0 }),
                generateTransactionLite({ generation: 1, offset: 1 }),
                generateTransactionLite({ generation: 2, offset: 0 }),
                generateTransactionLite({ generation: 2, offset: 1 }),
                generateTransactionLite({ generation: 2, offset: 2 }),
                generateTransactionLite({ generation: 2, offset: 3 }),
            ]);
        });
    });
    describe('parseQuickTrace', function () {
        it('parses empty trace', function () {
            var current = generateEventSelector({ generation: 0, offset: 0 }, 'transaction');
            expect(function () { return parseQuickTrace({ type: 'empty', trace: [] }, current); }).toThrow('Current event not in quick trace');
        });
        describe('partial trace', function () {
            it('parses correctly without the expected event', function () {
                var relevantPath = [generateTransactionLite({ generation: 0, offset: 0 })];
                var current = generateEventSelector({ generation: 1, offset: 0 }, 'transaction');
                expect(function () {
                    return parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                }).toThrow('Current event not in quick trace');
            });
            it('parses only the current event', function () {
                var relevantPath = [generateTransactionLite({ generation: 0, offset: 0 })];
                var current = generateEventSelector({ generation: 0, offset: 0 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: null,
                    ancestors: null,
                    parent: null,
                    current: generateTransactionLite({ generation: 0, offset: 0 }),
                    children: [],
                    descendants: null,
                });
            });
            it('parses current with only parent', function () {
                var relevantPath = [
                    generateTransactionLite({ generation: 0, offset: 0 }),
                    generateTransactionLite({ generation: 1, offset: 0 }),
                ];
                var current = generateEventSelector({ generation: 1, offset: 0 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: null,
                    ancestors: null,
                    parent: generateTransactionLite({ generation: 0, offset: 0 }),
                    current: generateTransactionLite({ generation: 1, offset: 0 }),
                    children: [],
                    descendants: null,
                });
            });
            it('parses current with only root', function () {
                var relevantPath = [
                    generateTransactionLite({ generation: 0, offset: 0 }),
                    generateTransactionLite({ generation: 2, offset: 0 }),
                ];
                var current = generateEventSelector({ generation: 2, offset: 0 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: null,
                    parent: null,
                    current: generateTransactionLite({ generation: 2, offset: 0 }),
                    children: [],
                    descendants: null,
                });
            });
            it('parses current with only children', function () {
                var relevantPath = [
                    generateTransactionLite({ generation: 0, offset: 0 }),
                    generateTransactionLite({ generation: 1, offset: 0 }),
                    generateTransactionLite({ generation: 1, offset: 1 }),
                ];
                var current = generateEventSelector({ generation: 0, offset: 0 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: null,
                    ancestors: null,
                    parent: null,
                    current: generateTransactionLite({ generation: 0, offset: 0 }),
                    children: [
                        generateTransactionLite({ generation: 1, offset: 0 }),
                        generateTransactionLite({ generation: 1, offset: 1 }),
                    ],
                    descendants: null,
                });
            });
            it('parses current with parent and children', function () {
                var relevantPath = [
                    generateTransactionLite({ generation: 0, offset: 0 }),
                    generateTransactionLite({ generation: 1, offset: 1 }),
                    generateTransactionLite({ generation: 2, offset: 2 }),
                ];
                var current = generateEventSelector({ generation: 1, offset: 1 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: null,
                    ancestors: null,
                    parent: generateTransactionLite({ generation: 0, offset: 0 }),
                    current: generateTransactionLite({ generation: 1, offset: 1 }),
                    children: [generateTransactionLite({ generation: 2, offset: 2 })],
                    descendants: null,
                });
            });
            it('parses current with root and children', function () {
                var relevantPath = [
                    generateTransactionLite({ generation: 0, offset: 0 }),
                    generateTransactionLite({ generation: 2, offset: 2 }),
                    generateTransactionLite({ generation: 3, offset: 4 }),
                    generateTransactionLite({ generation: 3, offset: 5 }),
                ];
                var current = generateEventSelector({ generation: 2, offset: 2 }, 'transaction');
                var parsedQuickTrace = parseQuickTrace({ type: 'partial', trace: relevantPath }, current);
                expect(parsedQuickTrace).toEqual({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: null,
                    parent: null,
                    current: generateTransactionLite({ generation: 2, offset: 2 }),
                    children: [
                        generateTransactionLite({ generation: 3, offset: 4 }),
                        generateTransactionLite({ generation: 3, offset: 5 }),
                    ],
                    descendants: null,
                });
            });
        });
        describe('full trace', function () {
            it('parses the full trace', function () {
                var trace = generateTrace(6);
                var current = generateEventSelector({ generation: 3, offset: 0 }, 'transaction');
                var relevantPath = flattenRelevantPaths(current, trace);
                var parsedQuickTrace = parseQuickTrace({ type: 'full', trace: relevantPath }, current);
                expect(parsedQuickTrace).toMatchObject({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: [generateTransactionLite({ generation: 1, offset: 0 })],
                    parent: generateTransactionLite({ generation: 2, offset: 0 }),
                    current: generateTransactionLite({ generation: 3, offset: 0 }),
                    children: [
                        generateTransactionLite({ generation: 4, offset: 0 }),
                        generateTransactionLite({ generation: 4, offset: 1 }),
                    ],
                    descendants: [
                        generateTransactionLite({ generation: 5, offset: 0 }),
                        generateTransactionLite({ generation: 5, offset: 1 }),
                        generateTransactionLite({ generation: 5, offset: 2 }),
                        generateTransactionLite({ generation: 5, offset: 3 }),
                    ],
                });
            });
            it('parses full trace without ancestors', function () {
                var trace = generateTrace(5);
                var current = generateEventSelector({ generation: 2, offset: 0 }, 'transaction');
                var relevantPath = flattenRelevantPaths(current, trace);
                var parsedQuickTrace = parseQuickTrace({ type: 'full', trace: relevantPath }, current);
                expect(parsedQuickTrace).toMatchObject({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: [],
                    parent: generateTransactionLite({ generation: 1, offset: 0 }),
                    current: generateTransactionLite({ generation: 2, offset: 0 }),
                    children: [
                        generateTransactionLite({ generation: 3, offset: 0 }),
                        generateTransactionLite({ generation: 3, offset: 1 }),
                    ],
                    descendants: [
                        generateTransactionLite({ generation: 4, offset: 0 }),
                        generateTransactionLite({ generation: 4, offset: 1 }),
                        generateTransactionLite({ generation: 4, offset: 2 }),
                        generateTransactionLite({ generation: 4, offset: 3 }),
                    ],
                });
            });
            it('parses full trace without descendants', function () {
                var trace = generateTrace(5);
                var current = generateEventSelector({ generation: 3, offset: 0 }, 'transaction');
                var relevantPath = flattenRelevantPaths(current, trace);
                var parsedQuickTrace = parseQuickTrace({ type: 'full', trace: relevantPath }, current);
                expect(parsedQuickTrace).toMatchObject({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: [generateTransactionLite({ generation: 1, offset: 0 })],
                    parent: generateTransactionLite({ generation: 2, offset: 0 }),
                    current: generateTransactionLite({ generation: 3, offset: 0 }),
                    children: [
                        generateTransactionLite({ generation: 4, offset: 0 }),
                        generateTransactionLite({ generation: 4, offset: 1 }),
                    ],
                    descendants: [],
                });
            });
            it('parses full trace without children descendants', function () {
                var trace = generateTrace(4);
                var current = generateEventSelector({ generation: 3, offset: 0 }, 'transaction');
                var relevantPath = flattenRelevantPaths(current, trace);
                var parsedQuickTrace = parseQuickTrace({ type: 'full', trace: relevantPath }, current);
                expect(parsedQuickTrace).toMatchObject({
                    root: generateTransactionLite({ generation: 0, offset: 0 }),
                    ancestors: [generateTransactionLite({ generation: 1, offset: 0 })],
                    parent: generateTransactionLite({ generation: 2, offset: 0 }),
                    current: generateTransactionLite({ generation: 3, offset: 0 }),
                    children: [],
                    descendants: [],
                });
            });
        });
    });
});
//# sourceMappingURL=utils.spec.jsx.map