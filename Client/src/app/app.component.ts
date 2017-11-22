import { Component } from '@angular/core';
import { ServerProvider } from './provider/server.provider';
import { AfterViewInit } from '@angular/core/src/metadata/lifecycle_hooks';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {
  title_header = 'Time Tracking';
  is_logged: any = false;

  constructor(private server: ServerProvider) {
      this.is_logged = this.server.logged;
      console.log('before: ' + this.is_logged);
  }

  ngAfterViewInit() {
    /*this.is_logged = this.server.logged;
    console.log("After logged:" + this.server.logged);*/
  }

}
