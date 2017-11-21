import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css']
})
export class CheckComponent implements OnInit {

  check = false;

  constructor() { }

  ngOnInit() {
  }

  checkIn() {
    this.check = true;
  }

  checkOut() {
    this.check = false;
  }

}
