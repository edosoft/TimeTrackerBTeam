import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ServerProvider } from './provider/server.provider';

import {AppRoutingModule} from './provider/router.provider';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { CheckComponent } from './check/check.component';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    CheckComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [ServerProvider],
  bootstrap: [AppComponent]
})
export class AppModule { }
