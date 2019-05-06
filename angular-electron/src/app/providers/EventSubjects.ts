import { Injectable } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import {map, filter} from 'rxjs/operators';
import {webSocket} from 'rxjs/webSocket';
export class AppEvent {
  constructor(event_type: string, data: any) {
    this.event_type = event_type;
    this.data = data;
  }
  event_type: string;
  data: any;
}
export class EventSubjects {
  eventSubjects = {};
  constructor() { }
  createIfNotExist(event_type) {
    if (!(event_type in this.eventSubjects)) {
      this.eventSubjects[event_type] = new Subject();
    }
  }
  emitEvent(event: AppEvent) {
    this.createIfNotExist(event.event_type);
    this.eventSubjects[event['event_type']]   .next(event['data']);
  }
  getSubject(event_type) {
    this.createIfNotExist(event_type);
    return this.eventSubjects[event_type];
  }

}
