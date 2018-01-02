import { Component, OnInit, NgZone } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { AfterViewInit, DoCheck } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements AfterViewInit {
  wrongAccount = false;
  constructor(private server: ServerProvider, private zone: NgZone) {
    this.server.getAccountWrong().subscribe((value) => {
      this.zone.run(() => {
        this.wrongAccount = value;
    });
    });
  }
  ngAfterViewInit() {
    this.server.googleInit();
  }

  closeWarning() {
    this.wrongAccount = false;
  }
}
