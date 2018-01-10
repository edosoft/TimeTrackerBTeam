import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';


@Component({
  selector: 'app-issues',
  templateUrl: './issues.component.html',
  styleUrls: ['./issues.component.scss']
})
export class IssuesComponent implements OnInit {
  issues_per_employee: any = [];
  JSON = JSON;
  personalView= false;
  changeViews= false;
  personalArray: any = [];
  personalIssue: any;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.server.getUserWithIssues().then((response) => this.issues_per_employee = response.issues_per_employee);
  }
  employeeView(row) {
    this.personalView = true;
    this.personalArray = row;
    console.log(this.personalArray);
  }
  changeView(issues) {
    this.changeViews = true;
    this.personalView = false;
    this.personalIssue = issues;
    console.log(this.personalIssue);
  }
  swapper() {
    if (this.changeViews == true) {
      this.changeViews = false;
      this.personalView = true;
    } else {
      this.personalView = false;
    }
  }

/* 
  // esta va a ser la funcion que recoja la wday referente a cada issue
  getReport() {
    if (this.selectedDate == '') {
      this.invalidDate = true;
      this.selectedDate = this.server.getUserWorkday().date;
    } else {
      const body = {
        date: this.selectedDate,
        report_type: this.reportType
      };
      this.server.getReport(body).then((response) => {
        if (response.response_code == 400) {
          this.noRecordsFound = true;
          this.selectedDate = this.server.getUserWorkday().date;
        } else {
          this.noRecordsFound = false;
          this.generateWorkdays(response);
        }
      });
    }
  } */
}
