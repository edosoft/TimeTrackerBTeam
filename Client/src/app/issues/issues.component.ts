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
}
