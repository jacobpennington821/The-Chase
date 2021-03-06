import { ComponentFactoryResolver, Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from "rxjs/webSocket";
import { ActionRunner } from './action-runner';
import { ClientState } from './client-state/client-state';
import { UnnamedStateComponent } from './client-state/unnamed-state/unnamed-state.component';
import { MessageSender } from './message-sender';

const socketPort = 8484;

@Injectable({
  providedIn: 'root'
})
export class ChaseSocketService implements ActionRunner, MessageSender {
  socket: WebSocketSubject<unknown>;
  state: ClientState;
  subscriber: StateSubscriber | null;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) {
    console.log("Connecting websocket");
    this.subscriber = null;
    this.state = new UnnamedStateComponent(componentFactoryResolver, this);
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

  sendMessage(msg: any): void {
    if (this.socket.closed) {
      console.log("Couldn't send, socket closed.")
      return;
    }
    this.socket.next(msg);
  }

  ngOnInit() { }

  private handleMessage(msg: any): void {
    console.log(msg);
    if (!("action" in msg)) {
      console.log("Malformed event: " + msg)
      return;
  }
    this.runAction(msg["action"], msg);
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
    this.subscriber?.stateUpdated(this.state);
  }

  public subscribe(subscriber: StateSubscriber) {
    this.subscriber = subscriber;
  }
}

export interface StateSubscriber {
  stateUpdated(newState: ClientState): void;
}