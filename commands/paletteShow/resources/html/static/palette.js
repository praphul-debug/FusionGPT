// Global variables
let isProcessing = false;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupKeyboardShortcuts();
    updateResponseArea('Ready to process your commands...', 'info');
});

function setupKeyboardShortcuts() {
    const input = document.getElementById('aiCommandInput');
    
    input.addEventListener('keydown', function(event) {
        // Ctrl+Enter to submit
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();
            processAICommand();
        }
    });
}

function insertMockCommand(command) {
    const input = document.getElementById('aiCommandInput');
    input.value = command;
    input.focus();
    
    // Add visual feedback
    const cards = document.querySelectorAll('.mock-model-card');
    cards.forEach(card => {
        if (card.textContent.includes(command)) {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = '';
            }, 150);
        }
    });
}

function processAICommand() {
    if (isProcessing) return;
    
    const input = document.getElementById('aiCommandInput');
    const command = input.value.trim();
    
    if (!command) {
        updateResponseArea('Please enter a command first.', 'error');
        return;
    }
    
    // Set processing state
    isProcessing = true;
    const button = document.getElementById('processCommand');
    const originalText = button.textContent;
    button.textContent = 'Processing...';
    button.disabled = true;
    button.classList.add('loading');
    
    updateResponseArea('🤖 Processing your command with AI...', 'processing');
    
    // Send command to Fusion 360 Python backend
    const messageData = {
        command: command,
        timestamp: new Date().toISOString()
    };
    
    // Send the data to Fusion as a JSON string
    adsk.fusionSendData("processAICommand", JSON.stringify(messageData))
        .then((result) => {
            try {
                const response = JSON.parse(result);
                handleAIResponse(response);
            } catch (e) {
                updateResponseArea(`Response: ${result}`, 'success');
            }
        })
        .catch((error) => {
            updateResponseArea(`Error: ${error}`, 'error');
        })
        .finally(() => {
            // Reset processing state
            isProcessing = false;
            button.textContent = originalText;
            button.disabled = false;
            button.classList.remove('loading');
        });
}

function handleAIResponse(response) {
    if (response.success) {
        updateResponseArea(`✅ ${response.message}`, 'success');
        
        // Clear input on successful execution
        setTimeout(() => {
            document.getElementById('aiCommandInput').value = '';
        }, 1000);
    } else {
        updateResponseArea(`❌ ${response.error || response.message}`, 'error');
    }
}

function updateResponseArea(message, type = 'info') {
    const responseArea = document.getElementById('aiResponse');
    const timestamp = new Date().toLocaleTimeString();
    
    // Create status message element
    const statusClass = type === 'processing' ? 'status-processing' : 
                       type === 'success' ? 'status-success' : 
                       type === 'error' ? 'status-error' : '';
    
    const statusMessage = statusClass ? 
        `<div class="status-message ${statusClass}">${message}</div>` : 
        message;
    
    responseArea.innerHTML = `
        <div style="margin-bottom: 12px;">
            <strong>[${timestamp}]</strong>
        </div>
        ${statusMessage}
    `;
    
    // Auto-scroll to bottom
    responseArea.scrollTop = responseArea.scrollHeight;
}

function getDateString() {
    const today = new Date();
    const date = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
    return `Date: ${date}, Time: ${time}`;
}

// Legacy function for compatibility
function sendInfoToFusion() {
    const args = {
        arg1: document.getElementById("sampleData")?.value || "test",
        arg2: getDateString()
    };

    adsk.fusionSendData("messageFromPalette", JSON.stringify(args)).then((result) =>
        updateResponseArea(`Legacy response: ${result}`, 'info')
    );
}

// Legacy function for compatibility
function updateMessage(messageString) {
    try {
        const messageData = JSON.parse(messageString);
        updateResponseArea(`Legacy message: ${JSON.stringify(messageData, null, 2)}`, 'info');
    } catch (e) {
        updateResponseArea(`Legacy message: ${messageString}`, 'info');
    }
}

// Main message handler for Fusion 360 communication
window.fusionJavaScriptHandler = {
    handle: function (action, data) {
        try {
            if (action === "updateMessage") {
                updateMessage(data);
            } else if (action === "aiResponse") {
                const response = JSON.parse(data);
                handleAIResponse(response);
            } else if (action === "debugger") {
                debugger;
            } else {
                console.log(`Unhandled action: ${action}`);
                return `Unexpected command type: ${action}`;
            }
        } catch (e) {
            console.log(e);
            console.log(`Exception caught with command: ${action}, data: ${data}`);
            updateResponseArea(`Error handling ${action}: ${e.message}`, 'error');
        }
        return "OK";
    },
};