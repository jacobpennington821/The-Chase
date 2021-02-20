import { TestBed } from '@angular/core/testing';

import { ChaseSocketService } from './chase-socket.service';

describe('ChaseSocketService', () => {
  let service: ChaseSocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ChaseSocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
