import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
	selector: 'app-login',
	standalone: true,
	imports: [CommonModule, FormsModule, ReactiveFormsModule],
	templateUrl: './login.component.html',
	styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
	loginForm!: FormGroup;

	constructor(private router: Router) {}

	ngOnInit(): void {
		this.loginForm = new FormGroup({
			username: new FormControl('', Validators.required),
			password: new FormControl('', Validators.required),
		});
	}

	login() {
		console.log(this.loginForm.value);
		if (this.loginForm.valid) {
			if (this.loginForm.value.username === 'samlv' && this.loginForm.value.password === '123123') {
				localStorage.setItem('token', 'true');
				this.router.navigate(['/']);
			} else {
				console.log('Wrong info!');
			}
		}
	}
}
