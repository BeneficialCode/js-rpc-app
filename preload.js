const { contextBridge,ipcRenderer } = require('electron')


/*
默认情况下，渲染器进程没有权限访问 Node.js 和 Electron 模块。 作为应用开发者，需要使用 contextBridge API 来选择要从预加载脚本中暴露哪些 API
*/
contextBridge.exposeInMainWorld('electronAPI', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron,
  // 发送消息给主进程
  setTitle: (title) => ipcRenderer.send('set-title', title),
  // we can also expose variables, not just functions
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  onUpdateCounter: (callback) => ipcRenderer.on('update-counter', (_event, value) => callback(value)),
  counterValue: (value) => ipcRenderer.send('counter-value', value),
})