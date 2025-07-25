// Dialog System JavaScript

class DialogSystem {
    constructor() {
        this.currentDialog = null;
        this.currentLineIndex = 0;
        this.dialogs = [];
        this.elements = {
            overlay: document.getElementById('dialogOverlay'),
            background: document.getElementById('dialogBackground'),
            speakerAvatar: document.getElementById('speakerAvatar'),
            speakerName: document.getElementById('speakerName'),
            dialogText: document.getElementById('dialogText'),
            progressText: document.getElementById('progressText'),
            progressFill: document.getElementById('progressFill'),
            previousBtn: document.getElementById('previousLine'),
            nextBtn: document.getElementById('nextLine'),
            completeBtn: document.getElementById('completeDialog'),
            closeBtn: document.getElementById('closeDialog'),
            dialogSelect: document.getElementById('dialogSelect'),
            loadBtn: document.getElementById('loadDialog')
        };
        
        this.init();
    }

    async init() {
        // Load dialogs data
        await this.loadDialogs();
        
        // Bind events
        this.bindEvents();
        
        // Check URL parameters for auto-load
        const urlParams = new URLSearchParams(window.location.search);
        const dialogId = urlParams.get('dialog');
        const questId = urlParams.get('quest');
        const dialogType = urlParams.get('type');
        
        if (dialogId) {
            this.currentQuestId = questId;
            this.currentDialogType = dialogType;
            this.loadDialog(parseInt(dialogId), questId, dialogType);
        } else {
            // Load first dialog for demo
            this.loadDialog(12);
        }
    }

    async loadDialogs() {
        try {
            const response = await fetch('/data/dialogs.json');
            this.dialogs = await response.json();
            console.log('Dialogs loaded:', this.dialogs.length);
        } catch (error) {
            console.error('Error loading dialogs:', error);
            // Fallback data for demo
            this.dialogs = [
                {
                    dialog_id: 12,
                    type: "start",
                    background: "village.jpg",
                    lines: [
                        { speaker: "elder", text: "Có phải bạn là một hiệp sĩ?" },
                        { speaker: "elder", text: "Hiệp sĩ mau giúp đỡ chúng tôi!" },
                        { speaker: "player", text: "Tôi sẽ giúp ngôi làng này. Nhưng có chuyện gì vậy?" },
                        { speaker: "elder", text: "Có quái vật xuất hiện ở làng phía đông!" },
                        { speaker: "player", text: "Tôi sẽ đến đó ngay lập tức!" }
                    ]
                }
            ];
        }
    }

    bindEvents() {
        // Navigation buttons
        this.elements.previousBtn.addEventListener('click', () => this.previousLine());
        this.elements.nextBtn.addEventListener('click', () => this.nextLine());
        this.elements.completeBtn.addEventListener('click', () => this.completeDialog());
        this.elements.closeBtn.addEventListener('click', () => this.closeDialog());
        
        // Debug controls
        this.elements.loadBtn.addEventListener('click', () => {
            const dialogId = parseInt(this.elements.dialogSelect.value);
            this.loadDialog(dialogId);
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (this.elements.overlay.style.display !== 'none') {
                switch (e.key) {
                    case 'ArrowRight':
                    case 'Space':
                    case 'Enter':
                        e.preventDefault();
                        this.nextLine();
                        break;
                    case 'ArrowLeft':
                        e.preventDefault();
                        this.previousLine();
                        break;
                    case 'Escape':
                        e.preventDefault();
                        this.closeDialog();
                        break;
                }
            }
        });
    }

    loadDialog(dialogId, questId = null, dialogType = null) {
        const dialog = this.dialogs.find(d => d.dialog_id === dialogId);
        if (!dialog) {
            console.error('Dialog not found:', dialogId);
            return;
        }

        this.currentDialog = dialog;
        this.currentQuestId = questId;
        this.currentDialogType = dialogType;
        this.currentLineIndex = 0;
        
        // Set background
        this.setBackground(dialog.background);
        
        // Show dialog and update display
        this.elements.overlay.style.display = 'flex';
        this.updateDisplay();
        
        console.log('Dialog loaded:', dialog.dialog_id, dialog.type, 'Quest:', questId);
    }

    setBackground(backgroundName) {
        // Remove existing background classes
        this.elements.background.className = 'dialog-background';
        
        // Add new background class
        const bgClass = backgroundName.replace('.jpg', '');
        this.elements.background.classList.add(bgClass);
    }

    updateDisplay() {
        if (!this.currentDialog || !this.currentDialog.lines[this.currentLineIndex]) {
            return;
        }

        const currentLine = this.currentDialog.lines[this.currentLineIndex];
        const totalLines = this.currentDialog.lines.length;
        
        // Update speaker info
        this.elements.speakerName.textContent = this.getSpeakerDisplayName(currentLine.speaker);
        this.elements.speakerAvatar.src = this.getSpeakerAvatar(currentLine.speaker);
        this.elements.speakerAvatar.alt = currentLine.speaker;
        
        // Update dialog text
        this.elements.dialogText.textContent = currentLine.text;
        
        // Update progress
        this.elements.progressText.textContent = `Line ${this.currentLineIndex + 1} of ${totalLines}`;
        const progressPercent = ((this.currentLineIndex + 1) / totalLines) * 100;
        this.elements.progressFill.style.width = `${progressPercent}%`;
        
        // Update button states
        this.elements.previousBtn.disabled = this.currentLineIndex === 0;
        
        const isLastLine = this.currentLineIndex === totalLines - 1;
        this.elements.nextBtn.style.display = isLastLine ? 'none' : 'flex';
        this.elements.completeBtn.style.display = isLastLine ? 'flex' : 'none';
    }

    getSpeakerDisplayName(speaker) {
        const displayNames = {
            'elder': 'Trưởng làng',
            'player': 'Người chơi',
            'merchant': 'Thương gia',
            'guard': 'Lính canh',
            'john-fisher': 'John - Ngư dân',
            'marcus-scholar': 'Marcus - Học giả',
            'mina-inn-keeper': 'Mina - Chủ quán trọ',
            'jack-sailor': 'Jack - Thủy thủ',
            'arch-mage': 'Đại pháp sư',
            'duke': 'Công tước',
            'kyrina-pirate-leader': 'Kyrina - Thủ lĩnh cướp biển',
            'mira-dancer': 'Mira - Vũ công',
            'amon-strange-merchant': 'Amon - Thương gia bí ẩn'
        };
        return displayNames[speaker] || speaker;
    }

    getSpeakerAvatar(speaker) {
        // Use the exact avatar file names
        const avatars = {
            'elder': '/static/img/avatar/elder.png',
            'player': '/static/img/avatar/player.png',
            'merchant': '/static/img/avatar/merchant.png',
            'guard': '/static/img/avatar/guard.png',
            'john-fisher': '/static/img/avatar/john-fisher.png',
            'marcus-scholar': '/static/img/avatar/marcus-scholar.png',
            'mina-inn-keeper': '/static/img/avatar/mina-inn-keeper.png',
            'jack-sailor': '/static/img/avatar/jack-sailor.png',
            'arch-mage': '/static/img/avatar/arch-mage.png',
            'duke': '/static/img/avatar/duke.png',
            'kyrina-pirate-leader': '/static/img/avatar/kyrina-pirate-leader.png',
            'mira-dancer': '/static/img/avatar/mira-dancer.png',
            'amon-strange-merchant': '/static/img/avatar/amon-strange-merchant.png'
        };
        return avatars[speaker] || '/static/img/avatar/default.png';
    }

    nextLine() {
        if (!this.currentDialog) return;
        
        const totalLines = this.currentDialog.lines.length;
        if (this.currentLineIndex < totalLines - 1) {
            this.currentLineIndex++;
            this.updateDisplay();
        }
    }

    previousLine() {
        if (!this.currentDialog) return;
        
        if (this.currentLineIndex > 0) {
            this.currentLineIndex--;
            this.updateDisplay();
        }
    }

    completeDialog() {
        console.log('Dialog completed:', this.currentDialog.dialog_id);
        
        // Send completion data to server
        this.sendDialogComplete();
        
        // Handle quest-related logic
        if (this.currentQuestId && this.currentDialogType) {
            this.handleQuestDialog();
        }
        
        // Close dialog
        this.closeDialog();
    }

    async handleQuestDialog() {
        if (!this.currentQuestId) return;
        
        try {
            if (this.currentDialogType === 'start') {
                // Starting a quest - add to user's active quests
                const response = await fetch('/api/start-quest', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        quest_id: this.currentQuestId
                    })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    console.log('Quest started:', result);
                    
                    // Show success message and redirect
                    alert('Quest đã được bắt đầu! Quay lại trang quests để tiếp tục.');
                    if (window.opener) {
                        window.opener.location.reload(); // Refresh parent window
                        window.close(); // Close dialog window
                    }
                }
            } else if (this.currentDialogType === 'complete') {
                // Completing a quest
                const response = await fetch('/api/complete-quest', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        quest_id: this.currentQuestId
                    })
                });
                
                if (response.ok) {
                    const result = await response.json();
                    console.log('Quest completed:', result);
                    
                    // Show rewards and redirect
                    alert(`Quest hoàn thành! Phần thưởng: ${result.rewards?.gold || 0} vàng, ${result.rewards?.exp || 0} EXP`);
                    if (window.opener) {
                        window.opener.location.reload();
                        window.close();
                    }
                }
            }
        } catch (error) {
            console.error('Error handling quest dialog:', error);
        }
    }

    closeDialog() {
        this.elements.overlay.style.display = 'none';
        this.currentDialog = null;
        this.currentLineIndex = 0;
    }

    async sendDialogComplete() {
        if (!this.currentDialog) return;
        
        try {
            const response = await fetch('/dialog/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    dialog_id: this.currentDialog.dialog_id,
                    type: this.currentDialog.type,
                    quest_id: this.currentQuestId,
                    dialog_type: this.currentDialogType
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                console.log('Dialog completion sent:', result);
            } else {
                console.error('Failed to send dialog completion');
            }
        } catch (error) {
            console.error('Error sending dialog completion:', error);
        }
    }

    // Public API for external calls
    static showDialog(dialogId) {
        if (window.dialogSystem) {
            window.dialogSystem.loadDialog(dialogId);
        }
    }
}

// Initialize dialog system when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.dialogSystem = new DialogSystem();
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DialogSystem;
}
