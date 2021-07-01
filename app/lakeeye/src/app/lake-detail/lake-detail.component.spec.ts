import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LakeDetailComponent } from './lake-detail.component';

describe('LakeDetailComponent', () => {
  let component: LakeDetailComponent;
  let fixture: ComponentFixture<LakeDetailComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LakeDetailComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LakeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
