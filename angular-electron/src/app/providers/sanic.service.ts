import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
// import {  } from 'rxjs/operators';
// (global as any).WebSocket = require('ws');

import {map,filter} from 'rxjs/operators';
import {webSocket} from 'rxjs/webSocket';
import {AppEvent, EventSubjects} from "./EventSubjects"

@Injectable()
export class SanicService extends EventSubjects {
  eventSubjects = {};
  constructor() {
    super();
    this.ws = webSocket('ws://localhost:8000/train');
    this.ws.subscribe((event: AppEvent) => {
      this.emitEvent(event);
    }, error => {
      console.log(error);
    });
  }
  ws;
  parseEvent(event: string) {
    return JSON.parse(event);
  }
  sendEvent(event: AppEvent) {
    this.ws.next(event);
  }

}
