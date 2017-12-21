import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { Injectable } from '@angular/core';
import { Report, Workday } from '../provider/model';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent {
  results: Report[];
  reportType: number;
  selectedDate: string;
  invalidDate: boolean;
  buttonTitle: string;
  infoText: string;
  daysList: any[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  dayNumbers: number[];
  noRecordsFound: boolean;
  todayDate: string;
  Math = Math;

  constructor(private server: ServerProvider) {
    this.todayDate = this.server.getUserWorkday().date;
    this.reportType = this.server.reportType;

    if (this.reportType === 0) {

      this.buttonTitle = 'Get Weekly Report';
      this.infoText = 'Select a week to get the report';
    } else {

      this.buttonTitle = 'Get Monthly Report';
      this.infoText = 'Select a month to get the report';
    }

    this.server.currentDate(this.reportType).then((response) => {
      this.selectedDate = response.date;
      this.getReport();
    });
    //this.getReport();
  }


  getCorrectWorkday(workday, num) {
    if (this.reportType === 0) {
      return workday.find(wd => wd.day_of_week == num + 1);
    } else {
      return workday.find(wd => parseInt(wd.date.split('-')[2], 10) == num + 1);
    }
  }

  generateWorkdays(rawValues) {
    const arrayReports: Report[] = rawValues.reports;
    let limitDaysForRow;

    if (this.reportType === 0) {
      limitDaysForRow = 7;
    } else {
      limitDaysForRow = rawValues.month;
      this.dayNumbers = [];

      for (let x = 1; x <= limitDaysForRow; x++) {
        this.dayNumbers.push(x);
      }

      this.daysList = this.dayNumbers;
    }

    for (let x = 0; x < arrayReports.length; x++) {
      const arrayWorkdaysByEmployee: Workday[] = [];

      for (let y = 0; y < limitDaysForRow; y++) {
        const existent_work = this.getCorrectWorkday(arrayReports[x].workday, y);
        arrayWorkdaysByEmployee.push(existent_work);
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.results = arrayReports;

  }

  // La funcion del boton
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
  }

  hoursColor(report) {
    const time = report.total;
    let min;
    let max;
    let color;

    // Weekly report
    if (this.reportType === 0) {
      min = 2400;
      max = min + 60;

      if (time < min) {
        color = 'red';
      } else if (time > max) {
        color = 'blue';
      } else {
        color = 'green';
      }

      return { 'font-weight': 'bold', 'color': `${color}` };

      // Monthly report
    } else if (this.reportType === 1) {
      return { 'font-weight': 'bold' };
    }
  }

  hoursFormat(time) {
    const hours = Math.trunc(time / 60);
    const mins = time % 60;

    const hoursStr = hours < 10 ? `0${hours}` : hours.toString();
    const minsStr = mins < 10 ? `0${mins}` : mins.toString();

    return `${hoursStr}:${minsStr}`;
  }

  weekendColumn() {
    /*if (this.reportType === 1) {
      return { 'background-color': 'grey' };
    }*/
  }

  returnToCheck() {
    this.server.returnToCheck();
  }

  close() {
    this.noRecordsFound = false;
    this.invalidDate = false;
  }
}

