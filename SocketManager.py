from fastapi import FastAPI , WebSocket,Depends
from typing import List, Annotated, Optional
#from model import JoinId
from collections import defaultdict
#import websockets
 
class SocketManager:
    #constructor for the class
    #keeping track of active connections
    def __init__(self):
        self.active_connections: Annotated[dict,dict[str,set[WebSocket]]]=defaultdict(set)
        #self.join_ids: dict[WebSocket]=None
    async def connect(self,websocket:Annotated[WebSocket, Optional],join_id:Annotated[str,Optional]=None):
        try:
           await websocket.accept()
           if join_id:
               self.active_connections[join_id].add(websocket)
        except Exception :
            await websocket.close()
    async def send_message(self, message: Annotated[str,Optional], websocket: Annotated[WebSocket, Optional]):
        '''sending the text message to a specific client'''
        await websocket.send_text(message)
    
    async def broadcast(self, join_id: Annotated[str,Optional] ,message: Annotated[str,Optional]):
        '''broadcast message to all connected clients to thwe specific join_id'''
        coonections=list(self.active_connections[join_id])
        for connection in coonections:
            try:
               await connection.send_text(message)
            except Exception as e:
               await self.disconnect(join_id,connection) 
    
    async def disconnect(self, join_id:Annotated[str,Optional],websocket: Annotated[WebSocket, Optional]):
        self.active_connections[join_id].discard(websocket)
        #well we dont want to keep any residue connections
        if not  self.active_connections[join_id]:
            del self.active_connections[join_id]
        await websocket.close()



