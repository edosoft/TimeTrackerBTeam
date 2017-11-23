import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.scss']
})
export class CheckComponent implements OnInit {

  check = false;

  constructor(private server: ServerProvider) { }

  ngOnInit() {

  }

  checkIn() {
    this.server.checkIn().then((check) => this.check = check).then(() => console.log(`check: ${this.check}`));
  }

  checkOut() {
    this.server.checkOut().then((check) => this.check = check).then(() => console.log(`check: ${this.check}`));
  }

}
