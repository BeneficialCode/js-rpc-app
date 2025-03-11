const {app,BrowserWindow, ipcMain,dialog,Menu} = require('electron');
const path = require('node:path')
const WebSocket = require('ws')

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
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences:{
            preload: path.join(__dirname, 'preload.js')
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

    // win.loadURL('https://login.189.cn/login')
    mainWindow.loadFile('index.html')

    
}

app.whenReady().then(() => {
    ipcMain.handle('dialog:openFile', handleFileOpen)
    createWindow()

    

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
      }
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
})



function Hlclient(wsURL) {
  this.wsURL = wsURL;
  this.handlers = {
      _execjs: function (resolve, param) {
          var res = eval(param)
          if (!res) {
              resolve("没有返回值")
          } else {
              resolve(res)
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

var demo = new Hlclient("ws://127.0.0.1:12080/ws?group=rpc&clientId=VirtualCC/"+new Date().getTime())




