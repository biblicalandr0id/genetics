class GeneticDominanceHandler {
    constructor() {
        // Define dominance rules for specialized traits
        this.specializationDominance = {
            pattern_recognition: {
                dominantPatterns: [3, 2], // Higher values are dominant
                recessivePatterns: [0, 1]
            },
            learning_rate: {
                dominantPatterns: [2, 3],
                recessivePatterns: [0, 1]
            },
            memory_formation: {
                dominantPatterns: [0, 3],
                recessivePatterns: [1, 2]
            },
            decision_making: {
                dominantPatterns: [1, 2],
                recessivePatterns: [0, 3]
            },
            data_processing: {
                dominantPatterns: [0, 1],
                recessivePatterns: [2, 3]
            },
            neural_plasticity: {
                dominantPatterns: [2, 3],
                recessivePatterns: [0, 1]
            },
            problem_solving: {
                dominantPatterns: [1, 3],
                recessivePatterns: [0, 2]
            },
            adaptation_speed: {
                dominantPatterns: [3, 2],
                recessivePatterns: [1, 0]
            },
            environmental_sensing: {
                dominantPatterns: [2, 3],
                recessivePatterns: [0, 1]
            },
            knowledge_integration: {
                dominantPatterns: [3, 1],
                recessivePatterns: [2, 0]
            }
        };
    }

    // Determine trait expression when combining sperm and egg genes
    determineTrait(spermGene, eggGene, specialization = null) {
        // If either gene is suppressed, it doesn't contribute to trait
        if (spermGene.suppressed && eggGene.suppressed) {
            return {
                value: 0, // Default value when both are suppressed
                expressed: false
            };
        }

        // If one gene is suppressed, use the other
        if (spermGene.suppressed) return {
            value: eggGene.value,
            expressed: true
        };
        if (eggGene.suppressed) return {
            value: spermGene.value,
            expressed: true
        };

        // Handle specialized chromosome traits
        if (specialization) {
            return this.determineSpecializedTrait(spermGene, eggGene, specialization);
        }

        // Standard dominance rules for non-specialized genes
        if (spermGene.dominant && eggGene.dominant) {
            // Co-dominance: average the values
            return {
                value: Math.floor((spermGene.value + eggGene.value) / 2),
                expressed: true
            };
        } else if (spermGene.dominant) {
            return {
                value: spermGene.value,
                expressed: true
            };
        } else if (eggGene.dominant) {
            return {
                value: eggGene.value,
                expressed: true
            };
        } else {
            // Both recessive