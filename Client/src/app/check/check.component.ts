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
  checkedIn: string;
  checkedOut: string;
  date: string;
  dateCheckin: any;
  checkHour: any;
  checkMins: any;
  soonCheckin= false;
  lateCheckin = false;
  dateCheck: string;
  dateCheckInt: number;
  checkOutMin: boolean;
  actualHour: any;
  checkinOutofRange: boolean;
  actualMinute: any;

  constructor(private server: ServerProvider, private datePipe: DatePipe) {
  }
  ngOnInit() {
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
    this.currentUser = this.server.getUser();
    this.actualHour = +(this.datePipe.transform(new Date(), 'HH'));
    this.actualMinute = +(this.datePipe.transform(new Date(), 'mm'));
    console.log(this.actualHour, this.actualMinute);
    if (this.actualHour <= 7 && this.actualMinute < 30 || (this.actualHour >= 19)) {
      this.checkinOutofRange = true;
    }
    this.checkedIn = this.server.getUser().checkin;
    this.checkedOut = this.server.getUser().checkout;
  }

  async checkIn() {
    this.check = await this.server.checkIn();
    console.log(`check: ${this.check}`);
    this.checkedIn = this.server.getUser().checkin;
    this.dateCheckin = (this.checkedIn).split(':', 2);
    this.checkHour = +this.dateCheckin[0];
    this.checkMins = +this.dateCheckin[1];
    if (this.checkHour <= 7 && this.checkMins < 30) {
      this.soonCheckin = true;
    } else {
      if (this.checkHour >= 10) {
        this.lateCheckin = true;
      }
    }
  }

  async checkOut() {
    this.check = await this.server.checkOut();
    this.checkedOut = this.server.getUser().checkout;
    this.dateCheckInt = +this.checkedOut.split(':', 1).join(); // Coge las cifras de horas y las convierte en numero
    if (this.dateCheckInt < 14) {
      this.checkOutMin = true;
    }
  }
  closeIn() {
    this.lateCheckin = false;
    this.soonCheckin = false;
  }
  closeOut() {
    this.checkOutMin = false;
  }
  weeklyReport(){
    this.server.report("No");
  }

  monthlyReport(){
    this.server.report("True");
  }
}
