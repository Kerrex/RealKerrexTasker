import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),
  tagName: "tr",



  actions: {
    selectUserPermission(value) {
      this.get('store').findRecord('permission', value).then(permission => {
        this.get('userPermission').set('permission', permission);
      });
    },
  }
});
