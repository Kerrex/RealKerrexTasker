import Ember from 'ember';
import AuthenticatedRouteMixin from 'ember-simple-auth/mixins/authenticated-route-mixin';

export default Ember.Route.extend(AuthenticatedRouteMixin, {
  model(params) {
    let projectId = params.projectId;
    let categories = this.store.query('category', {filter: {project_id: projectId}});
    let project = this.store.find('project', projectId);
    return Ember.RSVP.hash({
      categories: categories,
      project: project,
    });
  },
  setupController(controller, model) {
    this._super(...arguments);
    Ember.set(controller, 'categories', model.categories);
    Ember.set(controller, 'project', model.project);
  },
});
