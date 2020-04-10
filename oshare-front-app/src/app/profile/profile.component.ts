import { Component, OnInit } from '@angular/core';
import { PostService } from '../_services/post.service';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { UserService } from '../_services/user.service';
import { ProfileService } from '../_services/profile.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css'],
  providers: [PostService, ProfileService, UserService]
})
export class ProfileComponent implements OnInit {
  form: FormGroup;
  file: File[] = null;
  userURL: string;
  profileURL: string;

  constructor(formbuilder: FormBuilder, private router: Router,
    private userService: UserService, private profileService: ProfileService) {
    this.form = formbuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      password: ['', Validators.required],
      username: ['', Validators.required],
      email: ['']
    })
  }
  get first_name() {
    return this.form.get('first_name');
  }
  get last_name() {
    return this.form.get('last_name');
  }
  get username() {
    return this.form.get('username');
  }
  get password() {
    return this.form.get('password');
  }
  get email() {
    return this.form.get('email');
  }


  ngOnInit(): void {
    if (localStorage.getItem('userToken') == null) {
      alert('Required Login!');
      this.router.navigate(['/search'])
    }
  }

  fileChanged(event) {
    this.file = <File[]>event.target.files;
  }

  OnEditProfile() {
    this.userURL = this.userService.getUserURLById(localStorage.getItem('userId'));
    const formData = new FormData();
    formData.append('user', this.userURL);
    formData.append('first_name', this.form.get('first_name').value);
    formData.append('last_name', this.form.get('last_name').value);
    formData.append('username', this.form.get('username').value);
    formData.append('email', this.form.get('email').value);
    formData.append('password', this.form.get('password').value);

    this.profileService.editProfile(this.form.getRawValue()).subscribe(
      response => {
        this.profileURL = response.url;
        alert('Profile successfully edit!');
      },

      error => {
        console.log(error);
      }
    );
    window.location.reload();
  }
}


