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

  timerInterval: any;
  hours: string;
  minutes: string;

  whours: string;
  wminutes: string;

  fewerHours: boolean;
  higherHours: boolean;

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
    this.timer();
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
    this.timer();
    const weekly_hours = await this.server.getWeekTotal();
    this.weeklyLimit(weekly_hours); //Llamada a las notificaciones de limite semanal
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
      this.checkWait = true;
    }
    this.timer();
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

  getProperDate(check): Date {
    const date = new Date();
    const hour = check.split(':', 2)[0];
    const min = check.split(':', 2)[1];
    date.setMinutes(min);
    date.setHours(hour);
    return date;
  }

  async timer() {
    if (this.server.getUserWorkday().checkin_number != 0 &&
      this.server.getUserWorkday().checkin_number !=
      this.server.getUserWorkday().checkout_number) {
      // const server_time = this.server.getCurrentTime();
      if (this.timerInterval == undefined) {
        const server_time = new Date();
        const timeServer = new Date(server_time);
        const timeCheckIn = this.getProperDate(this.server.getUserWorkday().checkin);

        const timer = new Date(timeServer.getTime() - timeCheckIn.getTime() + this.server.getUserWorkday().total * 60 * 1000);

        const weekly_hours = await this.server.getWeekTotal();
        const wtimer = new Date(timeServer.getTime() - timeCheckIn.getTime()
          + weekly_hours * 60 * 1000);

        this.timerInterval = setInterval(() => {
          timer.setSeconds(timer.getSeconds() + 1);
          const hours = (timer.getHours() < 10 ? '0' : '') + timer.getHours();
          const minutes = (timer.getMinutes() < 10 ? '0' : '') + timer.getMinutes();
          const seconds = (timer.getSeconds() < 10 ? '0' : '') + timer.getSeconds();
          this.hours = hours;
          this.minutes = minutes;

          wtimer.setSeconds(wtimer.getSeconds() + 1);
          const whours = (wtimer.getHours() < 10 ? '0' : '') + wtimer.getHours();
          const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();
          const wseconds = (wtimer.getSeconds() < 10 ? '0' : '') + wtimer.getSeconds();


          this.whours = (parseInt(whours, 10) + Math.floor(weekly_hours / 1440) * 24).toString();
          this.wminutes = wminutes;
          // console.log(hours + ':' + minutes + ':' + seconds);
        }, 1000);
      }
    } else if (this.server.getUserWorkday().checkin_number != 0 &&
      this.server.getUserWorkday().checkin_number ==
      this.server.getUserWorkday().checkout_number) {
      const timer = new Date(this.server.getUserWorkday().total * 60 * 1000);
      const hours = (timer.getHours() < 10 ? '0' : '') + timer.getHours();
      const minutes = (timer.getMinutes() < 10 ? '0' : '') + timer.getMinutes();
      this.hours = hours;
      this.minutes = minutes;
      console.log(timer);

      const weekly_hours = await this.server.getWeekTotal();
      const wtimer = new Date(weekly_hours * 60 * 1000);
      const whours = (wtimer.getHours() < 10 ? '0' : '') + wtimer.getHours();
      const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();
      this.whours = (parseInt(whours, 10) + Math.floor(weekly_hours / 1440) * 24).toString();
      this.wminutes = wminutes;
      console.log(wtimer);
      clearInterval(this.timerInterval);

      this.weeklyLimit(weekly_hours); //Llamada a las notificaciones de limite semanal

    } else { // No se ha hecho checkin todavía
      this.hours = '00';
      this.minutes = '00';

      const weekly_hours = await this.server.getWeekTotal();
      const wtimer = new Date(weekly_hours * 60 * 1000);
      const whours = (wtimer.getHours() < 10 ? '0' : '') + wtimer.getHours();
      const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();
      this.whours = (parseInt(whours, 10) + Math.floor(weekly_hours / 1440) * 24).toString();
      this.wminutes = wminutes;
    }

  }

  weeklyLimit(weeklyTotalHours) {
    const today = new Date(this.currentUserWorkday.date);
    const dayWeek = today.getDay();
    console.log("Dia de la semana: " + dayWeek);
    const remainingDay = 5 - dayWeek;
    console.log("Remaining Day: " + remainingDay);
    if ((weeklyTotalHours / 60) + ((remainingDay - 1) * 10.5) + 7.5 < 40) {
      this.fewerHours = true;
      console.log("No has alcanzado el limite");
    } else {
      this.fewerHours = false;
      console.log("Has alcanzado el limite");
    }
    if ((weeklyTotalHours / 60) + ((remainingDay - 1) * 5) + 5 >= 40) {
      this.higherHours = true;
      console.log("Te has pasado");
    } else {
      this.higherHours = false;
      console.log("No te has pasado");
    }
  }

  closeLimitHour() {
    this.fewerHours = false;
    this.higherHours = false;
  }


}
