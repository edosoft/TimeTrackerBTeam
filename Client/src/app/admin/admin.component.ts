import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';
import { User } from '../provider/model';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {

  isSetRole: any;
  isUserList: any;
  checkedAdmin: boolean = false;
  checkedHRM: boolean = false;
  userEmail: string;
  hrmValue: number;
  adminValue: number;
  users: User[];
  user_position: number;
  user: any;
  userRole : string;
  response_submit_code: number;
  response_submit_message: string;

  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.isUserList = true;
    this.isSetRole = false;
    this.server.getUserList().then((response) => {
      this.users = response.user_list;
    });
  }

  setUserRole(user) {
    this.isSetRole = true;
    this.isUserList = false;
    this.user = user;
    if ((user.admin == 0) && (user.hrm == 0)){
      this.userRole = 'Employee';
    }
    if ((user.admin == 0) && (user.hrm == 1)) {
      this.checkedHRM = true;
      this.userRole = 'Human Resource Manager';
    }
    if ((user.admin == 1) && (user.hrm == 0)) {
      this.checkedAdmin = true;
      this.userRole = 'Administrator';
    }
    if ((user.admin == 1) && (user.hrm == 1)) {
      this.checkedAdmin = true;
      this.checkedHRM = true;
      this.userRole = 'Administrator, Human Resource Manager';
    }

  }

  backToListUser() {
    this.isSetRole = false;
    this.isUserList = true;
    this.response_submit_code = 0;
    this.checkedAdmin = false;
    this.checkedHRM = false;
    this.server.getUserList().then((response) => {
      this.users = response.user_list;
    });
  }

  close(){
    this.response_submit_code = 0;
  }

  adminCheck(){
    this.checkedAdmin = !this.checkedAdmin;
  }

  hrmCheck(){
    this.checkedHRM = !this.checkedHRM;
  }

  sendRole() {

    this.userEmail = this.user.email;

    if ((this.checkedAdmin) && (!this.checkedHRM)) {
      this.adminValue = 1;
      this.hrmValue = 0;
    }
    if ((!this.checkedAdmin) && (this.checkedHRM)) {
      this.adminValue = 0;
      this.hrmValue = 1;
    }
    if ((this.checkedAdmin) && (this.checkedHRM)) {
      this.adminValue = 1;
      this.hrmValue = 1;
    }
    if ((!this.checkedAdmin) && (!this.checkedHRM)) {
      this.adminValue = 0;
      this.hrmValue = 0;
    }

    this.server.assignRole(this.userEmail, this.hrmValue, this.adminValue).then((response) => {
      this.response_submit_code = response.response_code;
      this.response_submit_message = response.text;
      if (response.response_code == 200) { 
        if ((this.checkedAdmin) && (!this.checkedHRM)) {
        this.userRole = 'Administrator';
        }
        if ((!this.checkedAdmin) && (this.checkedHRM)) {
          this.userRole = 'Human Resource Manager';
        }
        if ((this.checkedAdmin) && (this.checkedHRM)) {
          this.userRole = 'Administrator, Human Resource Manager';
        }
        if ((!this.checkedAdmin) && (!this.checkedHRM)) {
          this.userRole = 'Employee';
        }
      }
    });
  }

}
