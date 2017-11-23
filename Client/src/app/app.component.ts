import { Component } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { DoCheck } from '@angular/core';
import { User } from './provider/model';
import {Observable} from 'rxjs/Observable';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements DoCheck {
  title_header = 'Time Tracking';
  is_logged: any;

  constructor(private server: ServerProvider) {

  }

  ngDoCheck() {
    this.is_logged = this.server.logged;
  }

}
