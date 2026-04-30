const { app, BrowserWindow, ipcMain } = require('electron')
const path = require('path')
const { spawn, execSync } = require('child_process')

let mainWindow
let processes = {}

function killProcess(type) {
  const proc = processes[type]
  if (proc) {
    const pid = proc.pid
    delete processes[type]
    try { execSync(`taskkill /F /T /PID ${pid}`, { timeout: 3000 }) } catch(e) {}
    try { proc.kill('SIGKILL') } catch(e) {}
  }
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    backgroundColor: '#d0d0d0',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  })
  mainWindow.loadFile('index.html')
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
  Object.keys(processes).forEach(type => killProcess(type))
  app.quit()
})

ipcMain.handle('run-script', (event, scriptPath, type) => {
  killProcess(type)

  const proc = spawn('cmd.exe', ['/c', scriptPath], {
    shell: false,
    stdio: ['pipe', 'pipe', 'pipe']
  })

  processes[type] = proc

  proc.stdout.on('data', (data) => {
    if (!processes[type] || processes[type].pid !== proc.pid) return
    if (!mainWindow) return
    mainWindow.webContents.send('log', { type, data: data.toString() })
  })

  proc.stderr.on('data', (data) => {
    if (!processes[type] || processes[type].pid !== proc.pid) return
    if (!mainWindow) return
    mainWindow.webContents.send('log', { type, data: data.toString() })
  })

  proc.on('close', () => {
    if (processes[type] && processes[type].pid === proc.pid) {
      delete processes[type]
    }
  })

  return true
})

ipcMain.handle('stop-script', (event, type) => {
  killProcess(type)
  return true
})
