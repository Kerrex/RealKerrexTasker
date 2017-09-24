import Ember from 'ember';

export default Ember.Mixin.create({
  actions: {
    save: function () {
      var route = this;
      this.currentModel.project.save().then(function () {
        if (route.currentModel.userPermissions) {
          route.currentModel.userPermissions.forEach(permission => {
            permission.save();
          });
        }
        route.transitionTo('projects');
      }, function () {
        //console.log('Failed to save the model');
      });
    },

    /*willTransition() {
      this._super(...arguments);
      const record = this.controller.get('model');
      record.rollbackAttributes();
    },*/
  },

});
