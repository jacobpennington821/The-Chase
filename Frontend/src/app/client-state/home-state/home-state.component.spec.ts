import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeStateComponent } from './home-state.component';

describe('HomeStateComponent', () => {
  let component: HomeStateComponent;
  let fixture: ComponentFixture<HomeStateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HomeStateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
