import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement() {
    let $this = this.$();
    $this.sortable({
      connectWith: ".connectedCategory"
    }).disableSelection();
  },

});
