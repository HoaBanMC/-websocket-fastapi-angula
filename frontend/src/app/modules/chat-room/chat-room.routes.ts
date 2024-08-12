import { Routes } from '@angular/router';
import { ListRoomComponent } from './list-room/list-room.component';
import { RoomComponent } from './room/room.component';

export const routes: Routes = [
	{
		path: '',
		component: ListRoomComponent,
	},
	{
		path: ':roomId',
		component: RoomComponent,
	},
];
