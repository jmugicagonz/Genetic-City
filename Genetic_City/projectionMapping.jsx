const WebSocket = require('ws')
const uiData = {
  time: 86400, //time of day in seconds
  ABMLayer: {
    active: true, //bool
    ABMmode: 'mode', //state
    zoomLevel: 12, //mapbox zoom levels
  },
  AggregatedTripsLayer: {
    active: true,
    ABMmode: 'mode',
  },
  GridLayer: {
    active: true,
  },
  AccessLayer: {
    active: true,
    accessToggle: 0,
  },
}
const server = new WebSocket.Server({ port: 8080 })

server.on('connection', (socket) => {
  socket.send(JSON.stringify(uiData))
  socket.on('message', (message) => {
    console.log(`received from a client: ${message}`)
  })

  setInterval(() => {
    console.log('sending...')
    uiData.time = Math.random() * 86400
    socket.send(JSON.stringify(uiData))
  }, 200)
})