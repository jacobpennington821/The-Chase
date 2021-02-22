import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ChaseSocketService } from 'src/app/chase-socket.service';
import { ClientState, ClientStateAction } from '../client-state';

@Component({
  selector: 'app-creating-lobby-state',
  templateUrl: './creating-lobby-state.component.html',
  styleUrls: ['./creating-lobby-state.component.less']
})
export class CreatingLobbyStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;

  constructor(private componentFactoryResolver: ComponentFactoryResolver, socketService: ChaseSocketService) {
    super(socketService);
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(CreatingLobbyStateComponent);
    this.addAction(new ClientStateAction("lobby_hosted", (args) => {
      return null; // Transition to hosting lobby state
    }));
  }

  ngOnInit(): void {
  }

  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }
}