import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RoundOneComponent } from './round-one/round-one.component';
import { CountdownTimerComponent } from './timer/timer.component';
import { RoundOneRemoteComponent } from './remote-rounds/round-one-remote/round-one-remote.component';
import { UnnamedStateComponent } from './client-state/unnamed-state/unnamed-state.component';
import { SubmittingNameStateComponent } from './client-state/submitting-name-state/submitting-name-state.component';
import { FormsModule } from '@angular/forms';
import { HomeStateComponent } from './client-state/home-state/home-state.component';
import { CreatingLobbyStateComponent } from './client-state/creating-lobby-state/creating-lobby-state.component';

@NgModule({
  declarations: [
    AppComponent,
    RoundOneComponent,
    CountdownTimerComponent,
    RoundOneRemoteComponent,
    UnnamedStateComponent,
    SubmittingNameStateComponent,
    HomeStateComponent,
    CreatingLobbyStateComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
