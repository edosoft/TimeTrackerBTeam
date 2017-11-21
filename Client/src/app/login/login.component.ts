import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { AfterViewInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})


export class LoginComponent implements AfterViewInit {

  /*user: string;
  pass: string;*/

  constructor(private server: ServerProvider) { 

  }

  ngAfterViewInit(){
    this.server.googleInit();
  }

  doSomething() {
    this.server.doSomething();
  }

  createUser(){
    this.server.createUser();
  }

}
