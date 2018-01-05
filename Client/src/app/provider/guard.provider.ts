import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { ServerProvider } from '../provider/server.provider';
import { SessionStorageService } from 'ngx-webstorage';
import { User } from './model';

@Injectable()
export class CanActivateViaUserWorkdayGuard implements CanActivate {

constructor(private server: ServerProvider) {}

delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async canActivate() {
    if (!this.server.retrieveUser()) {
        console.log('Guard: User not found. Returning...');
        this.server.returnToLogin();
        return false;
    }else {
        // await this.server.getUserPermission();
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('Guard: User verified. Accessing...');
        await this.delay(1000);
        return true;
    }
}
}

@Injectable()
export class CanActivateLoginToCheck implements CanActivate {

constructor(private server: ServerProvider) {}

delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async canActivate() {
    if (this.server.retrieveUser() == undefined) {
        console.log('Guard: User not found.');
        return true;
    }else {
        // await this.server.getUserPermission();
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('Guard: User verified. Accessing...');
        await this.delay(1000);
        this.server.returnToCheck();
        return false;
    }
}
}

@Injectable()
export class CanActivateViaHRMRole implements CanActivate {

constructor(private server: ServerProvider) {}

async canActivate() {
    // await this.server.getUserPermission();
    if (this.server.retrieveUser().hrm != 1) {
        console.log('Guard: User does not have HRM role. Returning...');
        this.server.logOut();
        this.server.returnToLogin();
        return false;
    }else {
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('Guard: HRM verified. Accessing...');
        return true;
    }
}
}

@Injectable()
export class CanActivateViaAdminRole implements CanActivate {

constructor(private server: ServerProvider) {}

async canActivate() {
    // await this.server.getUserPermission();
    if (this.server.retrieveUser().admin != 1) {
        console.log('Guard: User does not have Admin role. Returning...');
        this.server.logOut();
        this.server.returnToLogin();
        return false;
    }else {
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('Guard: Admin verified. Accessing...');
        return true;
    }

}

}
