import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dataset-creation',
  templateUrl: './dataset-creation.component.html',
  styleUrls: ['./dataset-creation.component.scss']
})
export class DatasetCreationComponent implements OnInit {

  constructor() { }
  classes = {};
  addClassModal = false;
  setClass(newModalName){
    this.classes[newModalName.value] = []
  }
  toggleAddClassModal($event){
    this.addClassModal =!this.addClassModal
  }
  ngOnInit() {
  }


}
