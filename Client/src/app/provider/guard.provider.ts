import { Injectable } from '@angular/core';
import { CanActivate } from '@angular/router';
import { ServerProvider } from '../provider/server.provider';
@Injectable()
export class CanActivateViaUserWorkdayGuard implements CanActivate {

constructor(private server: ServerProvider) {}

canActivate() {
    if (!this.server.getUserWorkday()) {
        console.log('User not found. Returning...');
        this.server.returnToLogin();
        return false;
    }else {
        // The guard checks the value of the role level of the user. Depending on it,
        // the user won't be able to access.
        console.log('User verified. Accessing...');
        return true;
    }
}

}
