import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('not-yet-planned-events', 'Integration | Component | not yet planned events', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{not-yet-planned-events}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#not-yet-planned-events}}
      template block text
    {{/not-yet-planned-events}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
