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
}
