const { exec } = require('child_process');

const pythonInstaller = 'C:\\Path\\To\\Your\\python-2.7.15.amd64.msi';
const vsBuildToolsInstaller = 'C:\\Path\\To\\Your\\vs_BuildTools.exe';

exec(`msiexec /i ${pythonInstaller} /quiet`, (err, stdout, stderr) => {
    if (err) {
        console.error(`Python installation failed: ${stderr}`);
        return;
    }
    console.log('Python installed successfully.');

    exec(`${vsBuildToolsInstaller} --quiet --wait`, (err, stdout, stderr) => {
        if (err) {
            console.error(`Visual Studio Build Tools installation failed: ${stderr}`);
            return;
        }
        console.log('Visual Studio Build Tools installed successfully.');
    });
});
