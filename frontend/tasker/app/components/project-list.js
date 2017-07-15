import Ember from 'ember';

export default Ember.Component.extend({
  didInsertElement() {
    let $this = this.$();
    $this.tooltip({
      position: {
        my: "center bottom-20",
        at: "center top",
        using: function (position, feedback) {
          $(this).css(position);
          $("<div>")
            .addClass("arrow")
            .addClass(feedback.vertical)
            .addClass(feedback.horizontal)
            .appendTo(this);
        },
      },
      content: function () {
        return this.getAttribute('title');
      }
    });
  }
});
