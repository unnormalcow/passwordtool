// Tab switching logic
function openTab(evt, tabName) {
    var i, tabcontent, tabbuttons;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
        tabcontent[i].classList.remove("active");
    }
    tabbuttons = document.getElementsByClassName("tab-button");
    for (i = 0; i < tabbuttons.length; i++) {
        tabbuttons[i].classList.remove("active");
    }
    document.getElementById(tabName).style.display = "block";
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
    updateStatusBar("准备就绪"); // Reset status bar on tab switch
}

// Initialize the first tab
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.tab-button').click();
});

// --- Base64 Functions ---
function encodeBase64() {
    const input = document.getElementById('base64Input').value;
    const outputField = document.getElementById('base64Output');
    if (!input) {
        alert("请输入需要编码的文本");
        updateStatusBar("编码失败: 输入为空", true);
        return;
    }
    try {
        const encoded = btoa(unescape(encodeURIComponent(input))); // Handle UTF-8 characters
        outputField.value = encoded;
        updateStatusBar("编码成功");
    } catch (e) {
        outputField.value = "编码错误: " + e.message;
        updateStatusBar("编码错误: " + e.message, true);
        console.error("Base64 Encoding Error:", e);
    }
}

function decodeBase64() {
    const input = document.getElementById('base64Input').value;
    const outputField = document.getElementById('base64Output');
    if (!input) {
        alert("请输入需要解码的文本");
        updateStatusBar("解码失败: 输入为空", true);
        return;
    }
    try {
        // Basic padding check, though btoa/atob are somewhat lenient
        let paddedInput = input;
        const missingPadding = input.length % 4;
        if (missingPadding) {
            paddedInput += '='.repeat(4 - missingPadding);
        }
        const decoded = decodeURIComponent(escape(atob(paddedInput))); // Handle UTF-8 characters
        outputField.value = decoded;
        updateStatusBar("解码成功");
    } catch (e) {
        outputField.value = "解码错误: " + e.message;
        updateStatusBar("解码错误: " + e.message, true);
        console.error("Base64 Decoding Error:", e);
        if (e.name === 'InvalidCharacterError') {
            alert("解码错误: 输入的字符串包含无效的Base64字符。请确保输入的是有效的Base64编码字符串。");
        }
    }
}

function clearBase64Fields() {
    document.getElementById('base64Input').value = '';
    document.getElementById('base64Output').value = '';
    updateStatusBar("Base64字段已清空");
}

// --- Password Generator Functions ---
function generatePasswordsBatch() {
    const useUppercase = document.getElementById('useUppercase').checked;
    const useLowercase = document.getElementById('useLowercase').checked;
    const useDigits = document.getElementById('useDigits').checked;
    const useSpecial = document.getElementById('useSpecial').checked;
    const length = parseInt(document.getElementById('passwordLength').value);
    const displayArea = document.getElementById('passwordsDisplayArea');
    displayArea.innerHTML = '';
    if (!useUppercase && !useLowercase && !useDigits && !useSpecial) {
        alert("请至少选择一种字符类型");
        updateStatusBar("密码生成失败: 未选择字符类型", true);
        return;
    }
    if (length <= 0 || length > 256) {
        alert("密码长度必须在1到256之间");
        updateStatusBar("密码生成失败: 长度无效", true);
        return;
    }
    let generatedPasswords = [];
    for (let i = 0; i < 10; i++) {
        const password = _generateSinglePassword(length, useUppercase, useLowercase, useDigits, useSpecial);
        if (password) {
            generatedPasswords.push(password);
            const { strengthText, strengthClass } = checkPasswordStrength(password);
            const passwordDiv = document.createElement('div');
            passwordDiv.className = 'password-entry';
            // 密码
            const passwordTextSpan = document.createElement('span');
            passwordTextSpan.className = 'password-text';
            passwordTextSpan.textContent = password;
            // 强度
            const strengthSpan = document.createElement('span');
            strengthSpan.className = `password-strength ${strengthClass}`;
            strengthSpan.textContent = strengthText.split(' (')[0];
            // 是否已用
            const usedSpan = document.createElement('span');
            usedSpan.className = 'password-used';
            usedSpan.textContent = '未使用';
            usedSpan.style.color = '';
            // 复制按钮
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-btn';
            copyButton.textContent = '复制';
            copyButton.onclick = function() {
                copyToClipboard(password);
                usedSpan.textContent = '已使用';
                usedSpan.style.color = 'red';
                passwordDiv.setAttribute('data-used', 'true');
            };
            passwordDiv.setAttribute('data-used', 'false');
            passwordDiv.appendChild(passwordTextSpan);
            passwordDiv.appendChild(strengthSpan);
            passwordDiv.appendChild(usedSpan);
            passwordDiv.appendChild(copyButton);
            displayArea.appendChild(passwordDiv);
        }
    }
    if (generatedPasswords.length > 0) {
        updateStatusBar("10个密码已生成");
    } else {
        updateStatusBar("未能生成密码，请检查选项", true);
    }
}

function _generateSinglePassword(length, useUpper, useLower, useDigits, useSpecial) {
    const upperChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowerChars = 'abcdefghijklmnopqrstuvwxyz';
    const digitChars = '0123456789';
    const specialChars = '!@#$%^&*()_+-=[]{}|;:,.<>?';

    let characterSet = '';
    let guaranteedChars = [];

    if (useUpper) {
        characterSet += upperChars;
        guaranteedChars.push(upperChars[Math.floor(Math.random() * upperChars.length)]);
    }
    if (useLower) {
        characterSet += lowerChars;
        guaranteedChars.push(lowerChars[Math.floor(Math.random() * lowerChars.length)]);
    }
    if (useDigits) {
        characterSet += digitChars;
        guaranteedChars.push(digitChars[Math.floor(Math.random() * digitChars.length)]);
    }
    if (useSpecial) {
        characterSet += specialChars;
        guaranteedChars.push(specialChars[Math.floor(Math.random() * specialChars.length)]);
    }

    if (characterSet === '') return null;

    // Remove duplicates from guaranteedChars if length is very small
    guaranteedChars = Array.from(new Set(guaranteedChars));

    let password = guaranteedChars.slice(0, length); // Start with guaranteed, truncate if needed

    for (let i = password.length; i < length; i++) {
        password.push(characterSet[Math.floor(Math.random() * characterSet.length)]);
    }

    // Shuffle the password array to ensure randomness
    for (let i = password.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [password[i], password[j]] = [password[j], password[i]];
    }

    return password.join('');
}

function checkPasswordStrength(password) {
    let score = 0;
    let feedback = [];
    const length = password.length;

    if (length >= 12) score += 2;
    else if (length >= 8) score += 1;
    else feedback.push("太短");

    const hasUpper = /[A-Z]/.test(password);
    const hasLower = /[a-z]/.test(password);
    const hasDigit = /[0-9]/.test(password);
    const hasSpecial = /[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password);

    if (hasUpper) score += 1; else feedback.push("无大写");
    if (hasLower) score += 1; else feedback.push("无小写");
    if (hasDigit) score += 1; else feedback.push("无数字");
    if (hasSpecial) score += 1; else feedback.push("无特殊字符");

    const numCharTypes = [hasUpper, hasLower, hasDigit, hasSpecial].filter(Boolean).length;
    if (numCharTypes >= 3) score += 1;
    if (numCharTypes === 4) score += 1;

    let strengthText, strengthClass;
    if (score >= 7) {
        strengthText = "强";
        strengthClass = "strength-强";
    } else if (score >= 4) {
        strengthText = "中";
        strengthClass = "strength-中";
    } else {
        strengthText = "弱";
        strengthClass = "strength-弱";
    }
    
    if (feedback.length > 0 && strengthText === "弱") {
        strengthText += ` (${feedback.slice(0, 2).join(', ')})`; // Show max 2 feedback items
    } else if (feedback.length > 0 && strengthText !== "强") {
         strengthText += ` (${feedback.slice(0,1).join('')})`; // Show 1 feedback for medium
    }


    return { strengthText, strengthClass };
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        updateStatusBar(`"${text.substring(0,10)}..." 已复制到剪贴板`);
    }).catch(err => {
        console.error('无法复制文本: ', err);
        updateStatusBar("复制失败", true);
        alert("无法复制到剪贴板，请手动复制。");
    });
}

function exportPasswordsToCSV() {
    const displayArea = document.getElementById('passwordsDisplayArea');
    const entries = displayArea.getElementsByClassName('password-entry');
    if (entries.length === 0) {
        alert('没有可导出的密码，请先生成密码');
        updateStatusBar('导出失败：无密码', true);
        return;
    }
    function formatDateTime(dt) {
        const pad = n => n.toString().padStart(2, '0');
        return dt.getFullYear() + '-' + pad(dt.getMonth()+1) + '-' + pad(dt.getDate()) + ' ' + pad(dt.getHours()) + ':' + pad(dt.getMinutes()) + ':' + pad(dt.getSeconds());
    }
    let csvContent = '日期,密码,强度\n';
    const now = new Date();
    const dateTimeStr = formatDateTime(now);
    for (let entry of entries) {
        const password = entry.querySelector('.password-text').textContent;
        const strength = entry.querySelector('.password-strength').textContent;
        const safeDate = '"' + dateTimeStr + '"';
        const safePassword = '"' + password.replace(/"/g, '""') + '"';
        const safeStrength = '"' + strength.replace(/"/g, '""') + '"';
        csvContent += `${safeDate},${safePassword},${safeStrength}\n`;
    }
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'generated_passwords.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    updateStatusBar('密码已导出为CSV');
}


// --- Status Bar Function ---
function updateStatusBar(message, isError = false) {
    const statusBar = document.getElementById('statusBar');
    statusBar.textContent = message;
    if (isError) {
        statusBar.className = 'status-bar status-error';
    } else {
        statusBar.className = 'status-bar status-success';
    }
    // Reset to default after 5 seconds
    setTimeout(() => {
        statusBar.textContent = "准备就绪";
        statusBar.className = 'status-bar';
    }, 5000);
}