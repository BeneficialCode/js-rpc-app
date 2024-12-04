


const information = document.getElementById('info')
information.innerText = `This app is using Chrome (v${electronAPI.chrome()}), Node.js (v${electronAPI.node()}), and Electron (v${electronAPI.electron()})`

const setButton = document.getElementById('btn')
const titleInput = document.getElementById('title')
setButton.addEventListener('click', () => {
    const title = titleInput.value
    window.electronAPI.setTitle(title)

})

const openButton = document.getElementById('fileBtn')
const filePathElement = document.getElementById('filePath')

openButton.addEventListener('click', async () => {
    const filePath = await window.electronAPI.openFile()
    if (filePath) {
        filePathElement.innerText = filePath
    }
})

const counter = document.getElementById('counter')

window.electronAPI.onUpdateCounter((value) => {
    const oldValue = Number(counter.innerText)
    const newValue = oldValue + value
    counter.innerText = newValue.toString()
    window.electronAPI.counterValue(newValue)
})

