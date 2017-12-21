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

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.server.getUserWithIssues().then((response) => this.issues_per_employee = response.issues_per_employee);
  }



}
