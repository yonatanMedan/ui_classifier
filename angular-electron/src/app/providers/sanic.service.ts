import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
// import {  } from 'rxjs/operators';
// (global as any).WebSocket = require('ws');

import {map,filter} from 'rxjs/operators';
import {webSocket} from 'rxjs/webSocket';
export class WSEvent {
  constructor(event_type: string, data: any) {
    this.event_type = event_type;
    this.data = data;
  }
  event_type: string;
  data: any;
}
@Injectable()
export class SanicService {
  eventSubjects = {};
  constructor() {
    this.ws = webSocket('ws://localhost:8000/train');
    this.ws.subscribe((event: WSEvent) => {
      this.emitEvent(event);
    }, error => {
      console.log(error);
    });
  }
  ws;
  parseEvent(event: string) {
    return JSON.parse(event);
  }
  createIfNotExist(event_type) {
    if (!(event_type in this.eventSubjects)) {
      this.eventSubjects[event_type] = new Subject();
    }
  }
  emitEvent(event: WSEvent) {
    this.createIfNotExist(event.event_type);
    this.eventSubjects[event['event_type']]   .next(event['data']);
  }
  getSubject(event_type) {
    this.createIfNotExist(event_type);
    return this.eventSubjects[event_type];
  }
  sendEvent(event: WSEvent) {
    this.ws.next(event);
  }

}
