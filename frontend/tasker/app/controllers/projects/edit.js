import Ember from 'ember';

export default Ember.Controller.extend({

  actions: {
    selectPermission(value) {
      this.store.findRecord('permission', value).then(permission => {
        //console.log(permission);
        this.get('project').set('defaultPermission', permission);
      });
    },

    selectUserPermission(userPermission, value) {
      //console.log(userPermission);
      //console.log(value);
      /*this.store.findRecord('permission', value).then(permission => {
        userPermission.set('permission', permission);
      });*/
    },
    openAddPermissionModal() {
      let modal = Ember.$('#add-edit-permission-modal');
      modal.css('display', 'block');
    },
    addNewPermission() {
      let usernameOrEmail = this.get('permissionUsernameOrEmail');
      this.store.query('user', {
        filter: {
          usernameOrEmail: usernameOrEmail
        }
      }).then(user => {
        if (!Ember.isEmpty(user)) {
          //console.log(user.get('firstObject'));
          let newUserPermission = this.store.createRecord('user-project-permission', {
            user: user.get('firstObject'),
            project: this.get('project')
          });
          newUserPermission.save();
          if (!Ember.testing) {
            window.location.reload();
          }
        } else {
          alert("User not found!");
        }
      });
    },
    removeProject() {
      let answer = confirm('Are you sure you want to DELETE this project COMPLETELY?');
      if (answer) {
        this.get('project').deleteRecord();
        this.get('project').save();
        this.transitionToRoute('projects.index');
      }
    }
  }
});
