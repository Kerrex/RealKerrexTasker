import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),
  cardDetailsDialogId: Ember.computed('card', function () {
    return `card-details-dialog-${this.get('card').get('id')}`;
  }),
  editingName: false,
  editingDescription: false,
  editCardDialog: null,
  isDescriptionEmpty: false,
  oldName: null,

  cardName: Ember.computed('card', {
    get (key) {
      return this.get('card').get('name');
    },
    set (key, value) {
      this.get('card').set('name', value);
    }
  }),

  cardDescription: Ember.computed('card', {
    get (key) {
      return this.get('card').get('description');
    },
    set (key, value) {
      this.get('card').set('description', value);
    }
  }),

  didInsertElement() {
    this.set('oldName', this.get('cardName'));
    this.set('isDescriptionEmpty', Ember.isBlank(this.get('card').get('description')));
    let that = this;
    let dialog = Ember.$(`#${this.get("cardDetailsDialogId")}`).dialog({
      autoOpen: false,
      height: 100,
      width: 250,
      closeOnEscape: false,
      modal: true,
      buttons: {
        "Close": function () {
          dialog.dialog('close');
        },
      },
      close: function () {
        that.send('disableEditName');
        that.send('disableEditDescription');
      }
    });
    this.set('editCardDialog', dialog);
  },

  actions: {
    editCard() {
      this.get('editCardDialog').dialog("close");
    },
    showCardEditDialog() {
      this.get('editCardDialog').dialog("open");
    },
    enableEditName() {
      this.set('editingName', true);
      this.$("#name-edit-input").focus();
    },
    disableEditName() {
      this.set('editingName', false);
      this.send('saveCard');
    },
    enableEditDescription() {
      this.set('editingDescription', true);
    },
    disableEditDescription() {
      this.set('editingDescription', false);
      this.send('saveCard');
      this.send('setIsDescriptionEmpty');
    },
    saveCard() {
      let name = this.get('card.name');
      if (!Ember.isBlank(name) && name.length <= 25) {
        console.log(name);
        this.get('card').save();
        this.set('oldName', name);
      } else {
        this.set('cardName', this.get('oldName'));
      }
    },
    setIsDescriptionEmpty() {
      let description = this.get('cardDescription');
      console.log(description);
      if (Ember.isBlank(description)) {
        this.set('isDescriptionEmpty', true);
      } else {
        this.set('isDescriptionEmpty', false);
      }
    }
  }
})
;
