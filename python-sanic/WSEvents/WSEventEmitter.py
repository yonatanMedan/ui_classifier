from rx.subjects import Subject
import json as JSON
import pdb
def parseEvent(event):
  event_dict = JSON.loads(event)
  return event_dict["event_type"],event_dict["data"]

class WSEvent:
  def __init__(self,event_type,data):
    self.event_type =event_type
    self.data = data
  
  def json(self):
    return JSON.dumps(self.__dict__)


class WSEventEmitter:
  def __init__(self,ws):
    self.ws = ws
    self.websocketEvents = Subject()
    self.eventSubjects = {}

  async def send(self,event_type,data=None):
    await self.ws.send(WSEvent(event_type,data).json())

  def emit_event(self,event):
    event_type,data = event
    print("messege recived")
    if event_type not in self.eventSubjects:
      self.eventSubjects[event_type] = Subject()
    self.eventSubjects[event_type].on_next(data)

  def get_subject(self,event_type):
    if event_type not in self.eventSubjects:
      self.eventSubjects[event_type] = Subject()
    return self.eventSubjects[event_type]



  async def start_event_loop(self):
      self.listen()
      while True:
        raw_event = await self.ws.recv()
        print("conecttion recived")
        event = parseEvent(raw_event)

        self.websocketEvents.on_next(event)

  def listen(self):
    self.websocketEvents.subscribe(self.emit_event)

