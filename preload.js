const { contextBridge,ipcRenderer } = require('electron')
const JSEncrypt = require("jsencrypt")

contextBridge.exposeInMainWorld("JSEncrypt", {
    encrypt: (message, publicKey) => {
        const encryptor = new JSEncrypt();
        encryptor.setPublicKey(publicKey);
        return encryptor.encrypt(message);
    }
});

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
  // 添加执行 JavaScript 的功能
  executeJavaScript: (code) => {
    try {
      // 使用 Function 构造函数代替 eval
      // 对于包含多个语句的代码，不使用 return 包装
      let result;
      // 创建一个可以捕获最后一个表达式结果的函数
      const executeFunction = new Function(`
        ${code}
        // 如果代码最后一行是表达式，它的值会被返回
      `);
      result = executeFunction();
      
      // 处理结果，确保它可以被序列化
      try {
        // 尝试序列化结果，检查是否可以通过 IPC 传递
        JSON.stringify(result);
        return result;
      } catch (serializeError) {
        console.warn('结果无法序列化:', serializeError);
        
        // 根据结果类型返回适当的信息
        if (result === undefined) {
          return { value: 'undefined' };
        } else if (result === null) {
          return { value: 'null' };
        } else if (typeof result === 'function') {
          return { value: '[Function]', type: 'function' };
        } else if (typeof result === 'object') {
          // 对于对象，尝试提取可序列化的属性
          const safeResult = {};
          for (const key in result) {
            try {
              const value = result[key];
              // 检查属性值是否可序列化
              JSON.stringify(value);
              safeResult[key] = value;
            } catch (e) {
              safeResult[key] = `[Unserializable: ${typeof value}]`;
            }
          }
          return safeResult;
        } else {
          return { value: String(result), type: typeof result };
        }
      }
    } catch (error) {
      console.error('执行 JavaScript 时出错:', error);
      return { error: error.message };
    }
  }
})

// 监听来自主进程的 execute-javascript 事件
ipcRenderer.on('execute-javascript', (event, code) => {
  try {
    // 使用 Function 构造函数代替 eval
    // 对于包含多个语句的代码，不使用 return 包装
    let result;
    // 创建一个可以捕获最后一个表达式结果的函数
    const executeFunction = new Function(`
      ${code}
      // 如果代码最后一行是表达式，它的值会被返回
    `);
    result = executeFunction();
    
    // 处理结果，确保它可以被序列化
    try {
      // 尝试序列化结果，检查是否可以通过 IPC 传递
      JSON.stringify(result);
    } catch (serializeError) {
      // 如果无法序列化，返回一个可序列化的对象
      console.warn('结果无法序列化:', serializeError);
      
      // 根据结果类型返回适当的信息
      if (result === undefined) {
        result = { value: 'undefined' };
      } else if (result === null) {
        result = { value: 'null' };
      } else if (typeof result === 'function') {
        result = { value: '[Function]', type: 'function' };
      } else if (typeof result === 'object') {
        // 对于对象，尝试提取可序列化的属性
        const safeResult = {};
        for (const key in result) {
          try {
            const value = result[key];
            // 检查属性值是否可序列化
            JSON.stringify(value);
            safeResult[key] = value;
          } catch (e) {
            safeResult[key] = `[Unserializable: ${typeof value}]`;
          }
        }
        result = safeResult;
      } else {
        result = { value: String(result), type: typeof result };
      }
    }
    
    // 将结果发送回主进程
    ipcRenderer.send('execute-javascript-result', result);
  } catch (error) {
    console.error('执行 JavaScript 时出错:', error);
    // 如果执行出错，发送错误信息
    ipcRenderer.send('execute-javascript-result', { error: error.message });
  }
});