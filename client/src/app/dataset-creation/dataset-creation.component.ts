import { Component, OnInit } from '@angular/core';
@Component({
  selector: 'app-dataset-creation',
  templateUrl: './dataset-creation.component.html',
  styleUrls: ['./dataset-creation.component.scss']
})
export class DatasetCreationComponent implements OnInit {

  constructor() { }
  classes = {};
  classList = Object.keys(this.classes);
  addClassModal = false;
  setClass(newModalName){
    this.classes[newModalName.value] = []
    this.updateClassList()
  }
  updateClassList(){
    this.classList = Object.keys(this.classes);
  }
  removeClass(className){
    if(confirm("Are You sure you would like to delete this class and all its images?")){
      delete this.classes[className];
      this.updateClassList()
    }
  }
  toggleAddClassModal($event){
    this.addClassModal =!this.addClassModal
  }
  handleFiles(event){
    debugger
  }
  ngOnInit() {
  }


}
