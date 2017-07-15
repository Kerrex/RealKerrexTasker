import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement() {
    let $this = this.$();
    $this.find('.cardList').sortable({
      connectWith: ".connectedCategory",
      placeholder: "ui-state-highlight",
      cancel: ".ui-state-disabled"
    }).disableSelection();
  },

});
