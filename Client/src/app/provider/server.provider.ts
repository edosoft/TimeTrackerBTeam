import { HttpClient } from '@angular/common/http';
import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { User } from '../provider/model';
import { Router } from '@angular/router';
import { SessionStorageService } from 'ngx-webstorage';
import { OnDestroy } from '@angular/core/src/metadata/lifecycle_hooks';
declare const gapi: any;

function getWindow(): any {
  return window;
}

@Injectable()
export class ServerProvider {

  constructor(private router: Router, private zone: NgZone, private store: SessionStorageService, private http: HttpClient) {
    this.sendLogin.subscribe((value) => {
      this.wrongAccount = value;
    });

    this.store.observe('key')
      .subscribe((value) => console.log('new value', value));

    this.initGapi();

    this.nativeWindow.onbeforeunload = () => {
      if (this.store.retrieve('savedUser') != undefined) {
        this.saveUser();
      }
    };
  }

  // Para seleccionar la url en local this.L y para trabajar sobre produccion con this.P
  L = 'http://localhost:8080/_ah/api';
  P = 'https://timetrackerbteam.appspot.com/_ah/api/';

  ip: string;
  url: string = this.P;
  logged = false;
  reportType: number;
  public wrongAccount = false;
  public sendLogin: Subject<boolean> = new Subject<boolean>();
  public auth2: any;

  public userWorkday: User;

  get nativeWindow(): any {
    return getWindow();
  }

  saveUser() {
    this.store.store('savedUser', this.userWorkday);
  }

  getReportType(): number {
    if (this.router.url == '/weeklyreport') {
      return 0;
    } else if (this.router.url == '/monthlyreport') {
      return 1;
    }
  }

  retrieveUser(): User {
    this.userWorkday = this.store.retrieve('savedUser');
    // console.log(this.userWorkday);
    if (this.userWorkday != undefined) {
      this.logged = true;
      return this.userWorkday;
    }
  }


  getAccountWrong(): Observable<any> {
    return this.sendLogin;
  }

  setAccountWrong() {
    this.sendLogin.next(true);
  }

  getUserWorkday(): User {
    return this.userWorkday;
  }

  public initGapi() {
    gapi.load('client:auth2', async () => {
      this.auth2 = gapi.auth2.init({
        client_id: '368116371345-ott8mvobq0aqcd8dvpu40b5n2fdjgs8v.apps.googleusercontent.com',
        cookiepolicy: 'single_host_origin',
        scope: 'profile email'
      });
      const that = this;
      gapi.client.load('timetrackerApi', 'v1', this.callback(that), this.url);
    });
  }

  public googleInit() {
    this.attachGSuite(document.getElementById('googleBtn'));
    return this.wrongAccount;
  }

  public callback(that) {
    console.log('gapi loaded');
    if (this.store.retrieve('savedUser') == undefined) {
      that.googleInit();
    }
  }

  public attachGSuite(element) {
    this.auth2.attachClickHandler(element, {},
      (googleUser) => {
        const profile = googleUser.getBasicProfile();
        this.userWorkday = new User();
        this.logIn({
          name: profile.getName()
        });
      }, (error) => {
        alert(JSON.stringify(error, undefined, 2));
      });
  }

  // Check that userWorkday exists in datastore
  logIn(body) {
    gapi.client.timetrackerApi.login(body).execute((response: any) => {
      if (response.result.response_code == 400) {
        this.setAccountWrong();
        console.log('Invalid user detected.');
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

        this.saveUser();
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
    } */
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
          // console.log(response.response_code);
          resolve(response.result);
        } else {
          // console.log(response.result);
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

  logOut() {
    this.logged = false;
    this.auth2 = gapi.auth2.getAuthInstance();
    this.auth2.signOut().then(function () {
      console.log('User signed out.');
    });
    window.location.reload();
    console.log('reload page');
    this.clearItem();
  }
  clearItem() {
    this.store.clear();
    // this.storage.clear(); //clear all the managed storage items
  }

  getIp() {
    this.http.get('https://ipinfo.io/json/').subscribe(data => {
      const value: any = data;
      console.log(value.ip);
      this.ip = value.ip;
    });
  }

  delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

  async checkIn() {
    this.getIp();
    await this.delay(400);
      const content = {
      ip: this.ip
    };
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.checkin(content).execute((response: any) => {
        if (response.result.response_code === '400') {
          this.userWorkday.checkin = 'None';
          // console.log(JSON.stringify(response.result));
          resolve(false);
        } else {
          // console.log(JSON.stringify(response.result));
          this.userWorkday.checkin = this.returnDate(response.result.checkin);
          this.userWorkday.checkin_number = response.result.number;
          resolve(true);
        }
      });
    });
  }

  async checkOut() {
    this.getIp();
    await this.delay(400);
    const content = {
      ip: this.ip
    };
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.checkout(content).execute((response: any) => {
        if (response.result.response_code === '400') {
          this.userWorkday.checkout = 'None';
          resolve(false);
        } else if (response.result.response_code === '300') {
          resolve(false);
        } else {
          // console.log(JSON.stringify(response.result));
          this.userWorkday.checkout = this.returnDate(response.result.checkout);
          this.userWorkday.checkout_number = response.result.number;
          this.userWorkday.total = response.result.total;
          resolve(true);
        }
      });
    });
  }

  getWeekTotal() {
    return new Promise<any>((resolve, reject) => {
      gapi.client.timetrackerApi.weektotal().execute((response: any) => {
        resolve(response.result.minutes);
      });
    });
  }

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
          resolve(response.result);
        } else {
          resolve(response.result);
        }
      });
    });
  }

  returnToIpReport() {
    this.zone.run(() => {
      this.router.navigate(['/ipreport']);
    });
  }

  getListIPUser(selectedDate) {
    return new Promise<any>((resolve) => {
      const content = {
        date: selectedDate
      };
      gapi.client.timetrackerApi.ip_userlist(content).execute((response: any) => {
        if (response.error) {
          resolve(response.result);
        } else {
          resolve(response.result);
        }
      });
    });
  }

  getIPByUser(email, startDate, endDate) {
    return new Promise<any>((resolve) => {
      const content = {
        email: email,
        start_date: startDate,
        end_date: endDate
      };
      gapi.client.timetrackerApi.ip_user(content).execute((response: any) => {
        if (response.error) {
          resolve(response.result);
        } else {
          resolve(response.result);
        }
      });
    });
  }

}
