import { Component, OnInit } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { DoCheck } from '@angular/core';
import { User } from './provider/model';
import { Observable } from 'rxjs/Observable';
import { SessionStorageService } from 'ngx-webstorage';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements DoCheck, OnInit {
  isLogged: any;
  currentUserWorkday: any;
  isCollapsed = true;
  location = location;

  constructor(private server: ServerProvider) {
    document.addEventListener('click', () => this.closeNavBar());
  }

  ngOnInit() {
    // this.currentUserWorkday = this.server.getUserWorkday();
    this.retrieveValue();
  }

  retrieveValue() {
    this.currentUserWorkday = this.server.retrieveUser();
  }

  ngDoCheck() {
    this.isLogged = this.server.logged;
    this.currentUserWorkday = this.server.getUserWorkday();
  }

  closeNavBar() {
    if (this.isCollapsed === false) {
      this.isCollapsed = true;
    }
  }

  toggleNavBar() {
    this.isCollapsed = !this.isCollapsed;
    event.stopPropagation();
  }

  logOut() {
    this.server.logOut();
    this.server.returnToLogin();
  }
  returnToCheck() {
    this.server.returnToCheck();
  }
  weeklyReport() {
    this.server.weeklyReport();
  }
  monthlyReport() {
    this.server.monthlyReport();
  }
  issuesReport() {
    this.server.issuesReport();
  }
  returnToIpReport() {
    this.server.returnToIpReport();
  }
  returnToAdmin() {
    this.server.returnToAdmin();
  }
}
