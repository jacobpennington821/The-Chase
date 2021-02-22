import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ChaseSocketService } from 'src/app/chase-socket.service';
import { ClientState, ClientStateAction } from '../client-state';
import { HomeStateComponent } from '../home-state/home-state.component';

@Component({
  selector: 'app-submitting-name-state',
  templateUrl: './submitting-name-state.component.html',
  styleUrls: ['./submitting-name-state.component.less']
})
export class SubmittingNameStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;

  constructor(private componentFactoryResolver: ComponentFactoryResolver, socketService: ChaseSocketService) {
    super(socketService);
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(SubmittingNameStateComponent);
    this.addAction(new ClientStateAction("ack_name", (args) => {
      console.log("Name acked");
      return new HomeStateComponent(componentFactoryResolver, socketService);
    }));
  }

  ngOnInit(): void {
  }

  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }

}
