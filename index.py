import asyncio
import websockets
import json

wss = WebSocketServer({ port: 80 });

wss.on('connection', function connection(ws, req) {
	# get client id
	const id = req.headers['sec-websocket-key'];
	console.log('New client connect:', id);

	ws.on('message', function message(data):
		print('received ' + data)
		ws.send(JSON.stringify(id: id))
