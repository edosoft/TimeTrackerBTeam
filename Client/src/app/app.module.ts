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
import { CanActivateViaUserWorkdayGuard } from './provider/guard.provider';
import { IssuesComponent } from './issues/issues.component';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CheckComponent,
    ReportsComponent,
    IssuesComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    NgbModule
  ],
  providers: [ServerProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }
