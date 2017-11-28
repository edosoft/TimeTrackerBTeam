import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.scss']
})
export class CheckComponent implements OnInit {

  check = false;
  currentUser: any;
  checkedIn: boolean;
  checkedOut: boolean;

  constructor(private server: ServerProvider) { }

  ngOnInit() {

  }

  async checkIn() {
    this.check = await this.server.checkIn();
    console.log(`check: ${this.check}`);
    this.currentUser = this.server.getUser();
    if (this.currentUser.checkin) {
      this.checkedIn = true;
    }
  }

  async checkOut() {
    this.check = await this.server.checkOut();
    console.log(`check: ${this.check}`);
    this.currentUser = this.server.getUser();
    if (this.currentUser.checkout) {
      this.checkedOut = true;
    }
  }

}
