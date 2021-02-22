import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ChaseSocketService } from 'src/app/chase-socket.service';
import { ClientState, ClientStateAction } from '../client-state';
import { CreatingLobbyStateComponent } from '../creating-lobby-state/creating-lobby-state.component';

@Component({
  selector: 'app-home-state',
  templateUrl: './home-state.component.html',
  styleUrls: ['./home-state.component.less']
})
export class HomeStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;
  joinCode: string;

  constructor(private componentFactoryResolver: ComponentFactoryResolver, socketService: ChaseSocketService) {
    super(socketService);
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(HomeStateComponent);
    this.addAction(new ClientStateAction("createLobby", (args) => {
      this.sendMessage({"action": "create_lobby"});
      return new CreatingLobbyStateComponent(componentFactoryResolver, socketService);
    }));
    this.addAction(new ClientStateAction("joinLobby", (args) => {
      return null;
    }));
    this.joinCode = "";
  }

  ngOnInit(): void {
  }

  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }

}
