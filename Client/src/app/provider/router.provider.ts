import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CheckComponent } from '../check/check.component';
import { LoginComponent } from '../login/login.component';
import { IssuesComponent } from '../issues/issues.component';
import { ReportsComponent } from '../reports/reports.component';
import { AdminComponent } from '../admin/admin.component';
import { CanActivateViaUserWorkdayGuard, CanActivateViaHRMRole, CanActivateViaAdminRole, CanActivateLoginToCheck } from './guard.provider';
import { IpreportComponent } from '../ipreport/ipreport.component';

const appRoutes: Routes = [{
  path: '',
  component: LoginComponent,
  canActivate: [CanActivateLoginToCheck]
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
    CanActivateViaUserWorkdayGuard, CanActivateViaHRMRole
  ]
}, {
  path: 'monthlyreport',
  component: ReportsComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard, CanActivateViaHRMRole
  ]
}, {
  path: 'issues',
  component: IssuesComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard, CanActivateViaHRMRole
  ]
}, {
  path: 'admin',
  component: AdminComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard, CanActivateViaAdminRole
  ]
}, {
  path: 'ipreport',
  component: IpreportComponent,
  canActivate: [
    CanActivateViaUserWorkdayGuard, CanActivateViaAdminRole
  ]
}, {
  path: '**',
  redirectTo: ''
}];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule],
  declarations: [],
  providers: [CanActivateViaUserWorkdayGuard, CanActivateViaHRMRole, CanActivateViaAdminRole, CanActivateLoginToCheck],
})
export class AppRoutingModule { }
