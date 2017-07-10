import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL,
});

Router.map(function() {
  this.route('login');
/*  this.route('main', {path: "/"});*/
  this.route('projects', function() {
    this.route('new');

    this.route('edit', {
      path: ':project_id/edit'
    });

    this.route('show', {
      path: ':project_id'
    });
  });
  this.route('permissions', function() {
    this.route('new');

    this.route('edit', {
      path: ':permission_id/edit'
    });

    this.route('show', {
      path: ':permission_id'
    });
  });
});

export default Router;
