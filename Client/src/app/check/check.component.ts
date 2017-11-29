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
  dateCheckin: any;
  checkHour: any;
  checkMins: any;
  soonCheckin= false;
  lateCheckin = false;
  dateCheck: string;
  dateCheckInt: number;
  checkOutMin: boolean;

  constructor(private server: ServerProvider, private datePipe: DatePipe) {
  }
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
    this.dateCheckin = (this.server.getUser().checkin).split(':', 2);
    this.checkHour = +this.dateCheckin[0];
    this.checkMins = +this.dateCheckin[1];
    if (this.checkHour <= 7 && this.checkMins < 30) {
      this.soonCheckin = true;
    } else {
      if (this.checkHour > 9 && this.checkMins > 0) {
        this.lateCheckin = true;
      }
    }
  }

  async checkOut() {
    this.check = await this.server.checkOut();
    console.log(`check: ${this.check}`);
    this.currentUser = this.server.getUser();
    if (this.currentUser.checkout) {
      this.checkedOut = true;
    }
    this.dateCheck = this.server.getUser().checkout;
    console.log(`check: ${this.dateCheck}`);
    this.dateCheckInt = +this.dateCheck.split(":", 1).join(); //Coge las cifras de horas y las convierte en numero
    console.log(`checkInt: ${this.dateCheckInt}`);
    if(this.dateCheckInt < 15){
      this.checkOutMin = true;
    }
  }
  close() {
    this.lateCheckin = false;
    this.soonCheckin = false;
    this.checkOutMin=false;
  }
}
