import { Component, OnInit } from '@angular/core';
import {ElectronService} from '../../providers/electron.service';
import {SanicService, WSEvent} from '../../providers/sanic.service';
import { Subject } from 'rxjs';
const { mergeMap }  = window.require('rxjs/operators');

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  classesDir: string;
  training = false;
  classDirChangeSubject = new Subject();
  datasetCreatedDataSet = new Subject();
  ws;
  constructor(public electronService: ElectronService, public sanic: SanicService) { }
  addClassDir() {
    let {dialog} = this.electronService.remote;
    let path = dialog.showOpenDialog({
      properties: ['openDirectory']
    });
    this.classesDir  = path[0];
    this.classDirChangeSubject.next(path[0]);
  }
  train() {
    this.training = true;


  }
  // connect(){
  //   this. ws = this.sanic.connect();
  //   return new Promise((resolve, reject) => {
  //     this.ws.on('open', () => {
  //       resolve();
  //     });
  //   });
  // }
  initPipeLine() {
    this.classDirChangeSubject.pipe(
      mergeMap((folder: string) => {
        this.sanic.sendEvent(new WSEvent('dataset_folder', folder));
        return this.sanic.getSubject('dataset_created');
      })
    ).subscribe(event => {
      console.log(event);
      alert(event);
    });

  }
  ngOnInit() {
    this.initPipeLine()
  }

}
