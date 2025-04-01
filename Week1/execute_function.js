const { exec } = require('child_process');

function isDockerAvailable(callback) {
    exec('docker --version', (error, stdout, stderr) => {
        if (error) {
            console.error('❌ Error: Docker CLI not found. Make sure Docker is installed and accessible.');
            callback(false);
        } else {
            callback(true);
        }
    });
}

function executeFunction(functionName, lang, timeout = 5) {
    const imageName = `$javascript-function`; // Match built images
    console.log(`🚀 Running ${functionName} in ${lang} with a timeout of ${timeout} seconds...`);

    isDockerAvailable((available) => {
        if (!available) {
            process.exit(1);
        }

        const command = `docker run --rm ${imageName}`;
        const process = exec(command, { timeout: timeout * 1000 }, (error, stdout, stderr) => {
            if (error) {
                if (error.killed) {
                    console.error(`❌ Function ${functionName} exceeded ${timeout} seconds and was terminated.`);
                } else {
                    console.error(`❌ Error: ${stderr}`);
                }
            } else {
                console.log(`✅ Output: ${stdout}`);
            }
        });

        process.on('error', (err) => {
            console.error(`❌ Error: ${err.message}`);
        });
    });
}

if (process.argv.length < 4) {
    console.log('Usage: node execute_function.js <function_name> <language> [timeout]');
    process.exit(1);
}

const functionName = process.argv[2];
const lang = process.argv[3];
const timeout = process.argv[4] ? parseInt(process.argv[4], 10) : 5; // Default timeout: 5 seconds

executeFunction(functionName, lang, timeout);