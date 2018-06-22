import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  store: Ember.inject.service(),
  session: Ember.inject.service(),
  changeNameDialog: null,
  projectName: Ember.computed.alias('project.name'),

  hasEditPermission: Ember.computed('store', function () {
    let that = this;
    let token = this.get('session.data').authenticated.token;
    Ember.$.ajax({
      url: ENV.host + '/api-has-permission/',
      type: 'POST',
      headers: {
        'Authorization': 'Token ' + token
      },
      data: that.get('project.id'),
      contentType: 'application/json;charset=utf-8',
      dataType: 'json'
    }).then(function (response) {
      that.set('hasEditPermission', response == 'True')
    }, function (xhr/*, status, error*/) {
      that.set('hasEditPermission', xhr.status === 200)
    });
  }),

  didRender() {
    let oldName = this.get('project').get('name');
    let project = this.get('project');
    let dialog = Ember.$("#dialog-form").dialog({
      autoOpen: false,
      height: 100,
      width: 250,
      modal: true,
      buttons: {
        "Apply": function () {
          project.save();
          dialog.dialog('close');
        },
        Cancel: function () {
          project.set('name', oldName);
          dialog.dialog('close');
        }
      },
      close: function () {
      }
    });
    this.set('changeNameDialog', dialog);
  },

  actions: {
    changeName() {
      this.get('project').save();
      this.get('changeNameDialog').dialog('close');
    },
    showDialog() {
      this.get('changeNameDialog').dialog("open");
    }
  }

});
