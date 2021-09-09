import { Component, OnInit, OnDestroy } from '@angular/core';
import { ApiService } from '../api.service';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-lakes-list',
  templateUrl: './lakes-list.component.html',
  styleUrls: ['./lakes-list.component.css']
})
export class LakesListComponent implements OnInit, OnDestroy {

  lakes: any;
  
  dtOptions: DataTables.Settings = {};
  dtTrigger: Subject<any> = new Subject<any>();

  constructor(private apiService: ApiService) { }

  ngOnInit(): void {

    this.dtOptions = {
      pagingType: 'full_numbers',
      pageLength: 10
    };
    this.apiService.getLakesRank().subscribe(data => {
      this.lakes = data;
      this.dtTrigger.next();
    });
  }

  ngOnDestroy(): void{
    this.dtTrigger.unsubscribe();
  }

}
