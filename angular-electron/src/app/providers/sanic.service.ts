import { Injectable } from '@angular/core';

const WebSocket = window.require('ws');



@Injectable()
export class SanicService {

  constructor() { }
  connect(){
    const ws = new WebSocket('ws://localhost:8000/train');
    return ws

  }
}
