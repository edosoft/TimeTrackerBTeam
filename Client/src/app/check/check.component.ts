import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.css']
})
export class CheckComponent implements OnInit {

  check = false;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
  }

  checkIn() {
    this.check = true;
    this.server.checkIn();
  }

  checkOut() {
    this.check = false;
    this.server.checkOut();
  }

}
