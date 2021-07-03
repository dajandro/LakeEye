import { Component, OnInit, Input, ElementRef, ViewChild } from '@angular/core';
import { ApiService } from '../api.service';
import * as chroma from 'chroma-js';

const range = (start:number, stop:number, step = 1) =>
  Array(Math.ceil((stop - start) / step)).fill(start).map((x, y) => x + y * step);

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit {

  @Input('idL') lakeID: any = "";
  @Input('idM') measID: any = 1;

  Graph: any;
  data: any;
  dataG: Array<any> = [];

  chart: any;

  public graph = {
    data: [
      {x:10, y:10, type:'scatter'}
    ],
    layout: {title: 'Plot 2'}
  }

  constructor(private apiService: ApiService, private GraphContainer: ElementRef) { }

  ngOnInit(): void {

    // Get Lake Information
    this.apiService.getLakeMeasurements(this.lakeID, this.measID).subscribe(data => {
      this.data = data;
      //this.data = this.data[0];
      console.log(this.data);

      var mName = "";
      var lats = [];
      var lons = [];
      var vals = [];
      var cols = [];

      for(var i = 0; i<this.data.length; i++){
        var obj = this.data[i];
        var dataG_i=['', obj.LON, obj.LAT, obj.VAL_QTY, 0.001]
        this.dataG.push(dataG_i);
        lats.push(obj.LAT);
        lons.push(obj.LON);
        vals.push(obj.VAL_QTY);
        mName = obj.MEASUREMENT;
      }

      console.log(this.dataG);

      var cS = chroma.scale(['yellow', 'lightgreen', '008ae5'])
        .domain([Math.min(...vals), Math.max(...vals)]);
        
      for(var i = 0; i<vals.length; i++){
        cols.push(cS(i).hex());
      }

      console.log(cols);

      this.chart = {
        title: mName,
        type: 'BubbleChart',
        data: this.dataG,
        options: {
          tooltip: {
            showColorCode: true
          },
          colors: cols,
          sizeAxis: {minValue:0, maxValue:1},
          width: 500,
          height: 500
        }
      }
    });   
  }

}
