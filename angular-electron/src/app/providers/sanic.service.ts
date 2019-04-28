import { Injectable } from '@angular/core';
let request = require('request-promise')
@Injectable()
export class SanicService {

  constructor() { }
  train(directories){
    console.log(directories)
    return request.get("http://localhost:8000/")
  }
}
