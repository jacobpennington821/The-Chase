import { Component, OnDestroy, OnInit } from '@angular/core';

// @Component({
//  selector: 'countdown-timer',
//  template: '<div class="text-shadow text-center"><p>{{message}}</p></div>',
//  styles: ["text-shadow: -2px 0 black, 0 2px black, 2px 0 black, 0 -2px black;"]
// })

@Component({
  selector: 'countdown-timer',
  template: '',
  styles: ['']
 })
export class CountdownTimerComponent implements OnInit, OnDestroy {

 intervalId = 0;
 message = '';
 seconds = 60;
 isTimeUp: boolean = false;
 clearTimer() { clearInterval(this.intervalId); }
 ngOnInit()    { }
 ngOnDestroy() { this.clearTimer(); }

 start() { this.countDown(); }

 private countDown() 
  {
   this.clearTimer();
   this.intervalId = window.setInterval(() => {
                                              this.seconds -= 1;
                                                if (this.seconds === 0) 
                                                  {
                                                    this.message = 'Time up!';
                                                    this.isTimeUp = true;
                                                    this.clearTimer();
                                                  }
                                              }, 1000);
  }
}