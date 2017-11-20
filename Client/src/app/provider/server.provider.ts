import { HttpClient, HttpHeaders} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs/Rx';
import { Subject } from 'rxjs/Subject';


declare const gapi: any;

@Injectable()
export class ServerProvider{

    public auth2: any;
    public api: any =null;
    public googleInit() {
        gapi.load('client:auth2', () => {
            this.auth2 = gapi.auth2.init({
                client_id: '953775827463-qnn5h5i227iaule8b9r575sgck494jbc.apps.googleusercontent.com',
                cookiepolicy: 'single_host_origin',
                scope: 'profile email'
            });
            this.attachGSuite(document.getElementById('googleBtn'));
        });
    }

    public callback() {
        console.log("gapi loaded");
    }

    public attachGSuite(element) {
        gapi.client.load('timetrackerApi', "v1",this.callback, "http://localhost:8080/_ah/api")
        this.auth2.attachClickHandler(element, {},
            (googleUser) => {
                let profile = googleUser.getBasicProfile();
                console.log('Token: ' + googleUser.getAuthResponse().id_token);
                console.log('ID: ' + profile.getId());
                console.log('Name: ' + profile.getName());
                console.log('Image URL: ' + profile.getImageUrl());
                console.log('Email: ' + profile.getEmail());

                //YOUR CODE HERE
            }, (error) => {
                alert(JSON.stringify(error, undefined, 2));
            });
        
        
            // Useful data for your client-side scripts:
            /*var profile = googleUser.getBasicProfile();
            console.log("ID: " + profile.getId()); // Don't send this directly to your server!
            console.log('Full Name: ' + profile.getName());
            console.log('Given Name: ' + profile.getGivenName());
            console.log('Family Name: ' + profile.getFamilyName());
            console.log("Image URL: " + profile.getImageUrl());
            console.log("Email: " + profile.getEmail());
        
            // The ID token you need to pass to your backend:
            var id_token = googleUser.getAuthResponse().id_token;
            console.log("ID Token: " + id_token);
        
            this.postToken(id_token);*/
            
            // POST the token to the server
            /* var xhr = new XMLHttpRequest();
            xhr.open('POST', 'URL');
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.onload = function() {
            console.log('Signed in as: ' + xhr.responseText);
            };
            xhr.send('idtoken=' + id_token);
            */
    }

    doSomething() {
        gapi.client.timetrackerApi.login().execute((response: any) => {
            if (response.error) {
                console.log(response.error)
            }
            else {
                console.log(JSON.stringify(response.result));
            }
        }
        );
    }

    createUser() {
        gapi.client.timetrackerApi.createUser().execute((response: any) => {
            if (response.error) {
                console.log(response.error)
            }
            else {
                console.log(JSON.stringify(response.result));
            }
        }
        );
    }
        

}