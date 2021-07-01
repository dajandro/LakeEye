import { Component, OnInit, Input, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';

import { MapInfoWindow, MapMarker, GoogleMap } from '@angular/google-maps';

@Component({
  selector: 'app-lake-detail',
  templateUrl: './lake-detail.component.html',
  styleUrls: ['./lake-detail.component.css']
})
export class LakeDetailComponent implements OnInit {

  @Input('id') lakeID: any = ""; 
  
  info: any;
  r1: number = 0;
  r2: number = 0;

  lat_center: number = 0;
  lon_center: number = 0;

  value: number = 3.5;

  markers : Array<any> = [];
  infoContent = '';

  constructor(private route: ActivatedRoute, private apiService: ApiService) { }

  ngOnInit(): void {
    this.lakeID = this.route.snapshot.paramMap.get('id');

    // Get Lake Information
    this.apiService.getLakeInfo(this.lakeID).subscribe(data => {
      this.info = data;
      this.info = this.info[0];
      
      this.lat_center = (this.info.MX_LAT+this.info.MN_LAT)/2;
      this.lon_center = (this.info.MX_LON+this.info.MN_LON)/2;
    });

    // Get Rank 1
    this.apiService.getLakeRank(this.lakeID, 1).subscribe(data => {
      var t : any;
      t = data;
      this.r1 = t[0].VAL_NUM;
    })

    // Get Rank 1
    this.apiService.getLakeRank(this.lakeID, 2).subscribe(data => {
      var t : any;
      t = data;
      this.r2 = t[0].VAL_NUM;
    })

    // Get TSI
    this.apiService.getLakeParam(this.lakeID, 1).subscribe(data => {
      var t : any;
      t = data;
      var tsi = t[0].VAL_NUM;
      // Create Marker
      var marker = {
        position: {
          lat: this.lat_center  + 0.02,
          lng: this.lon_center
        },
        label: {
          color: 'blue',
          text: 'TSI: ' + tsi.toFixed(2),
          fontSize: '20px'
        },
        title: 'Trophic State Index',
        info: 'Trophic State Index',
        //options: {animation: google.maps.Animation.BOUNCE}
      }
      this.markers.push(marker);
      //console.log(this.markers);
    })

    // Get Turbidity
    this.apiService.getLakeParam(this.lakeID, 2).subscribe(data => {
      var t : any;
      t = data;
      var tur = t[0].VAL_NUM;
      // Create Marker
      var marker = {
        position: {
          lat: this.lat_center,
          lng: this.lon_center
        },
        label: {
          color: 'red',
          text: 'TUR: ' + tur.toFixed(2),
          fontSize: '20px'
        },
        title: 'Turbidity',
        info: 'Turbidity',
        /*
        options: {
          icon: 'https://developers.google.com/maps/documentation/javascript/examples/full/images/info-i_maps.png'
        }*/
      }
      this.markers.push(marker);
      //console.log(this.markers);
    })

    // Get Temperature
    this.apiService.getLakeParam(this.lakeID, 3).subscribe(data => {
      var t : any;
      t = data;
      var tem = t[0].VAL_NUM;
      // Create Marker
      var marker = {
        position: {
          lat: this.lat_center - 0.02,
          lng: this.lon_center
        },
        label: {
          color: 'green',
          text: tem.toFixed(2) + ' °C',
          fontSize: '20px'
        },
        title: 'Temperature',
        info: 'Temperature',
        //options: {animation: google.maps.Animation.BOUNCE}
      }
      this.markers.push(marker);
    })

  }

}
