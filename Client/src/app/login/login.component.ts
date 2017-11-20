import { Component, OnInit } from '@angular/core';

declare const gapi: any;

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})


export class LoginComponent{
  
  /*user: string;
  pass: string;*/

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

    gapi.client.load('timetrackerApi', "v1",this.callback, "http://localhost:8080/_ah/api/")
    this.auth2.attachClickHandler(element, {},
      (googleUser) => {

        let profile = googleUser.getBasicProfile();
        console.log('Token || ' + googleUser.getAuthResponse().id_token);
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

  ngAfterViewInit(){
    this.googleInit();
  }

  /*postToken(token) {
    
    fetch('URL', {
      method: 'POST',
      headers : new Headers({'Content-Type': 'application/x-www-form-urlencoded'}),
      body: JSON.stringify({
        idtoken: token
      })
    }).then((res) => res.json())
    .then((data) =>  console.log(data))
    .catch((err)=>console.log(err))
  }*/

}
