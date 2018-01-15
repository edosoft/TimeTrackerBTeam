import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { IpReport } from '../provider/model';

@Component({
  selector: 'app-ipreport',
  templateUrl: './ipreport.component.html',
  styleUrls: ['./ipreport.component.scss']
})
export class IpreportComponent implements OnInit {

  ipUsers: IpReport[];
  reportType: number;
  currentDate: string;
  selectedDate: string;
  invalidDate: boolean;
  noRecordsFound: boolean;
  noTable: boolean;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.reportType = 2;
    this.server.currentDate(this.reportType).then((response) => {
      this.selectedDate = response.date;
      this.getIPList(this.selectedDate);
    });
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

  closeInvalidDate() {
    this.invalidDate = false;
  }

  closeNoRecordsFound() {
    this.noRecordsFound = false;
  }



}
