import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('scroll-reveal', 'Integration | Component | scroll reveal', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{scroll-reveal}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#scroll-reveal}}
      template block text
    {{/scroll-reveal}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
