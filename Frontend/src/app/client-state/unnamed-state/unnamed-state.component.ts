import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ClientState, ClientStateAction } from '../client-state';
import { SubmittingNameStateComponent } from '../submitting-name-state/submitting-name-state.component';

@Component({
  selector: 'app-unnamed-state',
  templateUrl: './unnamed-state.component.html',
  styleUrls: ['./unnamed-state.component.less']
})
export class UnnamedStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) {
    super();
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(UnnamedStateComponent);
    this.addAction(new ClientStateAction("submitName", (args) => {
      console.log("SUBMIT NAME");
      return new SubmittingNameStateComponent(componentFactoryResolver);
    }));
  }

  ngOnInit(): void {
  }


  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }

}
