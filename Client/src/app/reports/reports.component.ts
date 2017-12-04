import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { Injectable } from '@angular/core'
import { Report, Workday } from '../provider/model';

@Component({
  selector: 'app-reports',
  templateUrl: './reports.component.html',
  styleUrls: ['./reports.component.scss']
})
export class ReportsComponent{
  arrayResults: Report[];
  reportType: number;
  selectedDate: string;
  titleButton;
  arrayDays: string[] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
  numberDays: number[];
  noRecordsFound: string;
  todayDate: string;
  constructor(private server: ServerProvider) {
    this.todayDate = this.server.getUser().date;
    this.reportType = this.server.reportType;

    if (this.reportType == 0){
      this.titleButton = "Get Report";
    }else{
      this.titleButton = "Get Report";
    }
    this.selectedDate = this.server.getUser().date;
    this.getReport();
  }

  genMonthlyWorkdays(rawValues){
    let arrayReports: Report[] = rawValues.reports;
    let limitDaysForRow: number = rawValues.month;
    this.numberDays = new Array();
      for (var x = 1; x<=limitDaysForRow; x++){
        this.numberDays.push(x);
      }

    for (var x = 0; x < arrayReports.length; x++){
      let arrayWorkdaysByEmployee: Workday[] = [];
      for (var y = 0; y < limitDaysForRow; y++){
        let existent_work = arrayReports[x].workday.find(x => parseInt(x.date.split('-')[2]) == y+1);
        if (existent_work == undefined){
          let work = new Workday();
          work.day_week = y+1;
          work.total = '-';
          arrayWorkdaysByEmployee.push(work);
        }else{
          arrayWorkdaysByEmployee.push(existent_work)
        } 
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.arrayResults = arrayReports;
  }

  genWeeklyWorkdays(rawValues){
    let arrayReports: Report[] = rawValues.reports;
    let limitDaysForRow: number = 5;
    this.numberDays = new Array();
      for (var x = 1; x<=limitDaysForRow; x++){
        this.numberDays.push(x);
      }
    for (var x = 0; x < arrayReports.length; x++){
      let arrayWorkdaysByEmployee: Workday[] = [];
      for (var y = 0; y < limitDaysForRow; y++){
        let existent_work = arrayReports[x].workday.find(x => x.day_week == y+1);
        if (existent_work == undefined){
          let work = new Workday();
          work.day_week = y+1;
          work.total = '-';
          arrayWorkdaysByEmployee.push(work);
        }else{
          arrayWorkdaysByEmployee.push(existent_work)
        } 
      }
      arrayReports[x].workday = arrayWorkdaysByEmployee;
    }
    this.arrayResults = arrayReports;
  }

  //La funcion del boton
  getReport(){
    if (this.selectedDate == ""){
      this.noRecordsFound = "Please, insert a valid date. Returning to today";
      this.selectedDate = this.server.getUser().date;
    }else{
      var body = {
        date: this.selectedDate,
        report_type: this.reportType
    };
      this.server.getReport(body).then((response)=> {
        if (response.response_code == 400){
          this.noRecordsFound = "No records found in the selected date. Returning to today";
          this.selectedDate = this.server.getUser().date;
        }else{
          this.noRecordsFound = "";
          if (this.reportType== 1){
            this.genMonthlyWorkdays(response);
          }else{
            this.genWeeklyWorkdays(response);
          }
        }
      });
    }
}

  returnToCheck(){
    this.server.returnToCheck();
  }
}

