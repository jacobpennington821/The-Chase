import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingLobbyStateComponent } from './creating-lobby-state.component';

describe('CreatingLobbyStateComponent', () => {
  let component: CreatingLobbyStateComponent;
  let fixture: ComponentFixture<CreatingLobbyStateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreatingLobbyStateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreatingLobbyStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
