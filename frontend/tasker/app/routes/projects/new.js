import Ember from 'ember';
import SaveModelMixin from 'tasker/mixins/projects/save-model-mixin';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(SaveModelMixin, AuthenticatedRouteMixin, {
  model: function() {
    return this.store.createRecord('project');
  }
});
