import { Injectable } from '@angular/core';

const WebSocket = require('ws');



@Injectable()
export class SanicService {

  constructor() { }
  connect(){
    const ws = new WebSocket('ws://localhost:8000/train');
    return ws

  }
}
