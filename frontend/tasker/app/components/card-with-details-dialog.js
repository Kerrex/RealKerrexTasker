import Ember from 'ember';
import moment from "moment";

export default Ember.Component.extend({
  dateFormat: 'DD/MM/YYYY HH:mm',
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
  priorities: Ember.computed('store', function () {
    return this.get('store').findAll('priority')
  }),

  notifications: Ember.computed('store', function () {
    return this.get('store').query('userCardNotification', {filter: {card_id: this.get('card.id')}})
  }),

  priorityClass: Ember.computed('card', function () {
    let priorityId = this.get('priorityId');
    if (priorityId === '1') {
      return 'low-priority';
    } else if (priorityId === '2') {
      return 'medium-priority';
    } else if (priorityId === '3') {
      return 'high-priority';
    } else {
      return '';
    }
  }),

  priorityId: Ember.computed('card', function () {
    return this.get('card.priority.id');
  }),

  showOnCalendar: Ember.computed('card', {
    get() {
      return this.get('card.showOnCalendar');
    },
    set(key, value) {
      this.get('card').set('showOnCalendar', value);
      this.get('card').save();
      return value;
    }
  }),

  cardName: Ember.computed('card', {
    get() {
      return this.get('card').get('name');
    },
    set(key, value) {
      this.get('card').set('name', value);
    }
  }),

  cardDescription: Ember.computed('card', {
    get() {
      return this.get('card').get('description');
    },
    set(key, value) {
      this.get('card').set('description', value);
    }
  }),

  dateModifiedFormatted: Ember.computed('card', function () {
    return moment(this.get('card').get('lastModified')).format(this.get('dateFormat'));
  }),

  dateCreatedFormatted: Ember.computed('card', function () {
    return moment(this.get('card').get('dateCreated')).format(this.get('dateFormat'));
  }),

  calendarDateStartFormatted: Ember.computed('card', function () {
    return moment(this.get('card.calendarDateStart')).format(this.get('dateFormat'));
  }),

  calendarDateEndFormatted: Ember.computed('card', function() {
    return moment(this.get('card.calendarDateEnd')).format(this.get('dateFormat'));
  }),

  prepareCardDialog(self) {
    self.get('store').query('userCardNotification', {filter: {card_id: self.get('card.id')}}).then(notifications => {
      self.set('oldName', self.get('cardName'));
      self.set('oldShowOnCalendar', self.get('card.showOnCalendar'));
      self.set('isDescriptionEmpty', Ember.isBlank(self.get('card').get('description')));
      let that = self;
      let notification = notifications.toArray()[0];
      //console.log("dupa" + notifications);
      let notificationButton = Ember.isEmpty(notifications)
        ? {
          text: "Notify me about this event",
          "class": "notify-me-button btn btn-success",
          click: function () {
            let minutesInStr = prompt("Please enter number of minutes to notify before");
            let minutes = parseInt(minutesInStr);
            if (isNaN(minutes)) {
              alert("Incorrect value! Please use numbers only!");
              return;
            }
            that.get('store').query('userCardNotification', {
              filter: {
                card_id: that.get('card.id')
              }
            }).then(notification => {
              if (Ember.isEmpty(notification)) {
                let newNotification = that.get('store').createRecord('userCardNotification', {
                  card: that.get('card'),
                  minutesBeforeStart: minutes
                });
                newNotification.save();
                that.get('notifications');
                window.location.reload();
                that.rerender();
              } else {
                notification.toArray()[0].set('minutesBeforeStart', minutes);
                notification.toArray()[0].save();
                that.get('notifications');
                window.location.reload();
              }
            })
          }
        }
        : {
          text: "Click here to disable notification (" + notification.get('minutesBeforeStart') + " minutes before start)",
          "class": "unnotify-me-button btn btn-primary",
          click: function () {
            notification.deleteRecord();
            notification.save();
            that.rerender();
          }
        };

      let dialog = Ember.$(`#${self.get("cardDetailsDialogId")}`).dialog({
        autoOpen: false,
        height: 400,
        width: 550,
        closeOnEscape: false,
        modal: true,
        buttons: [
          notificationButton,
          {
            text: "Close",
            "class": "btn btn-default",
            click: function () {
              dialog.dialog('close');
            }
          }
        ],
        close: function () {
          that.send('disableEditName');
          that.send('disableEditDescription');
          that.sendAction();
        }
      });
      self.set('editCardDialog', dialog);

    });
  },

  didRender() {
    this.get('prepareCardDialog')(this);
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
      this.get('card').set('calendarDateStart', moment.utc(this.get('card.calendarDateStart')).valueOf());
      this.get('card').set('calendarDateEnd', moment.utc(this.get('card.calendarDateEnd')).valueOf());
      if (Ember.isEmpty(this.get('priorityId'))) {
        this.get('card').set('priority', null);
      } else {
        this.get('store').find('priority', this.get('priorityId')).then(priority => {
          this.get('card').set('priority', priority);
          this.get('card').save();
          //console.log(priority);
        });
      }

      let name = this.get('card.name');
      if (!Ember.isBlank(name) && name.length <= 25) {
        //console.log(name);
        this.get('card').save();
        this.set('oldName', name);
      } else {
        this.set('cardName', this.get('oldName'));
      }

      if (!!this.get('oldShowOnCalendar') && !this.get('card.showOnCalendar')) {
        this.get('card').set('calendarDateStart', '');
        this.get('card').set('calendarDateEnd', '');
        this.get('card').save();
      }

      // Must be last in saveCard()
      if (!this.get('oldShowOnCalendar') && !!this.get('card.showOnCalendar')) {
        window.location.reload();
      }
    },
    setIsDescriptionEmpty() {
      let description = this.get('cardDescription');
      //console.log(description);
      if (Ember.isBlank(description)) {
        this.set('isDescriptionEmpty', true);
      } else {
        this.set('isDescriptionEmpty', false);
      }
    }
  }
})
;
