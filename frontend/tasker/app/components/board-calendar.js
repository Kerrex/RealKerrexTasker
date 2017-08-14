import Ember from 'ember';

export default Ember.Component.extend({

  didInsertElement() {
    const that = this;
    this.$('#board-calendar-modal-content .modal-body').fullCalendar({
      schedulerLicenseKey: 'CC-Attribution-NonCommercial-NoDerivatives',
      droppable: true,
      defaultView: 'agendaWeek',
      editable: true,
      dropAccept: '.not-planned-calendar-event',
      drop: function (date) {
        alert("Dropped on " + date.format());
        Ember.$(this).remove();
      },
    });

    let modal = this.$('#board-calendar-modal');

    let button = Ember.$(`#${this.get('showButtonId')}`);
    button.click(function () {
      that.sendAction();
      modal.css('display', 'block');
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
