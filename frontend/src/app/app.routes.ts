import { Routes } from '@angular/router';
import { LoginComponent } from './modules/login/login.component';

export const routes: Routes = [
	{
		path: 'rooms',
		loadChildren: () => import('./modules/chat-room/chat-room.routes').then((m) => m.routes),
	},
	{
		path: 'login',
		component: LoginComponent,
	},
	{
		path: '**',
		redirectTo: 'rooms',
	},
];
