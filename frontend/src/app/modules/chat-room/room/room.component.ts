import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../../services/chat.service';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { CommonModule } from '@angular/common';

@Component({
	selector: 'app-room',
	standalone: true,
	imports: [CommonModule, FormsModule],
	templateUrl: './room.component.html',
	styleUrl: './room.component.scss',
})
export class RoomComponent implements OnInit {
	message = '';
	subscription = new Subscription();
	showRoomChat = true;

	constructor(
		public chatService: ChatService,
		private activatedRoute: ActivatedRoute,
	) {}

	ngOnInit(): void {
		this.subscription.add(
			this.activatedRoute.params.subscribe((params) => {
				if (params['roomId']) {
					this.chatService.roomId.set(params['roomId']);
					if (this.chatService.roomId() !== 0) {
						this.chatService.connectWebSocket(this.chatService.roomId());
						this.chatService.getMessages(this.chatService.roomId()).subscribe((res: any) => {
							this.chatService.receivedData = res;
							console.log(res);
							
						});
					}
				}
			}),
		);
	}

	onShowChat() {
		this.showRoomChat = !this.showRoomChat;
	}

	sendMessage(message: string) {
		if (message !== '') {
			this.chatService.sendMessage(message);
		}
	}

	ngOnDestroy() {
		this.chatService.close();
	}
}
