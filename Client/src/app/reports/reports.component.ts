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
  buttonTitle: string;
  daysList: any[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  dayNumbers: number[];
  noRecordsFound: string;
  todayDate: string;
  Math = Math;

  constructor(private server: ServerProvider) {
    this.todayDate = this.server.getUserWorkday().date;
    this.reportType = this.server.reportType;

    if (this.reportType === 0) {
      this.buttonTitle = 'Get Weekly Report';
    } else {
      this.buttonTitle = 'Get Monthly Report';
    }

    this.selectedDate = this.server.getUserWorkday().date;
    this.getReport();
  }


  getCorrectWorkday(workday, num) {
    if (this.reportType === 0) {
      return workday.find(wd => wd.day_of_week === num + 1);
    } else {
      return workday.find(wd => parseInt(wd.date.split('-')[2], 10) === num + 1);
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
        let existent_work;

        if (arrayReports[x].workday === undefined) {
          existent_work = undefined;
        } else {
          existent_work = this.getCorrectWorkday(arrayReports[x].workday, y);
        }

        if (existent_work === undefined) {
          const workday = new Workday();
          workday.day_of_week = y + 1;
          workday.total = 0;
          arrayWorkdaysByEmployee.push(workday);
        } else {
          arrayWorkdaysByEmployee.push(existent_work);
        }
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.results = arrayReports;

  }

  // La funcion del boton
  getReport() {
    if (this.selectedDate === '') {
      this.noRecordsFound = 'Please, insert a valid date. Returning to today';
      this.selectedDate = this.server.getUserWorkday().date;
    } else {

      const body = {
        date: this.selectedDate,
        report_type: this.reportType
      };

      this.server.getReport(body).then((response) => {
        if (response.response_code === 400) {
          this.noRecordsFound = 'No records found in the selected date. Returning to today';
          this.selectedDate = this.server.getUserWorkday().date;
        } else {
          this.noRecordsFound = '';
          this.generateWorkdays(response);
        }
      });
    }
  }

  hoursColor(report) {
    const time = report.total;
    let min;
    let max;

    // Weekly report
    if (this.reportType === 0) {
      min = 2400;
      max = min + 60;

      if (time < min) {
        return { 'color': 'red' };
      } else if (time > max) {
        return { 'color': 'blue' };
      } else {
        return { 'color': 'green' };
      }

      // Monthly report
    } else if (this.reportType === 1) {
      return { 'font-weight': 'bold' };
    }
  }

  hoursFormat(time) {
    const hours = time / 60;
    const mins = time % 60;

    const hoursStr = hours < 10 ? `0${hours}` : hours.toString();
    const minsStr = mins < 10 ? `0${mins}` : mins.toString();

    return `${hoursStr}:${minsStr}`;
  }

  returnToCheck() {
    this.server.returnToCheck();
  }
}

