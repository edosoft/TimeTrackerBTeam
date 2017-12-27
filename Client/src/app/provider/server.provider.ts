import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { User } from '../provider/model';
import { Router } from '@angular/router';

declare const gapi: any;

@Injectable()
export class ServerProvider {

  constructor(private router: Router, private zone: NgZone) { }

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
        // console.log(JSON.stringify(response.result));
        this.userWorkday.id = response.result.email;
        this.userWorkday.name = response.result.name;
        this.userWorkday.hrm = response.result.hrm;
        this.userWorkday.admin = response.result.admin;
        this.userWorkday.date = response.result.date;
        this.userWorkday.checkin = this.returnDate(response.result.checkin);
        this.userWorkday.checkout = this.returnDate(response.result.checkout);
        this.userWorkday.total = response.result.total;

        this.userWorkday.checkin_number = this.returnNumber(response.result.checkin);
        this.userWorkday.checkout_number = this.returnNumber(response.result.checkout);

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

  returnToLogin() {
    this.zone.run(() => {
      this.router.navigate(['']);
    });
  }
/*
  createMockUser() {
    gapi.client.timetrackerApi.create().execute((response: any) => {
      if (response.error) {
        console.log(response.error);
      }
    });
  }*/
  issuesReport() {
    this.zone.run(() => {
      this.router.navigate(['/issues']);
    });
  }

  weeklyReport() {
    // this.createMockUser();
    this.reportType = 0;
    this.zone.run(() => {
      this.router.navigate(['/weeklyreport']);
    });
  }

  monthlyReport() {
    // this.createMockUser();
    this.reportType = 1;
    this.zone.run(() => {
      this.router.navigate(['/monthlyreport']);
    });
  }

  getUserWithIssues() {
    return new Promise<any>((resolve) => {
      gapi.client.timetrackerApi.issues().execute((response: any) => {
        if (response.error) {
          console.log(response.response_code);
          resolve(response.result);
        } else {
          console.log(response.result);
          resolve(response.result);
        }
      });
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

  currentDate(reportType) {
    return new Promise<any>((resolve) => {

      const content = {
        report_type: reportType
      };
      gapi.client.timetrackerApi.date(content).execute((response: any) => {
        if (response.error) {
          console.log(response.error);
          resolve(response.result);
        } else {
          resolve(response.result);
        }
      });
    });
  }
  /*
    currentDate() {
      gapi.client.timetrackerApi.date() {
        return = response.result;
      }
    }
  */
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
          console.log(JSON.stringify(response.result));
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.userWorkday.checkin = this.returnDate(response.result.checkin);
          this.userWorkday.checkin_number = response.result.number;
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
        } else if (response.result.response_code === '300') {
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.userWorkday.checkout = this.returnDate(response.result.checkout);
          this.userWorkday.checkout_number = response.result.number;
          this.userWorkday.total = response.result.total;
          resolve(true);
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
/*
  getUserPermission() {
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.currentuser().execute((response: any) => {
        this.userWorkday.admin = response.result.admin_value;
        this.userWorkday.hrm = response.result.hrm_value;
        resolve(true);
      });
    });
  }*/

  returnDate(date) {
    let time;
    if (date == undefined) {
      return 'None';
    } else if (typeof (date) === 'string') {
      time = date;
    } else if (typeof (date) === 'object') {
      time = date[date.length - 1];
    }
    // 2017-12-21 15:43:34.251013
    time = (time.split(' ', 2)[1]).split(':', 2);
    return `${time[0]}:${time[1]}`;
  }

  returnNumber(array) {
    if (array == undefined) {
      return 0;
    }
    return array.length;
  }

  returnToAdmin() {
    this.zone.run(() => {
      this.router.navigate(['/admin']);
    });
  }

  assignRole(email, hrm, admin) {
    return new Promise<any>((resolve) => {
      const content = {
        user_email: email,
        hrm_value: hrm,
        admin_value: admin
      };
      gapi.client.timetrackerApi.change_role(content).execute((response: any) => {
      if (response.error) {
        console.log(response.error);
        resolve(response.result);
      } else {
        resolve(response.result);
      }
      });
    });
  }

  getUserList() {
    return new Promise<any>((resolve, reject) => {
      gapi.client.timetrackerApi.user_list().execute((response: any) => {
        if (response.error) {
          console.log(response.error);
          resolve(response.result);
        } else {
          console.log(response.result);
          resolve(response.result);
        }
      });
    });
  }

}
