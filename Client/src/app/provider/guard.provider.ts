import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { ServerProvider } from '../provider/server.provider';
@Injectable()
export class CanActivateViaUserWorkdayGuard implements CanActivate {

constructor(private server: ServerProvider) {}

async canActivate() {
    if (!this.server.getUserWorkday()) {
        console.log('User not found. Returning...');
        this.server.returnToLogin();
        return false;
    }else {
        // await this.server.getUserPermission();
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('User verified. Accessing...');
        return true;
    }
}

}

@Injectable()
export class CanActivateViaHRMRole implements CanActivate {

constructor(private server: ServerProvider) {}

async canActivate() {
    // await this.server.getUserPermission();

    if (this.server.getUserWorkday().hrm != 1) {
        console.log('User does not have HRM role. Returning...');
        this.server.logOut();
        this.server.returnToLogin();
        return false;
    }else {
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('HRM verified. Accessing...');
        return true;
    }

}

}

@Injectable()
export class CanActivateViaAdminRole implements CanActivate {

constructor(private server: ServerProvider) {}

async canActivate() {
    // await this.server.getUserPermission();
    if (this.server.getUserWorkday().admin != 1) {
        console.log('User does not have Admin role. Returning...');
        this.server.logOut();
        this.server.returnToLogin();
        return false;
    }else {
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('Admin verified. Accessing...');
        return true;
    }

}

}
