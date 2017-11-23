import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.scss']
})
export class CheckComponent implements OnInit {

  check = false;
  currentC: any;
  checkedin: boolean;
  checkedout: boolean;

  constructor(private server: ServerProvider) { }

  ngOnInit() {

  }

  async checkIn() {
    this.check = await this.server.checkIn();
    console.log(`check: ${this.check}`);
    this.currentC = this.server.getUser();
    if (this.currentC.checkin) {
      this.checkedin = true;
    }
  }

  async checkOut() {
    this.check = await this.server.checkOut();
    console.log(`check: ${this.check}`);
    this.currentC = this.server.getUser();
    if (this.currentC.checkout) {
      this.checkedout = true;
    }
  }

}
