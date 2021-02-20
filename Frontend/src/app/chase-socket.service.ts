import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { ClientState } from './client-state/client-state';

const socketPort = 8484;

@Injectable({
  providedIn: 'root'
})
export class ChaseSocketService {
  socket: WebSocketSubject<unknown>;
  state: ClientState;

  constructor() {
    console.log("Connecting websocket")
    this.socket = webSocket({
      url: "ws://" + window.location.hostname + ":" + socketPort,
      openObserver: {
        next: () => {
          this.onConnect();
        }
      },
    });
    this.socket.subscribe(
      msg => this.handleMessage(msg),
      err => this.handleError(err),
      () => this.handleClose(),
    );
    this.socket.next({ "action": "hello" });
  }

  private handleMessage(msg: any) {
    console.log("Socket message: " + msg);
    this.state.handleJSON(msg)
  }

  private handleError(err: unknown) {
    console.log("Socket error: " + err);
  }

  private onConnect() {
    console.log("Socket connected");
  }

  private handleClose() {
    console.log("Closed websocket");
  }

  public runAction(actionName: string, args: any) {
    let retState: ClientState | null = null;
    retState = this.state.runAction(actionName, args);
    while (retState != null) {
      this.state.exitState();
      let oldState = this.state;
      this.state = retState;
      retState = this.state.enterState(oldState);
    }
  }
}