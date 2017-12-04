import { Component, OnInit } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { DoCheck } from '@angular/core';
import { User } from './provider/model';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements DoCheck, OnInit {
  isLogged: any;
  currentUserWorkday: any;

  constructor(private server: ServerProvider) {}

  ngOnInit() {
    this.currentUserWorkday = this.server.getUserWorkday();
  }

  ngDoCheck() {
    this.isLogged = this.server.logged;
    this.currentUserWorkday = this.server.getUserWorkday();
  }

  logOut() {
    this.server.logOut();
  }

}
