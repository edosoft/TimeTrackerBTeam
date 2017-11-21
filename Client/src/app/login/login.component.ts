import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { AfterViewInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})


export class LoginComponent implements AfterViewInit {

  constructor(private server: ServerProvider) {

  }

  ngAfterViewInit() {
    this.server.googleInit();
  }

  createUser() {
    this.server.createUser();
  }

}
