const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('api', {
  run: (scriptPath, type) => ipcRenderer.invoke('run-script', scriptPath, type),
  stop: (type) => ipcRenderer.invoke('stop-script', type),
  onLog: (callback) => ipcRenderer.on('log', (_, payload) => callback(payload))
})
