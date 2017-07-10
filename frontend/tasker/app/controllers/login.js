import Ember from 'ember';
import ENV from '../config/environment'

export default Ember.Controller.extend({
  session: Ember.inject.service('session'),

  loginSelected: true,

  actions: {
    login() {
      let username = this.get('login-username');
      let password = this.get('login-password');
      this.get('session').authenticate('authenticator:drf-token-authenticator', username, password).catch((reason) => {
        this.set('error', reason);
      });
    },

    register() {
      let username = this.get('register-username');
      let email = this.get('email');
      let password = this.get('register-password');
      let confirmPassword = this.get('confirm-password');

      Ember.$.ajax({
        url: ENV.host + '/api-register/',
        type: 'POST',
        data: JSON.stringify({
          username: username,
          email: email,
          password: password,
          confirm_password: confirmPassword
        }),
        contentType: 'application/json;charset=utf-8',
        dataType: 'json'
      }).then((/*response*/) => {
        this.set('loginSelected', true);
        this.set('signupComplete', true);
        username = '';
        email = '';
        password = '';
        confirmPassword = '';
      }, (xhr/*, status, error*/) => {
        this.set('error', xhr.responseText);
      });
    },

    switchToLogin() {
      this.set('loginSelected', true);
    },
    switchToRegister() {
      this.set('loginSelected', false);
    },

    highlight() {

    }
  }
});
