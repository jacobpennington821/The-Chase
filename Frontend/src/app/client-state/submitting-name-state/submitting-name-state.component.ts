import { Component, ComponentFactory, ComponentFactoryResolver, OnInit } from '@angular/core';
import { ClientState } from '../client-state';

@Component({
  selector: 'app-submitting-name-state',
  templateUrl: './submitting-name-state.component.html',
  styleUrls: ['./submitting-name-state.component.less']
})
export class SubmittingNameStateComponent extends ClientState implements OnInit {

  componentFactory: ComponentFactory<ClientState>;

  constructor(private componentFactoryResolver: ComponentFactoryResolver) {
    super();
    this.componentFactory = this.componentFactoryResolver.resolveComponentFactory(SubmittingNameStateComponent);

  }

  ngOnInit(): void {
  }

  public getComponentFactory(): ComponentFactory<ClientState> {
    return this.componentFactory;
  }

}
