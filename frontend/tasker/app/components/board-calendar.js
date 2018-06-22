import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),
  session: Ember.inject.service(),
  eventArray: null,
  self: this,

  hasEditPermission: Ember.computed('store', function() {
    let that = this;
    let token = this.get('session.data').authenticated.token;
    Ember.$.ajax({
      url: ENV.host + '/api-has-permission/',
      type: 'POST',
      headers: {
        'Authorization': 'Token ' + token
      },
      data: that.get('project.id'),
      contentType: 'application/json;charset=utf-8',
      dataType: 'json'
    }).then(function(response) {
      alert(response);
      that.set('hasEditPermission', response == 'True')
    }, function(xhr/*, status, error*/) {
      that.set('hasEditPermission', xhr.status === 200)
    });
  }),

  updateCardDate(that, cardId, startDate, endDate) {
    that.get('store').findRecord('card', cardId).then(function (card) {
      card.set('calendarDateStart', Ember.Date.parse(startDate));
      card.set('calendarDateEnd', Ember.Date.parse(endDate));

      card.save();
      //console.log(`Card ${cardId}, startDate: ${Ember.Date.parse(startDate)}, endDate: ${Ember.Date.parse(endDate)}`);
    });

  },

  prepareEventArray(that) {
    let store = that.get('store');
    let projectId = that.get('project.id');
    store.query('category', {filter: {project_id: projectId}}).then(function (categories) {
      let categoryIds = categories.map(x => x.get('id'));
      that.get('store').query('card', {
        filter: {
          category_id: categoryIds,
          showOnCalendar: true,
        }
      }).then(function (cards) {
        let filteredCards = cards.filter(c => Ember.isPresent(c.get('calendarDateStart'))
          && Ember.isPresent(c.get('calendarDateEnd')));
        let eventArray = filteredCards.map(x => {
          return {
            id: x.get('id'),
            title: x.get('name'),
            start: x.get('calendarDateStart'),
            end: x.get('calendarDateEnd')
          };
        });
        //console.log(eventArray);

        let calendar = Ember.$('#board-calendar-modal-content .modal-body');
        calendar.fullCalendar('removeEvents');
        calendar.fullCalendar('addEventSource', eventArray);
        calendar.fullCalendar('refetchEvents');
      });
    });
  },

  didInsertElement() {
    const that = this;
    this.get('prepareEventArray')(this);
    this.$('#board-calendar-modal-content .modal-body').fullCalendar({
      schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
      droppable: true,
      defaultView: 'agendaWeek',
      editable: true,
      dropAccept: '.not-planned-calendar-event',
      drop: function (date) {
        let object = Ember.$(this);
        let cardId = object.attr('data-attr-id');
        that.get('updateCardDate')(that, cardId, date.format(), date.add(120, 'm').format());
        object.remove();

        that.get('prepareEventArray')(that);
      },
      eventDrop: function (event) {
        let cardId = event.id;
        let startDate = event.start;
        let endDate = event.end;

        that.get('updateCardDate')(that, cardId, startDate, endDate);
      },
      eventResize: function (event) {
        let cardId = event.id;
        let startDate = event.start;
        let endDate = event.end;

        that.get('updateCardDate')(that, cardId, startDate, endDate);
      },
    });

    let modal = this.$('#board-calendar-modal');

    let button = Ember.$(`#${this.get('showButtonId')}`);
    button.click(function () {
      that.sendAction();
      modal.css('display', 'block');
      Ember.$('#board-calendar-modal-content .modal-body').fullCalendar('removeEvents');
      that.get('prepareEventArray')(that);
    });
    window.onclick = function (event) {
      if (event.target == modal) {
        modal.css('display', 'none');
      }
    };
    let closeButton = this.$('#board-calendar-modal .close');
    closeButton.click(function () {
      modal.css('display', 'none');
    })
  }
});
