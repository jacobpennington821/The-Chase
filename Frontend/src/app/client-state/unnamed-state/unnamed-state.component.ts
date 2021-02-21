import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ActionRunner } from 'src/app/action-runner';
import { ChaseSocketService } from 'src/app/chase-socket.service';
import { MessageSender } from 'src/app/message-sender';
import { ClientState, ClientStateAction } from '../client-state';
import { SubmittingNameStateComponent } from '../submitting-name-state/submitting-name-state.component';

@Component({
  selector: 'app-unnamed-state',
  templateUrl: './unnamed-state.component.html',
  styleUrls: ['./unnamed-state.component.less']
})
export class UnnamedStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;
  playerName: string;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) {
    super();
    this.playerName = "";
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(UnnamedStateComponent);
    this.addAction(new ClientStateAction("submitName", (args) => {
      console.log("SUBMIT NAME");
      return new SubmittingNameStateComponent(componentFactoryResolver);
    }));
  }

  ngOnInit(): void {
  }

  onSubmit(event: unknown) {
    console.log(this.playerName);
    // TODO Theres got to be a better way to do this carcrash
    // this.socketService.runAction("submitName", { "name": this.playerName });
  }

  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }

}
