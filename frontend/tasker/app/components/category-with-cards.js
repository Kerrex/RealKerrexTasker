import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),

  cards: Ember.computed('category', function () {
    let categoryId = this.get('category').get('id');
    return this.get('store').query('card', {filter: {category_id: categoryId}});
  }),

  categoryClass: Ember.computed('category', function () {
    return `category-id-${this.get('category').get('id')}`;
  })
});
