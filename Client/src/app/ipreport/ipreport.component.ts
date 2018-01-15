import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { IpReport } from '../provider/model';
import { stringify } from '@angular/core/src/util';

@Component({
  selector: 'app-ipreport',
  templateUrl: './ipreport.component.html',
  styleUrls: ['./ipreport.component.scss']
})
export class IpreportComponent implements OnInit {

  ipUsers: IpReport[];
  ipUser: any;
  reportType: number;
  currentDate: string;
  selectedDate: string;
  invalidDate: boolean;
  noRecordsFound: boolean;
  noTable: boolean;
  isPersonalIP: boolean;
  isResportIPUsersList: boolean;
  ipInfoByUser: any;
  userTable: boolean;
  startDate: string;
  endDate: string;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.reportType = 2;
    this.server.currentDate(this.reportType).then((response) => {
      this.selectedDate = response.date;
      this.getIPList(this.selectedDate);
    });
    this.isResportIPUsersList = true;
    this.isPersonalIP = false;
  }

  getIPList(selectedDate) {
    if (this.selectedDate == '') {
      this.invalidDate = true;
      this.noTable = true;
    } else {
      this.server.getListIPUser(this.selectedDate).then((response) => {
        if (response.response_code == 400) {
          this.noRecordsFound = true;
          this.noTable = true;
        } else {
          this.noTable = false;
          this.noRecordsFound = false;
          this.ipUsers = response.ip_report;
        }
      });
    }
  }

  setPersonalReportIP(user) {
    this.isPersonalIP = true;
    this.isResportIPUsersList = false;
    this.ipUser = user;
    this.server.currentDate(this.reportType).then((response) => {
      this.startDate = response.date;
      this.endDate = response.date;
      this.getCheckIP(this.ipUser);
    });
  }

  isPersonalReportIP() {
    this.isPersonalIP = !this.isPersonalIP;
  }

  backToReportIPUsersList() {
    this.isPersonalIP = false;
    this.isResportIPUsersList = true;
    this.getIPList(this.selectedDate);
    this.noTable = false;
  }

  getCheckIP(user) {
    this.ipUser = user;
    if ((this.startDate == '')||(this.endDate == '')) {
      this.invalidDate = true;
      this.noTable = true;
    } else if ((new Date(this.startDate) > (new Date(this.endDate)))) {
      this.invalidDate = true;
      this.noTable = true;
    } else {
      this.server.getIPByUser(this.ipUser.email, this.startDate, this.endDate).then((response) => {
        if (response.response_code == 400) {
          this.noRecordsFound = true;
          this.noTable = true;
        } else {
          this.ipInfoByUser = response.ip_values;
        }
      });
    }
  }

  closeInvalidDate() {
    this.invalidDate = false;
  }

  closeNoRecordsFound() {
    this.noRecordsFound = false;
  }
}

