import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { DataTablesModule } from 'angular-datatables';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { HomeComponent } from './home/home.component';
import { HelpComponent } from './help/help.component';
import { ApiService } from './api.service';
import { LakesListComponent } from './lakes-list/lakes-list.component';
import { LakeDetailComponent } from './lake-detail/lake-detail.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { GoogleMapsModule } from '@angular/google-maps';
import { ChartComponent } from './chart/chart.component';
import { GoogleChartsModule } from 'angular-google-charts';

//import * as PlotlyJS from 'plotly.js/dist/plotly.js';
//import  * as PlotlyJS from '@types/plotly.js';
//import * as PlotlyJS from 'plotly.js/dist/plotly.js';
//import * as PlotlyJS from "plotly.js";
//import { PlotlyModule } from 'angular-plotly.js';
//PlotlyModule.plotlyjs = PlotlyJS;


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    HomeComponent,
    HelpComponent,
    LakesListComponent,
    LakeDetailComponent,
    ChartComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    DataTablesModule,
    NgbModule,
    GoogleMapsModule,
    GoogleChartsModule
    //PlotlyModule
  ],
  providers: [
    ApiService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
