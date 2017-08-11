import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),

  cards: Ember.computed('category', function () {
    let categoryId = this.get('category').get('id');
    return this.get('store').query('card', {filter: {category_id: categoryId}});
  }),

  categoryClass: Ember.computed('category', function () {
    return `category-id-${this.get('category').get('id')}`;
  }),

  insertElementDialogId: Ember.computed('category', function () {
    return `insert-card-dialog-form-${this.get('category').get('id')}`;
  }),

  addNewCardDialog: null,

  didInsertElement() {
    let category = this.get('category');
    let that = this;
    let store = this.get('store');
    console.log(this.get('insertElementDialogId'));
    let dialog = Ember.$("#" + this.get('insertElementDialogId')).dialog({
      autoOpen: false,
      height: 100,
      width: 250,
      modal: true,
      buttons: {
        "Apply": function () {
          let newCard = store.createRecord('card', {
            name: that.get('newCardName'),
            orderInCategory: 0,
            category: category,
            description: ''
          });
          newCard.save();
          dialog.dialog('close');
        },
        Cancel: function () {
          dialog.dialog('close');
        }
      },
      close: function () {
      }
    });
    this.set('addNewCardDialog', dialog);
  },

  actions: {
    showAddNewCardDialog() {
      this.get('addNewCardDialog').dialog('open');
    },

    insertNewCard() {
      let newCard = this.get('store').createRecord('card', {
        name: this.get('newCardName'),
        orderInCategory: 0,
        category: this.get('category'),
        description: ''
      });
      newCard.save();
      location.reload();
    }
  }
});
