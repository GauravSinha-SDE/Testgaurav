import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private apiUrl = 'http://127.0.0.1:5000/chat';
  constructor(private http: HttpClient) {}
  sendQuery(query: string): Observable<any> {
    return this.http.post<any>(this.apiUrl, { query });
  }
}
