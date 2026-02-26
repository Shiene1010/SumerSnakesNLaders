export class CYOAEngine {
    constructor() {
        this.reset();
    }

    reset() {
        this.gold = 10;
        this.stamina = 10;
        this.karma = 0;
        this.currentNode = "start";
        this.gameOver = false;
        // Do not nullify themeData here as loadTheme calls reset() after setting data
    }

    loadTheme(data) {
        this.themeData = data;
        this.reset();
        // Allow theme to override starting stats if defined
        if (data.initialStats) {
            this.gold = data.initialStats.gold ?? 10;
            this.stamina = data.initialStats.stamina ?? 10;
            this.karma = data.initialStats.karma ?? 0;
        }
    }

    applyEffects(effects) {
        if (!effects) return;
        if (effects.gold) this.gold += effects.gold;
        if (effects.stamina) this.stamina += effects.stamina;
        if (effects.karma) this.karma += effects.karma;
    }

    makeChoice(index) {
        const node = this.themeData.scenarios[this.currentNode];
        const choice = node.options[index];

        // Custom Requirement Checks (e.g., Karma gating)
        if (choice.requirement) {
            const { stat, min } = choice.requirement;
            if (this[stat] < min) {
                return {
                    success: false,
                    message: `Requirement not met: ${stat.toUpperCase()} must be at least ${min}.`
                };
            }
        }

        this.applyEffects(choice.effects);
        this.currentNode = choice.next;

        if (this.stamina <= 0) {
            this.gameOver = true;
            return { success: true, event: 'exhaustion' };
        }

        const nextNode = this.themeData.scenarios[this.currentNode];
        if (!nextNode.options || nextNode.options.length === 0) {
            this.gameOver = true;
            return { success: true, event: 'finish' };
        }

        return { success: true };
    }

    getCurrentNode() {
        return this.themeData.scenarios[this.currentNode];
    }
}
