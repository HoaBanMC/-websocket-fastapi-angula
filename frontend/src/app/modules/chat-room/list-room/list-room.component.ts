import { Component, OnInit } from '@angular/core';
import { ChatService } from '../../../services/chat.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
	selector: 'app-list-room',
	standalone: true,
	imports: [FormsModule],
	templateUrl: './list-room.component.html',
	styleUrl: './list-room.component.scss',
})
export class ListRoomComponent implements OnInit {
	isShowPopup = false;
	roomName: string = '';
	listChatrooms: any[] = [];

	constructor(
		private chatService: ChatService,
		private router: Router,
	) {}

	ngOnInit() {
		this.getChatRooms();
	}

	getChatRooms() {
		this.chatService.getChatRooms().subscribe((data) => {
			console.log(data);
			this.listChatrooms = data;
		});
	}

	onCreateRoom() {
		this.isShowPopup = true;
	}

	onJoinRoom(roomId: number) {
		this.router.navigate(['/rooms', roomId]);
	}

	userAction(event: boolean) {
		if (event) {
			if (this.roomName !== '') {
				this.chatService.postChatRooms({ name: this.roomName }).subscribe((res: any) => {
					console.log(res);
					this.isShowPopup = false;
					this.router.navigate(['/rooms', res.id]);
				});
			}
		} else {
			this.roomName = '';
			this.isShowPopup = false;
		}
	}
}
