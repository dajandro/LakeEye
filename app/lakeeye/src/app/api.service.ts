import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  apiURL = 'http://localhost:8090/api'

  constructor(private http: HttpClient) {}

  getLakesRank(){
    return this.http.get(`${this.apiURL}/lakesRank`);
  }

  getLakeInfo(id: string){
    return this.http.get(`${this.apiURL}/lakes/${id}`);
  }

  getLakeRank(idL:string, idR:number){
    return this.http.get(`${this.apiURL}/lakes/${idL}/rank/${idR}`);
  }

  getLakeParam(idL:string, idP:number){
    return this.http.get(`${this.apiURL}/lakes/${idL}/parameter/${idP}`);
  }

  getLakeMeasurements(idL: string, idM: number){
    return this.http.get(`${this.apiURL}/lakes/${idL}/measurement/${idM}`);
  }
}
