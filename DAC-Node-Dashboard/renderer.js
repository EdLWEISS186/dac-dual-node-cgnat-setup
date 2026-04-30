const base = 'scripts'

const paths = {
  winStart:  `${base}\\Windows\\start-node.bat`,
  wslStart:  `${base}\\WSL_Linux\\start-node.bat`,
  winMon:    `${base}\\Windows\\Monitor.bat`,
  winLog:    `${base}\\Windows\\Logging.bat`,
  wslMon:    `${base}\\WSL_Linux\\Monitor.bat`,
  wslLog:    `${base}\\WSL_Linux\\logging.bat`,
}

let currentMonitorMode = 'monitor'

// ─── ANSI COLOR PARSER ────────────────────────────────────────────────────────
function ansiToHtml(text) {
  // Strip all ANSI escape sequences except color codes we handle
  const ansiMap = {
    '30': 'ansi-white',   // black → show as white
    '31': 'ansi-red',
    '32': 'ansi-green',
    '33': 'ansi-yellow',
    '34': 'ansi-white',   // blue → white
    '35': 'ansi-white',   // magenta → white
    '36': 'ansi-cyan',
    '37': 'ansi-white',
    '90': 'ansi-white',   // bright black (gray)
    '91': 'ansi-red',
    '92': 'ansi-green',
    '93': 'ansi-yellow',
    '94': 'ansi-white',
    '95': 'ansi-white',
    '96': 'ansi-cyan',
    '97': 'ansi-white',
  }

  // Escape HTML special chars first
  text = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  let result = ''
  let currentClass = null
  // Match ANSI escape sequences
  const parts = text.split(/(\x1b\[[0-9;]*m)/)

  for (const part of parts) {
    if (part.startsWith('\x1b[')) {
      const code = part.slice(2, -1)
      if (code === '0' || code === '') {
        // Reset
        if (currentClass) { result += '</span>'; currentClass = null }
      } else {
        const codes = code.split(';')
        for (const c of codes) {
          const cls = ansiMap[c]
          if (cls) {
            if (currentClass) result += '</span>'
            currentClass = cls
            result += `<span class="${cls}">`
            break
          }
        }
      }
    } else {
      result += part
    }
  }

  if (currentClass) result += '</span>'
  return result
}

// Also color INFO/WARN/ERROR lines without ANSI codes
function colorLogLine(text) {
  if (text.includes('\x1b[')) return ansiToHtml(text)
  // Fallback: color by keyword
  const lines = text.split('\n')
  return lines.map(line => {
    if (line.includes('WARN')) return `<span class="ansi-yellow">${line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</span>`
    if (line.includes('ERROR') || line.includes('Fatal')) return `<span class="ansi-red">${line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}</span>`
    if (line.includes('INFO')) return line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    return line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
  }).join('\n')
}

// Append colored HTML to a console box
function appendToBox(box, text) {
  const html = colorLogLine(text)
  const div = document.createElement('div')
  div.innerHTML = html
  // Append each child node
  while (div.firstChild) box.appendChild(div.firstChild)
  box.scrollTop = box.scrollHeight
}

// ─── ZOOM ─────────────────────────────────────────────────────────────────────
const fontSizes = { winNodeBox: 8.5, wslNodeBox: 8.5, winMonBox: 8.5, wslMonBox: 8.5 }

function zoomPanel(id, delta) {
  fontSizes[id] = Math.min(20, Math.max(4, fontSizes[id] + delta))
  document.getElementById(id).style.fontSize = fontSizes[id] + 'px'
}

document.querySelectorAll('.console').forEach(box => {
  box.addEventListener('wheel', (e) => {
    if (e.ctrlKey) {
      e.preventDefault()
      zoomPanel(box.id, e.deltaY < 0 ? 1 : -1)
    }
  }, { passive: false })
})

// ─── NODE CONTROLS ────────────────────────────────────────────────────────────
document.getElementById('btnStartNode').addEventListener('click', () => {
  window.api.run(paths.winStart, 'win-node')
  window.api.run(paths.wslStart, 'wsl-node')
  setStatus('NODE RUNNING...')
})

document.getElementById('btnStopNode').addEventListener('click', () => {
  window.api.stop('win-node')
  window.api.stop('wsl-node')
  setStatus('NODE STOPPED')
})

// ─── MONITOR CONTROLS ─────────────────────────────────────────────────────────
document.getElementById('btnStartMonitor').addEventListener('click', () => {
  currentMonitorMode = document.querySelector('input[name="mode"]:checked').value
  document.getElementById('winMonBox').innerHTML = ''
  document.getElementById('wslMonBox').innerHTML = ''

  if (currentMonitorMode === 'monitor') {
    window.api.run(paths.winMon, 'win-monitor')
    window.api.run(paths.wslMon, 'wsl-monitor')
    setMonitorStatus('MONITORING...')
  } else {
    window.api.run(paths.winLog, 'win-monitor')
    window.api.run(paths.wslLog, 'wsl-monitor')
    setMonitorStatus('LOGGING...')
  }
})

document.getElementById('btnStopMonitor').addEventListener('click', () => {
  window.api.stop('win-monitor')
  window.api.stop('wsl-monitor')
  document.getElementById('winMonBox').innerHTML = ''
  document.getElementById('wslMonBox').innerHTML = ''
  setMonitorStatus('STOPPED')
})

function setStatus(t) { document.getElementById('nodeStatus').innerText = t }
function setMonitorStatus(t) { document.getElementById('monitorStatus').innerText = t }

// ─── LOG ROUTING ──────────────────────────────────────────────────────────────
const boxes = {
  'win-node':    document.getElementById('winNodeBox'),
  'wsl-node':    document.getElementById('wslNodeBox'),
  'win-monitor': document.getElementById('winMonBox'),
  'wsl-monitor': document.getElementById('wslMonBox'),
}

// Per-box pending buffer for monitor clear detection
const pendingBuffers = { 'win-monitor': '', 'wsl-monitor': '' }

window.api.onLog(({ type, data }) => {
  const box = boxes[type]
  if (!box) return

  const isMonitor = (type === 'win-monitor' || type === 'wsl-monitor')

  if (isMonitor && currentMonitorMode === 'monitor') {
    pendingBuffers[type] += data

    // Process all complete [CLR] cycles in buffer
    while (pendingBuffers[type].includes('[CLR]')) {
      const idx = pendingBuffers[type].indexOf('[CLR]')
      // Everything before [CLR] — discard (previous cycle tail)
      // Everything after [CLR] — new cycle content
      pendingBuffers[type] = pendingBuffers[type].slice(idx + 5) // 5 = '[CLR]'.length
      box.innerHTML = ''
    }

    // Append whatever is left in buffer
    if (pendingBuffers[type].trim()) {
      appendToBox(box, pendingBuffers[type])
      pendingBuffers[type] = ''
    }
  } else {
    appendToBox(box, data)
  }
})
