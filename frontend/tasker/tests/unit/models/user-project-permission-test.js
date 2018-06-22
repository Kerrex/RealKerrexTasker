import { moduleForModel, test } from 'ember-qunit';

moduleForModel('user-project-permission', 'Unit | Model | user project permission', {
  // Specify the other units that are required for this test.
  needs: []
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});
