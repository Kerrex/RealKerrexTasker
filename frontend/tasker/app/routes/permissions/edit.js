import Ember from 'ember';
import SaveModelMixin from 'tasker/mixins/permissions/save-model-mixin';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(SaveModelMixin, AuthenticatedRouteMixin, {
  model() {
    return Ember.RSVP.hash({
      project: this.store.createRecord('project'),
      permissions: this.store.findAll('permission')
    });
  }
});
