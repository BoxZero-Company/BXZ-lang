// src/cli/loader/loaderA.js
function loadFromA(message) {
  console.log(`Loader A received: ${message}`);
  return `Data loaded from A with: ${message}`;
}

// src/cli/loader/loaderB.js
function processWithB(value) {
  if (typeof value !== "number") {
    console.error("Loader B expects a number.");
    return NaN;
  }
  console.log(`Loader B processing: ${value}`);
  return value * 2;
}

// src/cli/loader/index.js
console.log("Initializing loader module...");
var resultA = loadFromA("Initial configuration");
console.log("Result from Loader A:", resultA);
var initialValue = 10;
var resultB = processWithB(initialValue);
console.log(`Result from Loader B for ${initialValue}:`, resultB);
var loader_default = {
  loadFromA,
  processWithB
  // سایر توابع یا متغیرهای export شده از این ماژول
};
export {
  loader_default as default
};
