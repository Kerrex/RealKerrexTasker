import Ember from 'ember';

const FancyTextField = Ember.Component.extend({
  fieldId: Ember.computed('id', function () {
    return `field-id-${this.get('id')}`;
  }),

  didInsertElement() {
    let $this = this.$().find('input');
    let _this = this;

    $this.on('keyup blur focus', function (e) {
      let value = _this.get('value');
      let label = $this.prev('label');
      if (e.type === 'keyup') {
        if (value === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
      } else if (e.type === 'blur') {
        if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.removeClass('highlight');
        }
      } else if (e.type === 'focus') {

        if ($this.val() === '') {
          label.removeClass('highlight');
        }
        else if ($this.val() !== '') {
          label.addClass('highlight');
        }
      }
    });
  }
});

FancyTextField.reopenClass({
  positionalParams: ['value', 'placeholder', 'inputType', 'id'],
});

export default FancyTextField;


