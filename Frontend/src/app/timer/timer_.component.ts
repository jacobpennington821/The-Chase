import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-timer',
  templateUrl: './timer.component.html',
  styleUrls: ['./timer.component.css']
})
export class TimerComponent implements OnInit {
  timeLeft :number ;
 
  timerId;
  
  Countdown() {
    if (this.timeLeft == 0) {
      clearTimeout(this.timerId);
      alert("Total Amount in Round 1 -");
    } 
  }

  

  constructor() {
  this.timeLeft = 120;
  this.timerId = setInterval(this.Countdown, 1000);
   }

  ngOnInit() {
  }

}
