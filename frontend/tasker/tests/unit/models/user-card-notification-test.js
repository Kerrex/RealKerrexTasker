import { moduleForModel, test } from 'ember-qunit';

moduleForModel('user-card-notification', 'Unit | Model | user card notification', {
  // Specify the other units that are required for this test.
  needs: ['model:user', 'model:card']
});

test('it exists', function(assert) {
  let model = this.subject();
  // let store = this.store();
  assert.ok(!!model);
});
