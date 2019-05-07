import { Component, OnInit } from '@angular/core';
import {ElectronService} from '../../providers/electron.service';
import {SanicService} from '../../providers/sanic.service';
import {AppEvent, EventSubjects} from '../../providers/EventSubjects';
import { Subject } from 'rxjs';
const { mergeMap, tap }  = window.require('rxjs/operators');

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  classesDir: string;
  training = false;
  componetSubjects = {};
  dataSetCreated = false;
  train_1st_stage = false;
  UIEvents = new EventSubjects();
  photoUrl: string;
  photoSrc: string;
  train_ops = {};
  photo_predictions;
  ws;
  constructor(public electronService: ElectronService, public sanic: SanicService) { }
  addClassDir() {
    const {dialog} = this.electronService.remote;
    const path = dialog.showOpenDialog({
      properties: ['openDirectory']
    });
    this.classesDir  = path[0];
    this.UIEvents.emitEvent(new AppEvent('classDirChange', path[0]));
  }
  predictOnePhoto() {
    const {dialog} = this.electronService.remote;
    const path = dialog.showOpenDialog({
      properties: ['openFile']
    });
    const fs = this.electronService.remote.require('fs');
    const _img = fs.readFileSync(path[0]).toString('base64');
    this.photoSrc = 'data:image/png;base64,' + _img;

    this.photoUrl = path[0];
    this.UIEvents.emitEvent(new AppEvent('predict_one', this.photoUrl));
  }
  train_1() {
    this.training = true;
    this.UIEvents.emitEvent(new AppEvent('train_stage_1', 'train_stage_1'));

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
    this.UIEvents.getSubject('classDirChange').pipe(
      mergeMap((folder: string) => {
        this.sanic.sendEvent(new AppEvent('dataset_folder', folder));
        return this.sanic.getSubject('dataset_created');
      }),
      mergeMap(() => {
        this.dataSetCreated = true;
        return this.UIEvents.getSubject('train_stage_1');
      }),
      mergeMap(() => {
        this.sanic.sendEvent(new AppEvent('train_stage_1', this.train_ops));
        return this.sanic.getSubject('train_stage_1');
      }),
      tap(() => {
        this.train_1st_stage = true;
      }),
      mergeMap(() => {
        return this.UIEvents.getSubject('predict_one');
      }),
      mergeMap((photo_url) => {
        this.sanic.sendEvent(new AppEvent('predict_one' , photo_url));
        return this.sanic.getSubject('photo_predictions');
      }),
      tap((predictions => {
        this.photo_predictions = predictions;
      }))
    ).subscribe(data => {
      console.log(data);
      alert(data);
    });

  }
  ngOnInit() {
    this.initPipeLine();
  }

}
