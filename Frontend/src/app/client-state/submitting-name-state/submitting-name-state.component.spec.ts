import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubmittingNameStateComponent } from './submitting-name-state.component';

describe('SubmittingNameStateComponent', () => {
  let component: SubmittingNameStateComponent;
  let fixture: ComponentFixture<SubmittingNameStateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SubmittingNameStateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmittingNameStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
