import { Routes } from '@angular/router';

export const routes: Routes = [
	{
		path: 'rooms',
		loadChildren: () => import('./modules/chat-room/chat-room.routes').then((m) => m.routes),
	},
];
