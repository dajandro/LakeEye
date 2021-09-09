import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LakesListComponent } from './lakes-list.component';

describe('LakesListComponent', () => {
  let component: LakesListComponent;
  let fixture: ComponentFixture<LakesListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LakesListComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LakesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
