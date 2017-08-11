import { moduleForComponent, test } from 'ember-qunit';
import hbs from 'htmlbars-inline-precompile';

moduleForComponent('project-name-with-change-name', 'Integration | Component | project name with change name', {
  integration: true
});

test('it renders', function(assert) {

  // Set any properties with this.set('myProperty', 'value');
  // Handle any actions with this.on('myAction', function(val) { ... });

  this.render(hbs`{{project-name-with-change-name}}`);

  assert.equal(this.$().text().trim(), '');

  // Template block usage:
  this.render(hbs`
    {{#project-name-with-change-name}}
      template block text
    {{/project-name-with-change-name}}
  `);

  assert.equal(this.$().text().trim(), 'template block text');
});
