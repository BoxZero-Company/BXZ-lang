// src/cli/loader/index.js

import { loadFromA } from './loaderA.js';
import { processWithB } from './loaderB.js';

console.log("Initializing loader module...");

// مثال استفاده از loaderA
const resultA = loadFromA("Initial configuration");
console.log("Result from Loader A:", resultA);

// مثال استفاده از loaderB
const initialValue = 10;
const resultB = processWithB(initialValue);
console.log(`Result from Loader B for ${initialValue}:`, resultB);

// می‌توانید منطق اصلی loader خود را در اینجا اضافه کنید
// که از توابع loaderA و loaderB استفاده می‌کند.

export default {
  loadFromA,
  processWithB,
  // سایر توابع یا متغیرهای export شده از این ماژول
};
