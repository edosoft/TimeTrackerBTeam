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
  }

  backToListUser() {
    this.isSetRole = false;
    this.isUserList = true;
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
    console.log(this.adminValue);
    console.log(this.hrmValue);
    this.server.assignRole(this.userEmail, this.hrmValue, this.adminValue);
  }

}
