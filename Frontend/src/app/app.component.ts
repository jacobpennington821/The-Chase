import { Component, ComponentFactoryResolver, ViewChild, ViewContainerRef } from '@angular/core';
import { ChaseSocketService, StateSubscriber } from './chase-socket.service';
import { ClientState } from './client-state/client-state';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent implements StateSubscriber {
  title = 'The Chase';

  @ViewChild("vc", { read: ViewContainerRef })
  vc!: ViewContainerRef;

  constructor(private r: ComponentFactoryResolver, private socketService: ChaseSocketService){
    this.socketService = socketService;
    this.socketService.subscribe(this);
  }

  stateUpdated(newState: ClientState): void {
    this.updateView();
  }

  private updateView(): void {
    const componentFactory = this.socketService.state.getComponentFactory();
    this.vc.clear();
    const componentRef = this.vc.createComponent(componentFactory);
  }

  ngAfterViewInit() {
    this.updateView();
  }
}
