import { CYOAEngine } from './engine.js';

class GameController {
    constructor() {
        this.engine = new CYOAEngine();
        this.views = {
            gallery: document.getElementById('theme-gallery'),
            game: document.getElementById('game-screen')
        };
        this.narrativeEl = document.getElementById('narrative-text');
        this.choicesEl = document.getElementById('choices-container');

        // Stat elements
        this.stats = {
            gold: document.getElementById('gold-val'),
            stamina: document.getElementById('stamina-val'),
            karma: document.getElementById('karma-val')
        };
    }

    async selectTheme(themeId) {
        try {
            // In Vite, files in 'public' are served at the root. 
            // Using 'data/' ensures we hit the public/data directory.
            const response = await fetch(`data/${themeId}.json`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            this.engine.loadTheme(data);
            this.showView('game');
            this.updateUI();
        } catch (err) {
            console.error('Failed to load theme:', err);
            alert('Error loading theme data.');
        }
    }

    showView(viewId) {
        Object.keys(this.views).forEach(v => {
            this.views[v].classList.remove('active');
        });
        this.views[viewId].classList.add('active');
    }

    updateUI() {
        const node = this.engine.getCurrentNode();

        // Update Stats
        this.stats.gold.textContent = this.engine.gold;
        this.stats.stamina.textContent = this.engine.stamina;
        this.stats.karma.textContent = this.engine.karma;

        // Update Narrative
        this.narrativeEl.innerHTML = `<p>${node.description}</p>`;
        this.narrativeEl.className = 'fade-in-text';

        // Update Choices
        this.choicesEl.innerHTML = '';
        if (this.engine.gameOver) {
            const restartBtn = document.createElement('button');
            restartBtn.className = 'choice-btn primary';
            restartBtn.textContent = 'Return to Menu';
            restartBtn.onclick = () => this.quitToMenu();
            this.choicesEl.appendChild(restartBtn);
        } else {
            node.options.forEach((opt, idx) => {
                const btn = document.createElement('button');
                btn.className = 'choice-btn';
                btn.textContent = opt.text;
                btn.onclick = () => this.handleChoice(idx);
                this.choicesEl.appendChild(btn);
            });
        }
    }

    handleChoice(index) {
        const result = this.engine.makeChoice(index);
        if (result.success) {
            this.updateUI();
        } else {
            alert(result.message);
        }
    }

    quitToMenu() {
        this.showView('gallery');
    }
}

// Global expose for onclick handlers in HTML
window.game = new GameController();
