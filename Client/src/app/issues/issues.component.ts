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

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.server.getUserWithIssues().then((response) => this.issues_per_employee = response.issues_per_employee);
  }
  employeeView(row) {
    this.personalView = true;
    this.personalArray = row;
    console.log(this.personalArray.issues);
  }
  changeView(issue) {
    this.changeViews = true;
    this.personalView = false;
    console.log(issue);
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
