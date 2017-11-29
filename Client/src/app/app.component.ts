import { Component } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { DoCheck } from '@angular/core';
import { User } from './provider/model';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements DoCheck {
  titleHeader = 'Time Tracking';
  isLogged: any;
  currentUser: any;

  constructor(private server: ServerProvider) {
  }

  ngDoCheck() {
    this.isLogged = this.server.logged;
    this.currentUser = this.server.getUser();
  }

  logOut() {
    this.server.logOut();
  }

}
