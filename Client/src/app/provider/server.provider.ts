import { HttpClient, HttpHeaders} from '@angular/common/http';
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
  ismonthly: string;
  public auth2: any;

  public user: User;

  getUser() {
    return this.user;
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
        // console.log('Token: ' + googleUser.getAuthResponse().id_token);
        // console.log('ID: ' + profile.getId());
        // console.log('Name: ' + profile.getName());
        // console.log('Image URL: ' + profile.getImageUrl());
        // console.log('Email: ' + profile.getEmail());

        // YOUR CODE HERE
        this.user = new User();
        this.user.name = profile.getName();
        this.logIn();

      }, (error) => {
        alert(JSON.stringify(error, undefined, 2));
      });

  }

  // Check that user exists in datastore
  logIn() {
    gapi.client.timetrackerApi.login().execute((response: any) => {
      if (response.result.response_code === '400') {
        console.log(response.response_code);
      } else {
        // console.log(JSON.stringify(response.result));
        this.user.date = response.result.date;
        //console.log(response.result.checkin);
        this.user.checkin = this.returnDate(response.result.checkin);
        this.user.checkout = this.returnDate(response.result.checkout);
        this.user.id = response.result.employeeid;
        this.user.total = response.result.total;
        this.logged = true;
        // console.log('server logged:' + this.logged);
        this.zone.run(() => {
          this.router.navigate(['/check']);
        });
      }
    });
  }

  returnToCheck(){
    this.zone.run(() => {
      this.router.navigate(['/check']);
    });
  }

  report(ismonthly){
/*
    gapi.client.timetrackerApi.create().execute((response: any) => {
      if (response.error) {
        console.log(response.error);
      } else {
        console.log(JSON.stringify(response.result));
      }
    });
*/
    this.ismonthly = ismonthly;
    this.zone.run(() => {
      this.router.navigate(['/report']);
    });
  }

  getReport(body){
    return new Promise<any>((resolve) => {
      var content = {
        date: body.date,
        ismonthly: body.ismonthly
    };
      gapi.client.timetrackerApi.report(content).execute((response: any) => {
        if (response.error) {
          console.log(response.error);
          resolve(response.result);
        } else {
          //console.log(response.result);
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
          this.user.checkin = 'None';
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.user.checkin = this.returnDate(response.result.checkin);
          resolve(true);
        }
      });
    });
  }

  checkOut() {
    return new Promise<boolean>((resolve, reject) => {
      gapi.client.timetrackerApi.checkout().execute((response: any) => {
        if (response.result.response_code === '400') {
          this.user.checkout = 'None';
          resolve(false);
        } else {
          console.log(JSON.stringify(response.result));
          this.user.checkout = this.returnDate(response.result.checkout);
          this.user.total = response.result.total;
          resolve(false);
        }
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
