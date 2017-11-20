import { Component, OnInit } from '@angular/core';
import { ServerProvider } from '../provider/server.provider';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})


export class LoginComponent{
  
  /*user: string;
  pass: string;*/

  constructor(private server: ServerProvider) { 
    
  }
 
  ngAfterViewInit(){
    this.server.googleInit();
  }

  doSomething() {
    this.server.doSomething();
  }



  /*postToken(token) {
    
    fetch('URL', {
      method: 'POST',
      headers : new Headers({'Content-Type': 'application/x-www-form-urlencoded'}),
      body: JSON.stringify({
        idtoken: token
      })
    }).then((res) => res.json())
    .then((data) =>  console.log(data))
    .catch((err)=>console.log(err))
  }*/

}
