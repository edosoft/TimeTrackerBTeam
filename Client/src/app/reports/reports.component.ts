import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { Injectable } from '@angular/core';
import { Report, Workday } from '../provider/model';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent{
  results: Report[];
  reportType: number;
  selectedDate: string;
  invalidDate: boolean;
  buttonTitle: string;
  daysList: any[] = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  dayNumbers: number[];
  noRecordsFound: boolean;
  todayDate: string;
  Math = Math;

  constructor(private server: ServerProvider) {
    this.todayDate = this.server.getUserWorkday().date;
    this.reportType = this.server.reportType;

    if (this.reportType == 0) {
      this.buttonTitle = 'Get Weekly Report';
    } else {
      this.buttonTitle = 'Get Monthly Report';
    }

    this.selectedDate = this.server.getUserWorkday().date;
    this.getReport();
  }


  getCorrectWorkday(Workday, num){
    if (this.reportType == 0){
      return Workday.find(workday => workday.day_of_week == num + 1);
    }else{
      return Workday.find(workday => {
        return parseInt(workday.date.split('-')[2], 10) == num + 1;
      });
      
    }
  }

  generateWorkdays(rawValues){
    const arrayReports: Report[] = rawValues.reports;
    let limitDaysForRow;
    if (this.reportType == 0){
      limitDaysForRow = 7;
    }else{
      limitDaysForRow= rawValues.month;
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
        if (arrayReports[x].workday == undefined){
        existent_work = undefined;
        }else{
        existent_work = this.getCorrectWorkday(arrayReports[x].workday, y);
        }
        if (existent_work === undefined) {
          const workday = new Workday();
          workday.day_of_week = y + 1;
          workday.total = 0;
          arrayWorkdaysByEmployee.push(workday);
        }else {
          arrayWorkdaysByEmployee.push(existent_work);
        }
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.results = arrayReports;

  }

/*
  generateMonthlyWorkdays(rawValues) {
    const arrayReports: Report[] = rawValues.reports;
    const limitDaysForRow: number = rawValues.month;
    this.dayNumbers = [];

    for (let x = 1; x <= limitDaysForRow; x++) {
      this.dayNumbers.push(x);
    }
    this.daysList = this.dayNumbers;

    for (let x = 0; x < arrayReports.length; x++) {
      const arrayWorkdaysByEmployee: Workday[] = [];

      for (let y = 0; y < limitDaysForRow; y++) {
        let existent_work;
        if (arrayReports[x].workday == undefined){
        existent_work = undefined;
        }else{
        existent_work = arrayReports[x].workday.find(workday => {
          return parseInt(workday.date.split('-')[2], 10) == y + 1;
        });
        }

        if (existent_work === undefined) {
          const workday = new Workday();
          workday.day_of_week = y + 1;
          workday.total = 0;
          arrayWorkdaysByEmployee.push(workday);
        }else {
          arrayWorkdaysByEmployee.push(existent_work);
        }
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.results = arrayReports;
  }

  generateWeeklyWorkdays(rawValues) {
    const arrayReports: Report[] = rawValues.reports;
    const limitDaysForRow = 5;
    this.dayNumbers = [];

    for (let x = 1; x <= limitDaysForRow; x++) {
      this.dayNumbers.push(x);
    }
    for (let x = 0; x < arrayReports.length; x++) {
      const arrayWorkdaysByEmployee: Workday[] = [];

      for (let y = 0; y < limitDaysForRow; y++) {
        let existent_work;
        if (arrayReports[x].workday == undefined){
        existent_work = undefined;
        }else{
        existent_work = arrayReports[x].workday.find(workday => workday.day_of_week == y + 1);
        }
        console.log(existent_work);
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
*/

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
          /*
          if (this.reportType == 1) {
            this.generateMonthlyWorkdays(response);
          } else {
            this.generateWeeklyWorkdays(response);
          }*/
          this.generateWorkdays(response);
        }
      });
    }
  }

  returnToCheck() {
    this.server.returnToCheck();
  }

  close() {
    this.noRecordsFound = false;
    this.invalidDate = false;
  }
}

