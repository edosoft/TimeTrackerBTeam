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


  constructor(private server: ServerProvider) { }

  ngOnInit() {
    this.isUserList = true;
    this.isSetRole = false;
    this.server.getUserList().then((response) => {
      this.users = response.user_list;
    });
  }

  setUserRole() {
    this.isSetRole = true;
    this.isUserList = false;
  }

  backToListUser() {
    this.isSetRole = false;
    this.isUserList = true;
  }

  sendRole() {
    this.userEmail = this.server.getUserWorkday().id;

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
    this.server.assignRole(this.userEmail, this.hrmValue, this.adminValue);
  }

}
