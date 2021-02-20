import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnnamedStateComponent } from './unnamed-state.component';

describe('UnnamedStateComponent', () => {
  let component: UnnamedStateComponent;
  let fixture: ComponentFixture<UnnamedStateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UnnamedStateComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UnnamedStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
