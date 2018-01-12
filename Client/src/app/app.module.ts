import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { ServerProvider } from './provider/server.provider';
import { AppRoutingModule } from './provider/router.provider';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { CheckComponent } from './check/check.component';
import { ReportsComponent } from './reports/reports.component';
import { IssuesComponent } from './issues/issues.component';
import { AdminComponent } from './admin/admin.component';

import {Ng2Webstorage} from 'ngx-webstorage';
import { IpreportComponent } from './ipreport/ipreport.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CheckComponent,
    ReportsComponent,
    IssuesComponent,
    AdminComponent,
    IpreportComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    NgbModule,
    Ng2Webstorage
  ],
  providers: [ServerProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }
