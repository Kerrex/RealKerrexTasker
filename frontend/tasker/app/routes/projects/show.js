import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  model(params) {
    let projectId = params.projectId;
    let categories = this.store.query('category', {filter: {project_id: projectId}})
    return categories
  },
});
