import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { FormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './provider/router.provider';
import { LoginComponent } from './login/login.component';
import { CheckComponent } from './check/check.component';
import { ReportsComponent } from './reports/reports.component';
import { IssuesComponent } from './issues/issues.component';
import { AdminComponent } from './admin/admin.component';
import {APP_BASE_HREF} from '@angular/common';
import { ServerProvider } from './provider/server.provider';
describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;
  let compiled;
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [FormsModule, NgbModule, AppRoutingModule],
      declarations: [
        AppComponent,
        LoginComponent,
        CheckComponent,
        ReportsComponent,
        IssuesComponent,
        AdminComponent
      ],
      providers: [ServerProvider, {provide: APP_BASE_HREF, useValue : '/' }]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    compiled = fixture.debugElement.nativeElement;
  });

  fit('should create the app', async(() => {
    expect(component).toBeTruthy();
  }));
  fit(`should have as title 'Time Tracking Application'`, async(() => {
    // const app = fixture.debugElement.componentInstance;
    expect(compiled.querySelector('#title')).toBeTruthy();
  }));
});
