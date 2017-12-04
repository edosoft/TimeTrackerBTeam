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

  constructor(private server: ServerProvider, private datePipe: DatePipe) {}

  ngOnInit() {
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
    this.currentUserWorkday = this.server.getUserWorkday();
    this.currentHour = +(this.datePipe.transform(new Date(), 'HH'));
    this.currentMinutes = +(this.datePipe.transform(new Date(), 'mm'));

    if (this.currentHour <= 7 && this.currentMinutes < 30 || (this.currentHour >= 19)) {
      this.checkInOutofRange = true;
    }

    this.checkInTime = this.currentUserWorkday.checkin;
    this.checkOutTime = this.currentUserWorkday.checkout;
  }

  async checkIn() {
    await this.server.checkIn();

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
    await this.server.checkOut();

    this.checkOutTime = this.server.getUserWorkday().checkout;
    // Coge las cifras de horas y las convierte en numero
    this.checkOutHour = +this.checkOutTime.split(':', 1).join();

    if (this.checkOutHour < 14) {
      this.checkOutSoon = true;
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

  weeklyReport() {
    this.server.report('No');
  }

  monthlyReport() {
    this.server.report('True');
  }
}
