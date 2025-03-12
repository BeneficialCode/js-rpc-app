const {app,BrowserWindow, ipcMain,dialog,Menu, globalShortcut} = require('electron');
const path = require('node:path')
const WebSocket = require('ws')



// 在全局范围内声明一个变量来存储主窗口的引用
let mainWindow;

// 声明一个全局变量来存储 WebSocket 客户端
let rpcClient;

// 回调函数
async function handleFileOpen () {
    const { canceled, filePaths } = await dialog.showOpenDialog()
    if (!canceled) {
      return filePaths[0]
    }
}

function handleSetTitle(event,title) {
    const webContents = event.sender
    const win = BrowserWindow.fromWebContents(webContents)
    if(win){
        win.setTitle(title)
    }
}

const createWindow = () => {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences:{
            preload: path.join(__dirname, 'preload.js'),
            devTools: true,
            nodeIntegration: true,
            contextIsolation: true,
            webSecurity: true,
            allowRunningInsecureContent: false
        }
    });

    // 接收渲染进程发送的消息
    ipcMain.on('set-title',handleSetTitle)

    ipcMain.on('counter-value', (_event, value) => {
        console.log(value) // will print value to Node console
    })

    const menu = Menu.buildFromTemplate([
        {
          label: app.name,
          submenu: [
            {
              click: () => mainWindow.webContents.send('update-counter', 1),
              label: 'Increment'
            },
            {
              click: () => mainWindow.webContents.send('update-counter', -1),
              label: 'Decrement'
            }
          ]
        }
    ])
    Menu.setApplicationMenu(menu)

    // 打开开发者工具
    mainWindow.webContents.openDevTools();
    
    // win.loadURL('https://login.189.cn/login')
    mainWindow.loadFile('index.html')
    
    //mainWindow.loadURL('https://passport.vivo.com.cn/#/login')
}

app.whenReady().then(() => {
    ipcMain.handle('dialog:openFile', handleFileOpen)
    createWindow()

    // 注册全局快捷键
    globalShortcut.register('CommandOrControl+Shift+I', () => {
        const win = BrowserWindow.getFocusedWindow();
        if (win) {
            win.webContents.toggleDevTools();
        }
    });

    // 在主窗口创建后创建 WebSocket 客户端
    rpcClient = new Hlclient("ws://127.0.0.1:12080/ws?group=rpc&clientId=VirtualCC/"+new Date().getTime());

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
      }
    })
})

// 当应用退出时，取消注册所有快捷键
app.on('will-quit', () => {
    globalShortcut.unregisterAll();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
})

function Hlclient(wsURL) {
  this.wsURL = wsURL;
  this.handlers = {
      _execjs: function (resolve, param) {
          // 使用全局存储的主窗口引用
          if (mainWindow && !mainWindow.isDestroyed()) {
              // 使用 webContents.executeJavaScript 在 DevTools 控制台的上下文中执行代码
              // 这样可以访问到 DevTools 环境中的所有对象，包括 window._dx
              mainWindow.webContents.executeJavaScript(param)
                  .then(result => {
                      console.log('DevTools 执行结果:', result);
                      
                      // 处理结果，确保它可以被序列化
                      try {
                          // 尝试序列化结果
                          JSON.stringify(result);
                          resolve(result);
                      } catch (serializeError) {
                          console.warn('结果无法序列化:', serializeError);
                          
                          // 返回一个可序列化的对象
                          if (result === undefined) {
                              resolve({ value: 'undefined' });
                          } else if (result === null) {
                              resolve({ value: 'null' });
                          } else if (typeof result === 'function') {
                              resolve({ value: '[Function]', type: 'function' });
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
                              resolve(safeResult);
                          } else {
                              resolve({ value: String(result), type: typeof result });
                          }
                      }
                  })
                  .catch(error => {
                      console.error('DevTools 执行出错:', error);
                      resolve({ error: error.message });
                  });
          } else {
              resolve({ error: "没有可用的窗口来执行 JavaScript" });
          }
      }
  };
  this.socket = undefined;
  if (!wsURL) {
      throw new Error('wsURL can not be empty!!')
  }
  this.connect()
}

Hlclient.prototype.connect = function () {
  console.log('begin of connect to wsURL: ' + this.wsURL);
  var _this = this;
  try {
      this.socket = new WebSocket(this.wsURL);
      this.socket.on('message', function (data) {
          _this.handlerRequest(data)
      })
  } catch (e) {
      console.log("connection failed,reconnect after 10s");
      setTimeout(function () {
          _this.connect()
      }, 10000)
  }
  this.socket.on('close', function () {
      console.log('rpc已关闭');
      setTimeout(function () {
          _this.connect()
      }, 10000)
  })
  this.socket.on('error', (error) => {  
      console.log('WebSocket connection onerror',error)
  })
  this.socket.on('open', function () {
      console.log('rpc已连接');
  })

};
Hlclient.prototype.send = function (msg) {
  this.socket.send(msg)
}

Hlclient.prototype.regAction = function (func_name, func) {
  if (typeof func_name !== 'string') {
      throw new Error("an func_name must be string");
  }
  if (typeof func !== 'function') {
      throw new Error("must be function");
  }
  console.log("register func_name: " + func_name);
  this.handlers[func_name] = func;
  return true

}

//收到消息后这里处理，
Hlclient.prototype.handlerRequest = function (requestJson) {
  var _this = this;
  try {
      var result = JSON.parse(requestJson)
  } catch (error) {
      console.log("请求信息解析错误", requestJson);
      return
  }
  if (!result['action'] || !result["message_id"]) {
      console.warn('没有方法或者消息id,不处理');
      return
  }
  var action = result["action"], message_id = result["message_id"]
  var theHandler = this.handlers[action];
  if (!theHandler) {
      this.sendResult(action, message_id, 'action没找到');
      return
  }
  try {
      if (!result["param"]) {
          theHandler(function (response) {
              _this.sendResult(action, message_id, response);
          })
          return
      }
      var param = result["param"]
      try {
          param = JSON.parse(param)
      } catch (e) {
      }
      theHandler(function (response) {
          _this.sendResult(action, message_id, response);
      }, param)

  } catch (e) {
      console.log("error: " + e);
      _this.sendResult(action, message_id, e);
  }
}

Hlclient.prototype.sendResult = function (action, message_id, e) {
  if (typeof e === 'object' && e !== null) {
      try {
          e = JSON.stringify(e)
      } catch (v) {
          console.log(v)//不是json无需操作
      }
  }
  this.send(JSON.stringify({"action": action, "message_id": message_id, "response_data": e}));
}




