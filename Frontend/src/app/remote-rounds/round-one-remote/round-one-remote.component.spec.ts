import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RoundOneRemoteComponent } from './round-one-remote.component';

describe('RoundOneRemoteComponent', () => {
  let component: RoundOneRemoteComponent;
  let fixture: ComponentFixture<RoundOneRemoteComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RoundOneRemoteComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RoundOneRemoteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
