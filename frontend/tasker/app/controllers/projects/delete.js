import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    removeProject() {
      let project = this.get('model');
      project.destroyRecord().then(() => {
        this.transitionToRoute('projects.index');
      });
    }
  }
});
