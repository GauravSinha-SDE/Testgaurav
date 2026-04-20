import { Component } from '@angular/core';
import { ChatService } from '../chat.service';

@Component({
  selector: 'app-chatbot',
  templateUrl: './chatbot.component.html',
  styleUrls: ['./chatbot.component.css']
})
export class ChatbotComponent {
  userQuery: string = '';
  response: string = '';
  loading: boolean = false;

  constructor(private chatService: ChatService) {}

  sendQuery() {
    if (!this.userQuery.trim()) {
      this.response = 'Please type a travel query.';
      return;
    }
    this.loading = true;
    this.response = 'Thinking...';
    this.chatService.sendQuery(this.userQuery).subscribe({
      next: (res) => {
        this.loading = false;
        this.response = res.trip_plan || 'No response.';
      },
      error: (err) => {
        this.loading = false;
        this.response = 'Network error: ' + err.message;
      }
    });
  }
}
