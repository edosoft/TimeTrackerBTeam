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

  checkWait: boolean;
  checkOutHour: number;
  checkOutSoon: boolean;
  currentHour: any;
  currentMinutes: any;
  checkInOutofRange: boolean;

  checkInActive;
  checkOutActive;

  constructor(private server: ServerProvider, private datePipe: DatePipe) { }

  ngOnInit() {
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
    this.currentUserWorkday = this.server.getUserWorkday();
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

    this.checkActiveLogic();

  }


  checkActiveLogic() {
    if ((this.currentUserWorkday.checkin_number == this.currentUserWorkday.checkout_number) &&
      this.currentUserWorkday.checkin_number < 3) {
      this.checkInActive = true;
      this.checkOutActive = false;
    } else if ((this.currentUserWorkday.checkin_number - this.currentUserWorkday.checkout_number) == 1) {
      this.checkInActive = false;
      this.checkOutActive = true;
    } else {
      this.checkInActive = false;
      this.checkOutActive = false;
    }
  }

  async checkIn() {
    await this.server.checkIn();
    // this.checkIndone = true;
    this.checkActiveLogic();
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
  }

  async checkOut() {
    const checkOutOk = await this.server.checkOut();
    if (checkOutOk) {
      this.checkWait = false;
      this.checkActiveLogic();

      this.checkOutTime = this.server.getUserWorkday().checkout;
      // Coge las cifras de horas y las convierte en numero
      this.checkOutHour = +this.checkOutTime.split(':', 1).join();

      if (this.checkOutHour < 14) {
        this.checkOutSoon = true;
      }
    } else {
      if (this.server.getUserWorkday().checkout == 'Wait5') {
        this.checkWait = true;
      }
    }
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

  closeWait() {
    this.checkWait = false;
  }
}
