import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('fancy-text-field', 'Integration | Component | fancy text field', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{fancy-text-field class="login" placeholder="Placeholder" type="text"}}`);

  assert.equal(this.$().text().trim(), 'Placeholder*');

});
