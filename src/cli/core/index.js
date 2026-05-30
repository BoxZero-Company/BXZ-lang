// src/cli/core/index.js

// این خط اکنون باید کار کند چون coreFunc1.js وجود دارد
import { logMessage } from './coreFunc1.js';

console.log("Running build:core...");

// استفاده از تابعی که از coreFunc1.js وارد شده است
logMessage("Core initialization complete.");

// اگر توابع یا کلاس‌های دیگری دارید، آن‌ها را نیز اینجا وارد و صادر کنید
// import AnotherCoreThing from './anotherCoreThing.js';
// export { AnotherCoreThing };
