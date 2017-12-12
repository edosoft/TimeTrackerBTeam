import { Component, OnInit } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { DoCheck, NgZone } from '@angular/core';
import { User } from './provider/model';
import { Observable } from 'rxjs/Observable';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements DoCheck, OnInit {
  isLogged: any;
  currentUserWorkday: any;

  constructor(private server: ServerProvider, private zone: NgZone, private router: Router) {}

  ngOnInit() {
    this.currentUserWorkday = this.server.getUserWorkday();
  }

  ngDoCheck() {
    this.isLogged = this.server.logged;
    this.currentUserWorkday = this.server.getUserWorkday();
  }

  logOut() {
    this.server.logOut();
    this.zone.run(() => {
      this.router.navigate(['']);
    });
  }
  returnToCheck() {
    console.log('returntocheck');
    this.server.returnToCheck();
  }
  weeklyReport() {
    this.server.weeklyReport();
  }
  monthlyReport() {
    this.server.monthlyReport();
  }
}
