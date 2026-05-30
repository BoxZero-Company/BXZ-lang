const codeEditor = document.getElementById('codeEditor');
const outputArea = document.getElementById('output');
const runBtn = document.getElementById('runBtn');
const clearBtn = document.getElementById('clearBtn');

// Default code
const defaultCode = `print("Hello World!")

let name = "BXZ User"
let version = 1.0
print("Welcome " + name + " to BXZ v" + version)

// Variables and calculations
let x = 10
let y = 20
let sum = x + y
print("Sum of " + x + " and " + y + " is: " + sum)

// Function example
func square(n) {
    return n * n
}

print("Square of 5 is: " + square(5))

// Python integration (if Python is installed)
python("print('Hello from Python!')")

// JavaScript integration (if Node.js is installed)
js("console.log('Hello from JavaScript!')")`;

codeEditor.value = defaultCode;

// Run code
runBtn.addEventListener('click', async () => {
    const code = codeEditor.value;
    if (!code.trim()) {
        addOutput('No code to run', 'error');
        return;
    }
    
    runBtn.disabled = true;
    runBtn.textContent = '⏳ Running...';
    addOutput('🚀 Running BXZ code...', 'info');
    
    try {
        const response = await fetch('/api/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (data.output) {
                addOutput(data.output, 'output');
            }
            if (data.result !== undefined && data.result !== null) {
                addOutput(`Result: ${data.result}`, 'success');
            }
            addOutput('✅ Execution completed', 'success');
        } else {
            addOutput(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        addOutput(`❌ Connection error: ${error.message}`, 'error');
    } finally {
        runBtn.disabled = false;
        runBtn.textContent = '▶ Run Code';
    }
});

// Clear output
clearBtn.addEventListener('click', () => {
    outputArea.innerHTML = '';
    addOutput('Output cleared', 'info');
});

// Example cards
document.querySelectorAll('.example-card').forEach(card => {
    card.addEventListener('click', () => {
        const code = card.getAttribute('data-code');
        if (code) {
            codeEditor.value = code.replace(/\\n/g, '\\n');
            addOutput(`📋 Loaded example: ${card.textContent}`, 'info');
        }
    });
});

function addOutput(text, type = 'output') {
    const p = document.createElement('p');
    p.textContent = text;
    
    if (type === 'error') {
        p.style.borderLeftColor = '#fc8181';
        p.style.color = '#fc8181';
    } else if (type === 'success') {
        p.style.borderLeftColor = '#68d391';
        p.style.color = '#68d391';
    } else if (type === 'info') {
        p.style.borderLeftColor = '#63b3ed';
        p.style.color = '#63b3ed';
    }
    
    outputArea.appendChild(p);
    p.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Keyboard shortcuts
codeEditor.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runBtn.click();
    }
});

// Welcome message
addOutput('🎉 Welcome to BXZ Web IDE!', 'success');
addOutput('Write BXZ code and click "Run Code" to execute', 'info');
addOutput('Try the examples below or write your own code!', 'info');
''