import Ember from 'ember';
import SaveModelMixin from 'tasker/mixins/projects/save-model-mixin';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(SaveModelMixin, AuthenticatedRouteMixin, {

  model(params) {
    return Ember.RSVP.hash({
      project: this.get('store').findRecord('project', params.project_id),
      permissions: this.get('store').findAll('permission')
    });
  },

  setupController(controller, model) {
    this._super(...arguments);
    Ember.set(controller, 'project', model.project);
    Ember.set(controller, 'permissions', model.permissions);
  },
});
