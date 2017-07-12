import { test } from 'qunit';
import moduleForAcceptance from 'tasker/tests/helpers/module-for-acceptance';

moduleForAcceptance('Acceptance | login');

test('visiting /login', function(assert) {
  visit('/login');
  andThen(function() {
    assert.equal(currentURL(), '/login');
  });
});

test('logging in', (assert) => {
  visit('/login');
  andThen(function() {
    assert.equal(currentURL(), '/login');
  });

  fillIn('.field-id-login-username', 'goodusername');
  fillIn('.field-id-login-password', 'goodpassword');
  click('#submit-login');

  andThen(() => {
    assert.equal(currentURL(), '/');
  });
});

test('logging in with wrong creds', (assert) => {
  visit('/login');

  andThen(function() {
    assert.equal(currentURL(), '/login');
  });

  fillIn('.field-id-login-username', 'wrongusername');
  fillIn('.field-id-login-password', 'wrongpassword');
  click('#submit-login');

  andThen(() => {
    assert.equal(currentURL(), '/login');
    let $errors = find('#errors').html();
    assert.equal(JSON.parse($errors).status, '400');
  });
});
