import { formatBytesBase2 } from 'app/utils';
function formatMemory(memory_size, free_memory, usable_memory) {
    if (!Number.isInteger(memory_size) ||
        memory_size <= 0 ||
        !Number.isInteger(free_memory) ||
        free_memory <= 0) {
        return null;
    }
    var memory = "Total: " + formatBytesBase2(memory_size) + " / Free: " + formatBytesBase2(free_memory);
    if (Number.isInteger(usable_memory) && usable_memory > 0) {
        memory = memory + " / Usable: " + formatBytesBase2(usable_memory);
    }
    return memory;
}
export default formatMemory;
//# sourceMappingURL=formatMemory.jsx.map