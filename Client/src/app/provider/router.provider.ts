import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { CheckComponent } from '../check/check.component';
import { LoginComponent } from '../login/login.component';
import { ReportsComponent } from '../reports/reports.component';

const appRoutes: Routes = [{
  path: '',
  component: LoginComponent
}, {
  path: 'check',
  component: CheckComponent
}, {
  path: 'report',
  component: ReportsComponent
}, {
  path: '**',
  redirectTo: ''
}];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule],
  declarations: [],
  providers: [],
})
export class AppRoutingModule { }
