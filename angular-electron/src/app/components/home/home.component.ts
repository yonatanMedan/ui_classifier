import { Component, OnInit } from '@angular/core';
import {ElectronService} from "../../providers/electron.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  classDirs = [];
  constructor(public electronService: ElectronService) { }
  addClassDir(){
    var {dialog} = this.electronService.remote;
    var path = dialog.showOpenDialog({
      properties:["openDirectory"]
    })
    this.classDirs.push(path)
  }
  train(){

  }
  ngOnInit() {
  }

}
