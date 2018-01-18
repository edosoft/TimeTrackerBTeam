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
  wissue: any;
  startingIssues= false;
  noIssues= false;

  issueDate: any;
  issueType: any;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.getList();
  }
  close() {
    this.noIssues = false;
  }
  getList() {
    this.server.getUserWithIssues().then((response) => {
      if (response.text == 'Returning Issues') {
        const array = [];
        for (let x = 0; x < response.issues_per_employee.length; x++) {
          if (response.issues_per_employee[x].total_unsolved_peremp != 0) {
            array.push(response.issues_per_employee[x]);
          }
        }
        this.issues_per_employee = array;
        if (response.total_unsolved > 0) {
          this.startingIssues = true;
          this.changeViews = false;
        } else {
          this.noIssues = true;
          this.changeViews = false;
        }
      } else {
        this.noIssues = true;
        this.changeViews = false;
      }
      });
  }
  getList2() {
    this.server.getUserWithIssues().then((response) => {
    if (response.text == 'Returning Issues') {
      const array = [];
      for (let x = 0; x < response.issues_per_employee.length; x++) {
        if (response.issues_per_employee[x].total_unsolved_peremp != 0) {
          array.push(response.issues_per_employee[x]);
        }
      }
      this.issues_per_employee = array;
    }
    });
  }

  employeeView(row) {
    this.personalView = true;
    this.personalArray = row;
  }
  changeView(issue) {
    this.changeViews = true;
    this.personalView = false;
  }

  swapper() {
    if (this.changeViews == true) {
      this.changeViews = false;
      this.personalView = true;
    } else {
      this.personalView = false;
      this.startingIssues = true;
    }
  }


  // esta va a ser la funcion que recoja la wday referente a cada issue
  getWissue(issue, employee) {
      this.issueDate = issue.date.split(' ')[0];
      this.issueType = issue.issue_type;
      const content = {
        date: this.issueDate,
        email: employee,
        issue_type: this.issueType
      };
      this.server.getWorkdayFromIssue(content).then((response) => {
        if (this.issueType == 'Late Check In') {
          this.wissue = response.workday.checkin;
        } else {
            this.wissue = response.workday.checkout;
        }
        this.changeViews = true;
        this.personalView = false;
        });
    }
    sendCheckTimes() {
      const inputs = document.querySelectorAll('.checkInput');
      const correction = Array.prototype.map.call(inputs, (item) => item.value);
      const issueCorrection = {
        email: this.personalArray.employee,
        date: this.issueDate,
        issue_type: this.issueType,
        correction: correction
      };
      this.server.correctIssue(issueCorrection).then((response) => {
        this.getList();
      });
    }
}

