import Ember from 'ember';
import config from './config/environment';

const Router = Ember.Router.extend({
  location: config.locationType,
  rootURL: config.rootURL,
});

Router.map(function() {
  this.route('login');
  /*  this.route('main', {path: "/"});*/
  this.route('projects', {path: "/"}, function() {
    this.route('new');

    this.route('edit', {
      path: ':project_id/edit'
    });

    this.route('show', {
      path: ':projectId'
    });

    this.route('delete', {
      path: ':project_id/delete'
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
  this.route('categories', function() {
    this.route('new');

    this.route('edit', {
      path: ':category_id/edit'
    });

    this.route('show', {
      path: ':category_id'
    });
  });
  this.route('cards', function() {
    this.route('new');

    this.route('edit', {
      path: ':card_id/edit'
    });

    this.route('show', {
      path: ':card_id'
    });
  });
});

export default Router;
