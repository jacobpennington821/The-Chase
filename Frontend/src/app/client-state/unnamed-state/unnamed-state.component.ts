import { Component, OnInit } from '@angular/core';
import { ClientState, ClientStateAction } from '../client-state';

@Component({
  selector: 'app-unnamed-state',
  templateUrl: './unnamed-state.component.html',
  styleUrls: ['./unnamed-state.component.less']
})
export class UnnamedStateComponent extends ClientState implements OnInit {

  constructor() {
    super();
    this.addAction(new ClientStateAction("submitName", (args) => {
      return null;
    }));
  }

  ngOnInit(): void {
  }

}
