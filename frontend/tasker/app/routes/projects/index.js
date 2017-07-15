import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';
import UnauthenticatedRouteMixin from 'ember-simple-auth/mixins/unauthenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  actions: {
    remove: function (model) {
      if (confirm('Are you sure?')) {
        model.destroyRecord();
      }
    },

    didTransition() {

    }
  },
  model: function () {
    return this.store.findAll('project');

  },
});
