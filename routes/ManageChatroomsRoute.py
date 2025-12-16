from fastapi import APIRouter , Depends, status ,HTTPException
#from fastapi.exceptions  import HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from DBConnection import SessionDep
from model import ChatRoom , JoinId ,ChatMessage
from DBConnection import *
from typing import Annotated
from datetime import UTC, datetime
from generate_joinId import generate_joinId
from SocketManager import SocketManager
router = APIRouter()

#Sessiondep=Annotated[Session,Depends(get_session)]
manager=SocketManager()
@router.post("/check_chatroom/{join_id}", response_model=None)
async def check_chatroom(join_id: str, session:SessionDep) :
      #first we shall check it the id exists in the database
      # If it exists, allow the user to enter the chat room
      checkID= session.exec(select(ChatRoom).where(ChatRoom.join_id==join_id)).first()
      if not checkID:
            raise HTTPException(
                  status_code=status.HTTP_404_NOT_FOUND,
                  detail="Chat room not found"
            )
      #frontend will handle the actual entering of the chat room using websockets 
      #if it receives a 200 OK response from this endpoint
      return HTTPException(status_code=status.HTTP_200_OK, headers={"message":"Entered chat room successfully"})


#now that the user  has enetered the chat room we gotta handle the websocket connections in SocketEndpoint.py

#but first we shall also show or open up the chatroom page from here itself

@router.get("/fetch_chatroom/{join_id}")
async def fetch_chatroom(join_id:str ,session:SessionDep):
      #now we gotta throw the excat chatroom the user is trying to access
      #honestly  i dont to know how to do that like do i need to fetch only or use the websocket connection also here
      #for now lets just try it
      #ChatRoomData=await session.exec(select(ChatRoom).where(join_id.join_id==ChatRoom.join_id)).all()
      '''i think using sql is useless here cuase here we just nee to open the connection right and throw the ouput 
      stating that socket is open and running so no need for uncessary db calls
      db calls are needed when we either want to check if the chatroom exist ,create it or delete it but here its just opening the connection
      '''
      manager.connect(join_id.join_id)

@router.post("/send_message/{join_id}")
async def send_messages(join_id:str,message: ChatMessage):
      try:
            await manager.broadcast(join_id.join_id,message.message)
      except Exception as e:
            await manager.disconnect(join_id.join_id)
            raise HTTPException(
                  status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  detail=f"Error broadcasting message: {e}"
            )
      return HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Message broadcasted successfully"
      )
@router.post("/create_chatroom/")
async def create_chatroom(deatils:ChatRoom ,session:SessionDep) -> JSONResponse:
      new_chatroom=ChatRoom(
            join_id=generate_joinId(),
            created_at=datetime.now(UTC),
            is_active=True
      )
      session.add(new_chatroom)
      session.commit()
      session.refresh(new_chatroom)
      return JSONResponse(content={
            "join_id":new_chatroom.join_id
      },status_code=status.HTTP_201_CREATED
      , 
      
      headers={"message":"chat room live"}
      
      )