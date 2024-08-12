import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import * as env from '../../environments/environment';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
	providedIn: 'root',
})
export class ChatService {
	private socket$!: WebSocketSubject<any>;
	roomId = signal<number>(0);
	userId = signal<string>('unknow');
	public receivedData: MessageData[] = [];

	constructor(private http: HttpClient) {}

	getChatRooms(): Observable<any[]> {
		return this.http.get<any[]>(`${env.apiUrl}/chatrooms`);
	}

	postChatRooms(body: any): Observable<any[]> {
		return this.http.post<any[]>(`${env.apiUrl}/chatrooms`, body);
	}

	getMessages(roomId: number): Observable<any[]> {
		return this.http.get<any[]>(`${env.apiUrl}/chatrooms/${roomId}/messages`);
	}

	public connectWebSocket(roomId: number): void {
		if (!this.socket$ || this.socket$.closed) {
			this.socket$ = webSocket(`${env.webSocketUrl}/${roomId}`);
			this.socket$.subscribe((data: MessageData) => {
				this.receivedData.push(data);
			});
		}
	}

	sendMessage(message: string) {
		this.socket$.next({ message });
	}

	close() {
		this.socket$.complete();
	}
}

export interface MessageData {
	content: string;
	time: string;
	id?: string;
	user_id: string;
}
