import Ember from 'ember';

export default Ember.Controller.extend({
  actions: {
    selectPermission(value) {
      this.store.findRecord('permission', value).then(permission => {
        this.get('project').set('defaultPermission', permission);
      });
    }
  }
});
