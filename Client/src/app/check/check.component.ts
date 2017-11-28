import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { Pipe, PipeTransform } from '@angular/core';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-check',
  templateUrl: './check.component.html',
  styleUrls: ['./check.component.scss'],
  providers: [DatePipe]
})
export class CheckComponent implements OnInit {

  check = false;
  currentUser: any;
  checkedIn: boolean;
  checkedOut: boolean;
  date: string;

  constructor(private server: ServerProvider, private datePipe: DatePipe) { }

  ngOnInit() {
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
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
