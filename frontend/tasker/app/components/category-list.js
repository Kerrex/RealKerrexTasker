import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),
  addNewCategoryDialog: null,

  didInsertElement() {
    let store = this.get('store');
    let $this = this.$();
    $this.find('.cardList').sortable({
      connectWith: ".connectedCategory",
      placeholder: "ui-state-highlight",
      cancel: ".ui-state-disabled",
      dropOnEmpty: true,
      update: function (event, ui) {
        let cardId = ui.item.find('li').attr('data-card-id');
        console.log(`Dragged item has id ${cardId}`);

        let card = store.find('card', cardId).then(function (card) {
          $this.find('.ember-list-element').each(function (cat_index) {

            let categoryId = Ember.$(this).attr('data-category-id');
            Ember.$(this).find('.cardList li').each(function (card_index) {

              if (Ember.$(this).attr('data-card-id') === cardId) {
                let category = store.find('category', categoryId).then(function (category) {
                  if (card.get('category') !== category
                    || card.get('orderInCategory') !== card_index) {
                    card.set('category', category);
                    card.set('orderInCategory', card_index);
                    console.log("Dragged to category " + category.get('id'));
                    console.log("Order in category: " + card_index);
                    card.save();
                  }
                });
              }
            })
          });
        });
      }
    }).disableSelection();

    let dialog = Ember.$("#addNewCategoryDialog").dialog({
      autoOpen: false,
      height: 100,
      width: 250,
      modal: true,
      buttons: {
        "Apply": function () {
          let newCategory = that.get('store').createRecord('category', {
            name: that.get('newCategoryName'),
            project: that.get('project')
          });
          newCategory.save();
          //location.reload();
          dialog.dialog('close');
        },
        Cancel: function () {
          dialog.dialog('close');
        }
      },
      close: function () {
      }
    });
    this.set('addNewCategoryDialog', dialog);
  },
  actions: {
    showAddNewCategoryDialog() {
      this.get('addNewCategoryDialog').dialog("open");
    },

    addNewCategory() {
      let newCategory = this.get('store').createRecord('category', {
        name: this.get('newCategoryName'),
        project: this.get('project')
      });
      newCategory.save();
      location.reload();
      this.get('addNewCategoryDialog').dialog('close');
    },
    reloadModel() {
      this.sendAction();
    }
  }


});
