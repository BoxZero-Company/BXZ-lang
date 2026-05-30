// src/cli/loader/loaderB.js

/**
 * یک تابع نمونه برای loaderB.
 * این تابع یک عدد را دریافت کرده و آن را دو برابر می‌کند.
 * @param {number} value - عددی که باید پردازش شود.
 * @returns {number} - مقدار دو برابر شده.
 */
export function processWithB(value) {
  if (typeof value !== 'number') {
    console.error("Loader B expects a number.");
    return NaN;
  }
  console.log(`Loader B processing: ${value}`);
  // در اینجا می‌توانید منطق بارگذاری یا پردازش خاصی را اضافه کنید.
  return value * 2;
}

// می‌توانید موارد بیشتری را export کنید:
// export default { ... }; // Export پیش‌فرض
