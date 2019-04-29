import { Component, OnInit } from '@angular/core';
import {ElectronService} from "../../providers/electron.service";
import {SanicService} from "../../providers/sanic.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  classDirs = [];
  training=false;
  constructor(public electronService: ElectronService,public sanic:SanicService) { }
  addClassDir(){
    var {dialog} = this.electronService.remote;
    var path = dialog.showOpenDialog({
      properties:["openDirectory"]
    })
    this.classDirs.push(...path)
  }
  train(){
    this.training=true;
    let ws = this.sanic.connect();
    ws.on('open', ()=> {
      ws.send(JSON.stringify(this.classDirs));
    });

    ws.on('message', (data) => {
      console.log(data);
    });
    // console.log()
    //   .then(res=>{
    //   alert(res)
    // });

  }
  ngOnInit() {
  }

}
