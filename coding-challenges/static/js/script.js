/**
 * Code Challenges Platform - Client-side Enhancements
 */

document.addEventListener('DOMContentLoaded', () => {
    initFormValidation();
    initCodeEditor();
    initAlertDismiss();
});

/**
 * Form validation for registration
 */
function initFormValidation() {
    const registerForm = document.getElementById('register-form');
    if (!registerForm) return;

    registerForm.addEventListener('submit', (e) => {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;

        if (password !== confirmPassword) {
            e.preventDefault();
            showAlert('Passwords do not match.', 'error');
            return;
        }

        if (password.length < 6) {
            e.preventDefault();
            showAlert('Password must be at least 6 characters.', 'error');
            return;
        }
    });
}

/**
 * Code editor enhancements (tab support, auto-indent)
 */
function initCodeEditor() {
    const editor = document.getElementById('code-editor');
    if (!editor) return;

    // Tab key support
    editor.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = editor.selectionStart;
            const end = editor.selectionEnd;
            editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
            editor.selectionStart = editor.selectionEnd = start + 4;
        }
    });

    // Auto-resize
    editor.addEventListener('input', () => {
        editor.style.height = 'auto';
        editor.style.height = Math.max(300, editor.scrollHeight) + 'px';
    });

    // Reset button
    const resetBtn = document.getElementById('reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            if (confirm('Reset your code to the starter template?')) {
                editor.value = editor.defaultValue;
            }
        });
    }
}

/**
 * Auto-dismiss alerts after 5 seconds
 */
function initAlertDismiss() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

/**
 * Show a temporary alert message
 */
function showAlert(message, type = 'info') {
    const container = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    container.insertBefore(alert, container.firstChild);

    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}
