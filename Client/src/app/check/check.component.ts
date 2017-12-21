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

  currentUserWorkday: any;
  checkInTime: string;
  checkOutTime: string;
  date: string;

  checkInClock: any;
  checkInHour: any;
  checkInMinutes: any;
  checkInSoon = false;
  checkInLate = false;

  checkOutHour: number;
  checkOutSoon: boolean;
  currentHour: any;
  currentMinutes: any;
  checkInOutofRange: boolean;

  /* Variables for dailyWorkedTime function */

  checkIndone = false;
  checkOutdone = false;
  currentTime: any;
  currentTimeMinutes: any;
  currentTimeHour: any;
  timeCheckIn: any;
  timecheckInHour: any;
  timecheckInMinutes: any;
  timeCheckOut: any;
  timecheckOutHour: any;
  timecheckOutMinutes: any;
  dailytotalTimeMinutes: any;
  dailytotaltime: any;
  dailyWorkedTimeHour: any;
  dailyWorkedTimeMinutes: any;
  timer: any = null;

  /* END Variables for dailyWorkedTime function */

  constructor(private server: ServerProvider, private datePipe: DatePipe) { }

  ngOnInit() {
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
    this.currentUserWorkday = this.server.getUserWorkday();
    console.log("usuario: " + this.server.getUserWorkday().id);
    this.currentHour = +(this.datePipe.transform(new Date(), 'HH'));
    this.currentMinutes = +(this.datePipe.transform(new Date(), 'mm'));

    if (this.currentHour <= 7 && this.currentMinutes < 30 || (this.currentHour >= 19)) {
      this.checkInOutofRange = true;
    }

    if (this.currentUserWorkday === undefined) {
      this.checkInTime = 'None';
    } else {
      this.checkInTime = this.currentUserWorkday.checkin;
    }

    if (this.currentUserWorkday === undefined) {
      this.checkOutTime = 'None';
    } else {
      this.checkOutTime = this.currentUserWorkday.checkout;
    }
    if (this.checkInTime != 'None') {
      this.checkIndone = true;
      if (this.checkOutTime == 'None') {
        this.timer = setInterval(this.dailyWorkedTime.bind(this), 60 * 1000);
        this.dailytotaltime = this.dailyWorkedTime();
      } else {
        clearInterval(this.timer);
        this.checkOutdone = true;
        this.dailytotaltime = this.dailyWorkedTime();
      }
    }

  }

  async checkIn() {
    await this.server.checkIn();
    this.checkIndone = true;
    this.checkInTime = this.server.getUserWorkday().checkin;
    this.checkInClock = (this.checkInTime).split(':', 2);
    this.checkInHour = +this.checkInClock[0];
    this.checkInMinutes = +this.checkInClock[1];

    if (this.checkInHour <= 7 && this.checkInMinutes < 30) {
      this.checkInSoon = true;
    } else {
      if (this.checkInHour >= 9) {
        this.checkInLate = true;
      }
    }
    this.dailytotaltime = '00:00';
    this.timer = setInterval(this.dailyWorkedTime.bind(this), 60 * 1000);
  }

  async checkOut() {
    await this.server.checkOut();
    this.checkOutdone = true;
    this.checkOutTime = this.server.getUserWorkday().checkout;
    // Coge las cifras de horas y las convierte en numero
    this.checkOutHour = +this.checkOutTime.split(':', 1).join();

    if (this.checkOutHour < 14) {
      this.checkOutSoon = true;
    }
    clearInterval(this.timer);
    this.dailyWorkedTime();
  }

  async getWeekTotal() {
    await this.server.getWeekTotal();
  }

  closeIn() {
    this.checkInLate = false;
    this.checkInSoon = false;
  }

  closeOut() {
    this.checkOutSoon = false;
  }


  dailyWorkedTime() {

    /**
     * Calculate the daily time worked when has done check in and check out.
     */

    this.timeCheckIn = this.server.getUserWorkday().checkin;
    this.timeCheckIn = this.timeCheckIn.split(':');
    this.timecheckInHour = parseInt(this.timeCheckIn[0], 10);
    this.timecheckInMinutes = parseInt(this.timeCheckIn[1], 10);

    if ((this.checkIndone == true) && (this.checkOutdone == false)) {

      this.currentTimeHour = new Date().getHours();
      this.currentTimeMinutes = new Date().getMinutes();

      this.currentTime = (this.currentTimeHour * 60) + this.currentTimeMinutes;
      this.timeCheckIn = (this.timecheckInHour * 60) + this.timecheckInMinutes;

      this.dailytotalTimeMinutes = this.currentTime - this.timeCheckIn;

      this.dailyWorkedTimeMinutes = this.dailytotalTimeMinutes % 60;
      this.dailyWorkedTimeHour = (this.dailytotalTimeMinutes - this.dailyWorkedTimeMinutes) / 60;

      if (this.dailyWorkedTimeHour < 10) {
        this.dailyWorkedTimeHour = '0' + this.dailyWorkedTimeHour;
      }

      if (this.dailyWorkedTimeMinutes < 10) {
        this.dailyWorkedTimeMinutes = '0' + this.dailyWorkedTimeMinutes;
      }

      this.dailytotaltime = this.dailyWorkedTimeHour + ':' + this.dailyWorkedTimeMinutes;

    } else if ((this.checkIndone == true) && (this.checkOutdone == true)) {

      this.timeCheckOut = this.server.getUserWorkday().checkout;
      this.timeCheckOut = this.timeCheckOut.split(':');
      this.timecheckOutHour = parseInt(this.timeCheckOut[0], 10);
      this.timecheckOutMinutes = parseInt(this.timeCheckOut[1], 10);

      this.timeCheckIn = (this.timecheckInHour * 60) + this.timecheckInMinutes;
      this.timeCheckOut = (this.timecheckOutHour * 60) + this.timecheckOutMinutes;

      this.dailytotalTimeMinutes = this.timeCheckOut - this.timeCheckIn;

      this.dailyWorkedTimeMinutes = this.dailytotalTimeMinutes % 60;
      this.dailyWorkedTimeHour = (this.dailytotalTimeMinutes - this.dailyWorkedTimeMinutes) / 60;

      if (this.dailyWorkedTimeHour < 10) {
        this.dailyWorkedTimeHour = '0' + this.dailyWorkedTimeHour;
      }

      if (this.dailyWorkedTimeMinutes < 10) {
        this.dailyWorkedTimeMinutes = '0' + this.dailyWorkedTimeMinutes;
      }

      this.dailytotaltime = this.dailyWorkedTimeHour + ':' + this.dailyWorkedTimeMinutes;

    }

    return this.dailytotaltime;

  }


}
