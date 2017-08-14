import Ember from 'ember';
import moment from "moment";

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
  oldShowOnCalendar: null,
  showOnCalendar: Ember.computed('card',  {
    get(key) {
      return this.get('card.showOnCalendar');
    },
    set(key, value) {
      this.get('card').set('showOnCalendar', value);
      this.get('card').save();
      return value;
    }
  }),

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

  dateModifiedFormatted: Ember.computed('card', function () {
    return moment(this.get('card').get('lastModified')).format('DD/MM/YYYY hh:mm');
  }),

  dateCreatedFormatted: Ember.computed('card', function () {
    return moment(this.get('card').get('dateCreated')).format('DD/MM/YYYY hh:mm');
  }),

  didInsertElement() {
    this.set('oldName', this.get('cardName'));
    this.set('showOnCalendar', this.get('card.showOnCalendar'));
    this.set('isDescriptionEmpty', Ember.isBlank(this.get('card').get('description')));

    let that = this;
    let dialog = Ember.$(`#${this.get("cardDetailsDialogId")}`).dialog({
      autoOpen: false,
      height: 400,
      width: 550,
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
        that.sendAction();
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
