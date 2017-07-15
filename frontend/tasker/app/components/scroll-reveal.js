import Ember from 'ember';

const ScrollReveal = Ember.Component.extend({
  className: Ember.computed('attachTo', function () {
    return `\".${this.get('attachTo')}\"`
  }),

  didInsertElement() {
    //TODO FIX THIS COMPONENT
  }
});

ScrollReveal.reopenClass({
  positionalParams: ['attachTo',]
});

export default ScrollReveal;
