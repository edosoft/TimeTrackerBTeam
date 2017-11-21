import { HttpClient, HttpHeaders} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';


declare const gapi: any;

@Injectable()
export class ServerProvider {

    // Para seleccionar la url en local this.L y para trabajar sobre produccion con this.P

    L: string = 'http://localhost:8080/_ah/api';
    P: string =  'http://timetracking-186111.appspot.com';
    url: string = this.L;

    public auth2: any;
    public api: any = null;
    public googleInit() {
        gapi.load('client:auth2', () => {
            this.auth2 = gapi.auth2.init({
                client_id: '953775827463-phpb8caafp8iceclntam7mpqaou3as8v.apps.googleusercontent.com',
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
                console.log('Token: ' + googleUser.getAuthResponse().id_token);
                console.log('ID: ' + profile.getId());
                console.log('Name: ' + profile.getName());
                console.log('Image URL: ' + profile.getImageUrl());
                console.log('Email: ' + profile.getEmail());

                // YOUR CODE HERE
            }, (error) => {
                alert(JSON.stringify(error, undefined, 2));
            });

    }

    doSomething() {
        gapi.client.timetrackerApi.login().execute((response: any) => {
            if (response.error) {
                console.log(response.error);
            } else {
                console.log(JSON.stringify(response.result));
            }
        }
        );
    }

    createUser() {
        gapi.client.timetrackerApi.createUser().execute((response: any) => {
            if (response.error) {
                console.log(response.error);
            } else {
                console.log(JSON.stringify(response.result));
            }
        });
    }
}
