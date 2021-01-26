import { Component, OnInit, Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';
import { CountdownTimerComponent } from '../timer/timer.component';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

@Injectable()
@Component({
  selector: 'app-round-one',
  templateUrl: './round-one.component.html',
  styleUrls: ['./round-one.component.less']
})
export class RoundOneComponent implements OnInit {
  data: Question | null = null;
  loading: boolean;
  JSON;
  result: string = "";
  showResult: boolean;
  tallyAmount: number;
  isClickedOnce: boolean;
  answersArray: string[] | null = null;
  message: string = "";
  isTimeUp: boolean;
  enableRoundTwo: boolean = false;

  constructor(private http: HttpClient) {
    this.tallyAmount = 0;
    this.JSON = JSON;
    this.loading = true;
    this.showResult = false;
    this.isClickedOnce = false;
    this.isTimeUp = false;
  }

  ngOnInit() {
  }

  GetNewQuestion(): void {
    this.result = "";
    this.loading = true;
    this.http.get<QuestionResponse>('https://opentdb.com/api.php?amount=1&type=multiple')
      .subscribe((res: QuestionResponse) => {
        console.log(res);
        this.answersArray = this.ShuffleAnswers(res.results[0].incorrect_answers.concat(res.results[0].correct_answer));
        this.data = res.results[0];
        this.loading = false;
      });
  }

  private ShuffleAnswers(array: string[]): string[] {
    var currentIndex = array.length, temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  CheckAnswer(submittedAnswer: string): void {
    if (this.data == null) {
      return;
    }
    if (submittedAnswer === this.data.correct_answer) {
      this.result = "correct";
      this.tallyAmount = this.tallyAmount + 5000;
      this.message = "This is the correct answer!"
    }
    else {
      this.result = "incorrect";
      this.message = "Sorry,this is the wrong answer";
    }
    this.showResult = true;

    window.setTimeout(this.AlertResult.bind(this), 1000);
  }

  private AlertResult(): void {
    this.GetNewQuestion.bind(this)();
  }
}

interface QuestionResponse {
  results: Question[];
}

interface Question {
  category: string;
  type: string;
  difficulty: string;
  question: string;
  correct_answer: string;
  incorrect_answers: string[];
}
