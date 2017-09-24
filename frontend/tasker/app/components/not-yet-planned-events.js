import Ember from 'ember';

export default Ember.Component.extend({
  store: Ember.inject.service(),

  didInsertElement() {
    let store = this.get('store');
    let that = this;
    let projectId = this.get('project.id');
    store.query('category', {filter: {project_id: projectId}}).then(function (categories) {
      let categoryIds = categories.map(x => x.get('id'));
      let cards = that.get('store').query('card', {
        filter: {
          category_id: categoryIds,
          showOnCalendar: true,
          calendarDateStart: null
        }
      }).then(function (cards) {
        //console.log(cards);
        that.set('cards', cards);
      });
    });
  },

  didRender() {
    Ember.$('.external-events').each(function () {
      //console.log(this);
      Ember.$(this).data('event', {
        title: Ember.$.trim(Ember.$(this).text()), // use the element's text as the event title
        stick: true // maintain when user navigates (see docs on the renderEvent method)
      });

      // make the event draggable using jQuery UI
      Ember.$(this).draggable({
        zIndex: 999,
        revert: true,      // will cause the event to go back to its
        revertDuration: 0  //  original position after the drag
      });
    });
  }
});
