// src/cli/loader/loaderA.js

/**
 * یک تابع نمونه برای loaderA.
 * این تابع یک پیام را در کنسول چاپ می‌کند.
 * @param {string} message - پیامی که باید چاپ شود.
 */
export function loadFromA(message) {
  console.log(`Loader A received: ${message}`);
  // در اینجا می‌توانید منطق بارگذاری یا پردازش خاصی را اضافه کنید.
  return `Data loaded from A with: ${message}`;
}

// می‌توانید موارد بیشتری را export کنید:
// export const someConstant = 123;
// export class SomeClassFromA { ... }
