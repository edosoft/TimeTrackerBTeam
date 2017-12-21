import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CheckComponent } from '../check/check.component';
import { LoginComponent } from '../login/login.component';
import { IssuesComponent } from '../issues/issues.component';
import { ReportsComponent } from '../reports/reports.component';
import { CanActivateViaUserWorkdayGuard } from './guard.provider';

const appRoutes: Routes = [{
  path: '',
  component: LoginComponent
}, {
  path: 'check',
  component: CheckComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard
  ]
}, {
  path: 'weeklyreport',
  component: ReportsComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard
  ]
}, {
  path: 'monthlyreport',
  component: ReportsComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard
  ]
}, {
  path: 'issues',
  component: IssuesComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard
  ]
}, {
  path: '**',
  redirectTo: ''
}];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule],
  declarations: [],
  providers: [CanActivateViaUserWorkdayGuard],
})
export class AppRoutingModule { }
