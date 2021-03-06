import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {baseurl} from '../MockComments';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private httpOptions: any;

  public username: string;

  baseurl = baseurl;
  // baseurl = "http://127.0.0.1:8000";
  // baseUrl: 'http://ec2-54-183-253-130.us-west-1.compute.amazonaws.com:8000';
  httpHeaders = new HttpHeaders({ 'Content-Type': 'application/json' });

  

  constructor(private httpClient: HttpClient, private router: Router) {

   }

  registerUser(userData): Observable<any> {
    return this.httpClient.post<any>(this.baseurl + '/register/', userData);
  }

  loginUser(userData): Observable<any> {
    return this.httpClient.post(this.baseurl + '/auth/', userData, { headers: this.httpHeaders });
  }

  getCurrentUser(){
    if(localStorage.getItem('userToken')!=null){
      var authorize_header = new HttpHeaders({'Authorization':'Token '+ localStorage.getItem('userToken')})
      return this.httpClient.get<any>(this.baseurl + '/register/get_current_user/', {headers: authorize_header});
    }
    return null;
  }

  getCurrentUserId(){
    if(localStorage.getItem('userToken')!=null){
      var authorize_header = new HttpHeaders({'Authorization':'Token '+ localStorage.getItem('userToken')})
      this.httpClient.get<any>(this.baseurl + '/register/get_current_userid/', {headers: authorize_header}).subscribe(
        response=>{
          return response.id;
        }, error=>{
          return null;
        }
      )
    }
    return null;
  }

  getUserURLById(id) {
    return this.baseurl + '/register/' + id + '/';
  }

  getUserObjectById(id): Observable<any> {
    return this.httpClient.get(this.getUserURLById(id));
  }

  getUserObjectByURL(url: string): Observable<any> {
    return this.httpClient.get(url);
  }

  getUserByUsername(username: string): Observable<any> {
    return this.httpClient.get<any>(this.baseurl + '/register/get_by_username/?username=' + username);
  }


}
