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
  remainingDayGeneral: number;
  friday: boolean;
  totalHoursPerDay: number;

  forgetcheckin: boolean = false;

  constructor(private server: ServerProvider, private datePipe: DatePipe) {
  }

  ngOnInit() {
    console.log('Check onInit');
    this.date = this.datePipe.transform(new Date(), 'EEEE, MMMM d, y');
    this.currentUserWorkday = this.server.getUserWorkday();
    this.currentHour = +(this.datePipe.transform(new Date(), 'HH'));
    this.currentMinutes = +(this.datePipe.transform(new Date(), 'mm'));

    if (this.currentHour <= 7 && this.currentMinutes < 30 || (this.currentHour >= 19)) {
      this.checkInOutofRange = true;
    }

    if (this.currentUserWorkday == undefined) {
      this.checkInTime = 'None';
    } else {
      this.checkInTime = this.currentUserWorkday.checkin;
    }

    if (this.currentUserWorkday == undefined) {
      this.checkOutTime = 'None';
    } else {
      this.checkOutTime = this.currentUserWorkday.checkout;
    }

    this.checkActiveLogic();
    this.timer();
    this.sendNotifyCheckIn();

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
    this.weeklyLimitHigher(weekly_hours); // Llamada a las notificaciones de limite semanal
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
      this.timer();
    } else {
      this.checkWait = true;
    }
    const weekly_hours = await this.server.getWeekTotal();
    this.weeklyLimitFewer(weekly_hours); // Llamada a las notificaciones de limite semanal
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
        const whours = (wtimer.getHours() + Math.floor(weekly_hours / 1440) * 24);
        const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();

        this.whours = (whours < 10 ? '0' : '') + whours;
        this.wminutes = wminutes;
        // console.log(hours + ':' + minutes + ':' + seconds);
      }, 1000);

    } else if (this.server.getUserWorkday().checkin_number != 0 &&
      this.server.getUserWorkday().checkin_number ==
      this.server.getUserWorkday().checkout_number) {
      const timer = new Date(this.server.getUserWorkday().total * 60 * 1000);
      const hours = (timer.getHours() < 10 ? '0' : '') + timer.getHours();
      const minutes = (timer.getMinutes() < 10 ? '0' : '') + timer.getMinutes();
      this.hours = hours;
      this.minutes = minutes;

      const weekly_hours = await this.server.getWeekTotal();
      const wtimer = new Date(weekly_hours * 60 * 1000);
      const whours = (wtimer.getHours() + Math.floor(weekly_hours / 1440) * 24);
      const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();

      this.whours = (whours < 10 ? '0' : '') + whours;
      this.wminutes = wminutes;
      clearInterval(this.timerInterval);

    } else { // No se ha hecho checkin todavía
      this.hours = '00';
      this.minutes = '00';

      const weekly_hours = await this.server.getWeekTotal();
      const wtimer = new Date(weekly_hours * 60 * 1000);
      const whours = (wtimer.getHours() + Math.floor(weekly_hours / 1440) * 24);
      const wminutes = (wtimer.getMinutes() < 10 ? '0' : '') + wtimer.getMinutes();

      this.whours = (whours < 10 ? '0' : '') + whours;
      this.wminutes = wminutes;
    }

  }

  getRemainingDay() {
    const today = new Date(this.currentUserWorkday.date);
    const dayWeek = today.getDay();
    if (dayWeek === 5) {
      this.friday = true;
    }
    this.remainingDayGeneral = 5 - dayWeek;
    return this.remainingDayGeneral;
  }

  weeklyLimitHigher(weeklyTotalHours) {
    const remainingDay = this.getRemainingDay();
    this.totalHoursPerDay = this.server.getUserWorkday().total;
    if (this.totalHoursPerDay < 5) {
      if (this.friday === false) {
        if (((weeklyTotalHours / 60) + (remainingDay * 5) + (5 - this.totalHoursPerDay)) >= 40) {
          this.higherHours = true;
        } else {
          this.higherHours = false;
        }
      } else {
        if (((weeklyTotalHours / 60) + (remainingDay * 5) + this.totalHoursPerDay) >= 40) {
          this.higherHours = true;
        } else {
          this.higherHours = false;
        }
      }
    } else {
      if (((weeklyTotalHours / 60) + (remainingDay * 5)) >= 40) {
        this.higherHours = true;
      } else {
        this.higherHours = false;
      }
    }
  }

  weeklyLimitFewer(weeklyTotalHours) {
    const remainingDay = this.getRemainingDay();
    this.totalHoursPerDay = this.server.getUserWorkday().total;
    if (this.friday === false) {
      if ((weeklyTotalHours / 60) + ((remainingDay - 1) * 10.5) + (10.5 - this.totalHoursPerDay) + 7.5 < 40) {
        this.fewerHours = true;
      } else {
        this.fewerHours = false;
      }
    } else {
      if ((weeklyTotalHours / 60) + (7.5 - this.totalHoursPerDay) < 40) {
        this.fewerHours = true;
      } else {
        this.fewerHours = false;
      }
    }
  }

  closeLimitHour() {
    this.fewerHours = false;
    this.higherHours = false;
  }

  sendNotifyCheckIn() {
    // Send Notification when has forgot to do checkin after 09:00
    this.currentHour = +(this.datePipe.transform(new Date(), 'HH'));
    this.currentMinutes = +(this.datePipe.transform(new Date(), 'mm'));
    if ((this.currentHour >= 9) && (this.currentMinutes >= 1)) {
      if (this.server.getUserWorkday().checkin_number == 0){
        this.forgetcheckin = true;
      }
    }
  }

  closeCheckInNotify() {
    this.forgetcheckin = !this.forgetcheckin;
  }

}
