const fs = require('fs');
const path = require('path');
const DigitalSperm = require('./digital-sperm.js');
const DigitalEgg = require('./digital-egg.js');
const DigitalEmbryo = require('./digital-embryo.js');

function conceive() {
    // Create new sperm and egg cells
    const sperm = new DigitalSperm();
    const egg = new DigitalEgg();
    
    // Ensure viability
    if (!sperm.isViable() || !egg.isViable()) {
        console.log('Conception failed: Gametes not viable');
        return null;
    }
    
    // Create embryo
    const embryo = new DigitalEmbryo(sperm, egg);
    
    // Save embryo data
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const embryoData = {
        creationTime: timestamp,
        status: embryo.getStatus(),
        genome: embryo.genome,
        parentalData: {
            sperm: sperm.getGeneticProfile(),
            egg: egg.getGeneticProfile()
        }
    };
    
    // Create embryos directory if it doesn't exist
    const embryosDir = path.join(__dirname, 'embryos');
    if (!fs.existsSync(embryosDir)) {
        fs.mkdirSync(embryosDir);
    }
    
    // Save embryo to file
    const filename = path.join(embryosDir, `embryo-${timestamp}.json`);
    fs.writeFileSync(filename, JSON.stringify(embryoData, null, 2));
    
    console.log(`Embryo created successfully!`);
    console.log(`Saved to: ${filename}`);
    console.log('\nEmbryo Status:');
    console.log('==============');
    console.log(`Developmental Stage: ${embryo.developmentalStage}`);
    console.log(`Cell Count: ${embryo.cellCount}`);
    console.log(`Viability: ${(embryo.properties.viability * 100).toFixed(2)}%`);
    console.log(`Sex: ${embryo.genome.sex}`);
    console.log(`Genetic Health Score: ${(embryo.properties.geneticHealth.overallHealth * 100).toFixed(2)}%`);
    
    return embryo;
}

// Execute conception
conceive();