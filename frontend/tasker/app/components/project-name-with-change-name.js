import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),
  changeNameDialog: null,
  projectName: Ember.computed.alias('project.name'),

  didInsertElement() {
    let oldName = this.get('project').get('name');
    let project = this.get('project');
    let actions = this.get('actions');
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
