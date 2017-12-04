import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { User } from '../provider/model';
import { Router } from '@angular/router';

declare const gapi: any;

@Injectable()
export class ServerProvider {

  constructor (private router: Router, private zone: NgZone) {}

  // Para seleccionar la url en local this.L y para trabajar sobre produccion con this.P
  L = 'http://localhost:8080/_ah/api';
  P = 'https://timetrackerbteam.appspot.com/_ah/api/';

  url: string = this.L;

  logged = false;
  reportType: number;
  public auth2: any;

  public userWorkday: User;

  getUserWorkday() {
    return this.userWorkday;
  }

  public googleInit() {
    gapi.load('client:auth2', () => {
      this.auth2 = gapi.auth2.init({
        client_id: '368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com',
        cookiepolicy: 'single_host_origin',
        scope: 'profile email'
      });
      this.attachGSuite(document.getElementById('googleBtn'));
    });
  }

  public callback() {
    console.log('gapi loaded');
  }

  public attachGSuite(element) {
    gapi.client.load('timetrackerApi', 'v1', this.callback, this.url);
    this.auth2.attachClickHandler(element, {},
      (googleUser) => {
        const profile = googleUser.getBasicProfile();

        this.userWorkday = new User();
        this.userWorkday.name = profile.getName();
        this.logIn();
      }, (error) => {
        alert(JSON.stringify(error, undefined, 2));
      });
  }

  // Check that userWorkday exists in datastore
  logIn() {
    gapi.client.timetrackerApi.login().execute((response: any) => {
      if (response.result.response_code === '400') {
        window.alert(response.result.text);
      } else {
        this.userWorkday.date = response.result.date;
        this.userWorkday.checkin = this.returnDate(response.result.checkin);
        this.userWorkday.checkout = this.returnDate(response.result.checkout);
        this.userWorkday.id = response.result.employeeid;
        this.userWorkday.total = response.result.total;
        this.logged = true;

        this.zone.run(() => {
          this.router.navigate(['/check']);
        });
      }
    });

  }

  returnToCheck() {
    this.zone.run(() => {
      this.router.navigate(['/check']);
    });
  }


  createMockUser(){
    gapi.client.timetrackerApi.create().execute((response: any) => {
      if (response.error) {
        console.log(response.error);
      } else {
        console.log(JSON.stringify(response.result));
      }
      });
  }

  weeklyReport(){
    this.createMockUser();
    this.reportType = 0;
    this.zone.run(() => {
      this.router.navigate(['/weeklyreport']);
    });
  }

  monthlyReport(){
    this.createMockUser();
    this.reportType = 1;
    this.zone.run(() => {
      this.router.navigate(['/monthlyreport']);
    });
  }

  getReport(body) {
    return new Promise<any>((resolve) => {

      const content = {
        date: body.date,
        report_type: body.report_type
    };
      gapi.client.timetrackerApi.report(content).execute((response: any) => {
        if (response.error) {
          console.log(response.error);
          resolve(response.result);
        } else {
          resolve(response.result);
        }
      });
    });
  }

  logOut() {
    this.logged = false;
    this.auth2 = gapi.auth2.getAuthInstance();
    this.auth2.signOut().then(function () {
      console.log('User signed out.');
    });
    window.location.reload();
    console.log('reload page');
  }

  checkIn() {
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.checkin().execute((response: any) => {
        if (response.result.response_code === '400') {
          this.userWorkday.checkin = 'None';
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.userWorkday.checkin = this.returnDate(response.result.checkin);
          resolve(true);
        }
      });
    });
  }

  checkOut() {
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.checkout().execute((response: any) => {
        if (response.result.response_code === '400') {
          this.userWorkday.checkout = 'None';
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.userWorkday.checkout = this.returnDate(response.result.checkout);
          this.userWorkday.total = response.result.total;
          resolve(false);
        }
      });
    });
  }

  getWeekTotal() {
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.weektotal().execute((response: any) => {
        console.log(response);
      });
    });
  }

  returnDate(date) {
    if (date === 'None') {
      return 'None';
    }

    const d = new Date(date);

    if (d.getMinutes() < 10) {
      return `${d.getHours()}:0${d.getMinutes()}`;
    }

    return `${d.getHours()}:${d.getMinutes()}`;
  }

}
