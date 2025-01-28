class DigitalNucleotide {
    constructor(value) {
        this.value = value;
        this.generation = 0;
        this.mutationHistory = [];
    }

    complement() {
        return new DigitalNucleotide(this.value ^ 0b11);
    }

    mutate() {
        const oldValue = this.value;
        // Advanced mutation patterns
        const mutationType = Math.random();
        
        if (mutationType < 0.7) {  // Point mutation
            this.value = Math.floor(Math.random() * 4);
        } else if (mutationType < 0.85) {  // Bit flip
            this.value = this.value ^ (Math.random() < 0.5 ? 0b01 : 0b10);
        } else {  // Complement mutation
            this.value = this.value ^ 0b11;
        }

        this.mutationHistory.push({
            generation: this.generation,
            from: oldValue,
            to: this.value,
            type: mutationType < 0.7 ? 'point' : mutationType < 0.85 ? 'bit-flip' : 'complement'
        });
        
        this.generation++;
        return this;
    }
}

class DigitalDNA {
    constructor(sequence = []) {
        this.sequence = sequence.map(v => new DigitalNucleotide(v));
        this.generation = 0;
        this.fitness = 0;
        this.mutationRates = {
            point: 0.001,    // Basic point mutations
            insertion: 0.0005, // Insert new nucleotides
            deletion: 0.0005,  // Remove nucleotides
            duplication: 0.0002, // Duplicate segments
            inversion: 0.0002   // Reverse segments
        };
    }

    createComplementaryStrand() {
        return new DigitalDNA(
            this.sequence.map(nucleotide => nucleotide.complement().value)
        );
    }

    // Enhanced replication with multiple types of mutations
    replicate() {
        let newSequence = [...this.sequence];

        // Handle insertions
        if (Math.random() < this.mutationRates.insertion) {
            const position = Math.floor(Math.random() * (newSequence.length + 1));
            newSequence.splice(position, 0, new DigitalNucleotide(Math.floor(Math.random() * 4)));
        }

        // Handle deletions
        if (Math.random() < this.mutationRates.deletion && newSequence.length > 1) {
            const position = Math.floor(Math.random() * newSequence.length);
            newSequence.splice(position, 1);
        }

        // Handle duplications
        if (Math.random() < this.mutationRates.duplication) {
            const start = Math.floor(Math.random() * newSequence.length);
            const length = Math.floor(Math.random() * (newSequence.length - start)) + 1;
            const segment = newSequence.slice(start, start + length);
            newSequence.splice(start, 0, ...segment.map(n => new DigitalNucleotide(n.value)));
        }

        // Handle inversions
        if (Math.random() < this.mutationRates.inversion) {
            const start = Math.floor(Math.random() * (newSequence.length - 1));
            const length = Math.floor(Math.random() * (newSequence.length - start)) + 1;
            const segment = newSequence.slice(start, start + length).reverse();
            newSequence.splice(start, length, ...segment);
        }

        // Point mutations
        newSequence = newSequence.map(nucleotide => {
            if (Math.random() < this.mutationRates.point) {
                return nucleotide.mutate();
            }
            return new DigitalNucleotide(nucleotide.value);
        });

        const offspring = new DigitalDNA(newSequence.map(n => n.value));
        offspring.generation = this.generation + 1;
        offspring.mutationRates = {...this.mutationRates};
        return offspring;
    }

    // Enhanced crossover with multiple crossover points
    crossover(otherDNA) {
        const numCrossoverPoints = Math.floor(Math.random() * 3) + 1; // 1-3 crossover points
        const points = Array(numCrossoverPoints)
            .fill(0)
            .map(() => Math.floor(Math.random() * this.sequence.length))
            .sort((a, b) => a - b);

        let currentStrand = true; // true = this DNA, false = other DNA
        let newSequence = [];
        let lastPoint = 0;

        points.forEach(point => {
            const segment = (currentStrand ? this : otherDNA)
                .sequence.slice(lastPoint, point)
                .map(n => n.value);
            newSequence.push(...segment);
            currentStrand = !currentStrand;
            lastPoint = point;
        });

        // Add remaining segment
        const finalSegment = (currentStrand ? this : otherDNA)
            .sequence.slice(lastPoint)
            .map(n => n.value);
        newSequence.push(...finalSegment);

        const offspring = new DigitalDNA(newSequence);
        offspring.generation = Math.max(this.generation, otherDNA.generation) + 1;
        
        // Inherit mutation rates with possible variations
        offspring.mutationRates = Object.fromEntries(
            Object.entries(this.mutationRates).map(([key, rate]) => {
                const variation = (Math.random() - 0.5) * 0.1 * rate; // ±5% variation
                return [key, Math.max(0, rate + variation)];
            })
        );
        
        return offspring;
    }

    // Calculate sequence entropy as a measure of complexity
    calculateEntropy() {
        const frequencies = this.sequence.reduce((freq, nucleotide) => {
            freq[nucleotide.value] = (freq[nucleotide.value] || 0) + 1;
            return freq;
        }, {});

        return -Object.values(frequencies).reduce((entropy, count) => {
            const probability = count / this.sequence.length;
            return entropy + probability * Math.log2(probability);
        }, 0);
    }

    // Calculate evolutionary distance from ancestor
    calculateDistance(ancestorDNA) {
        if (this.sequence.length !== ancestorDNA.sequence.length) {
            return 1; // Maximum distance for different lengths
        }

        const differences = this.sequence.filter((nucleotide, index) =>
            nucleotide.value !== ancestorDNA.sequence[index].value
        ).length;

        return differences / this.sequence.length;
    }

    // Get mutation statistics
    getMutationStats() {
        return this.sequence.reduce((stats, nucleotide) => {
            nucleotide.mutationHistory.forEach(mutation => {
                stats.total++;
                stats.types[mutation.type] = (stats.types[mutation.type] || 0) + 1;
            });
            return stats;
        }, { total: 0, types: {} });
    }

    // Optimize mutation rates based on fitness history
    optimizeMutationRates(fitnessHistory) {
        if (fitnessHistory.length < 2) return;

        const recentFitness = fitnessHistory.slice(-2);
        const fitnessChange = recentFitness[1] - recentFitness[0];

        // Adjust rates based on fitness trajectory
        Object.keys(this.mutationRates).forEach(key => {
            if (fitnessChange > 0) {
                // Slightly increase rates when fitness is improving
                this.mutationRates[key] *= 1.1;
            } else {
                // Decrease rates when fitness is declining
                this.mutationRates[key] *= 0.9;
            }
            // Ensure rates stay within reasonable bounds
            this.mutationRates[key] = Math.max(0.0001, Math.min(0.01, this.mutationRates[key]));
        });
    }
}

// Example usage:
const originalSequence = [0, 1, 2, 3, 0, 1, 2, 3];
const dna1 = new DigitalDNA(originalSequence);
const dna2 = new DigitalDNA(originalSequence.reverse());

// Simulate evolution
let evolved = dna1;
const fitnessHistory = [];

for (let i = 0; i < 10; i++) {
    evolved = evolved.replicate();
    evolved.fitness = evolved.calculateEntropy(); // Using entropy as fitness
    fitnessHistory.push(evolved.fitness);
    evolved.optimizeMutationRates(fitnessHistory);
}

console.log("Original DNA:", originalSequence);
console.log("Evolved DNA:", evolved.sequence.map(n => n.value));
console.log("Generation:", evolved.generation);
console.log("Entropy:", evolved.calculateEntropy());
console.log("Mutation Stats:", evolved.getMutationStats());
console.log("Final Mutation Rates:", evolved.mutationRates);
