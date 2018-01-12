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
      this.selectedDate = this.server.getUserWorkday().date;
    } else {
      this.server.getListIPUser(this.selectedDate).then((response) => {
      this.ipUsers = response.ip_report;
      });
    }
  }

  close() {
    this.invalidDate = false;
  }

 /* getReport() {
    
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
  }*/
  
}
