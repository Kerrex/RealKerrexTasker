import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),

  didInsertElement() {
    let store = this.get('store');
    let $this = this.$();
    $this.find('.cardList').sortable({
      connectWith: ".connectedCategory",
      placeholder: "ui-state-highlight",
      cancel: ".ui-state-disabled",
      update: function (event, ui) {
        let cardId = ui.item.attr('data-card-id');
        console.log(`Dragged item has id ${cardId}`);
        let card = store.find('card', cardId).then(function(card) {
          console.log('dupadupa');
          card.set('orderInCategory', 0);
          card.save();
        });
      }
    }).disableSelection();
  },


});
