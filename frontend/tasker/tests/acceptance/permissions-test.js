import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;
var originalConfirm;
var confirmCalledWith;

module('Acceptance: Permission', {
  beforeEach: function() {
    application = startApp();
    originalConfirm = window.confirm;
    window.confirm = function() {
      confirmCalledWith = [].slice.call(arguments);
      return true;
    };
  },
  afterEach: function() {
    Ember.run(application, 'destroy');
    window.confirm = originalConfirm;
    confirmCalledWith = null;
  }
});

test('visiting /permissions without data', function(assert) {
  visit('/permissions');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.index');
    assert.equal(find('#blankslate').text().trim(), 'No Permissions found');
  });
});

test('visiting /permissions with data', function(assert) {
  server.create('permission');
  visit('/permissions');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('create a new permission', function(assert) {
  visit('/permissions');
  click('a:contains(New Permission)');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.new');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('update an existing permission', function(assert) {
  server.create('permission');
  visit('/permissions');
  click('a:contains(Edit)');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.edit');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('show an existing permission', function(assert) {
  server.create('permission');
  visit('/permissions');
  click('a:contains(Show)');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.show');

    assert.equal(find('p strong:contains(Name:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Description:)').next().text(), 'MyString');
  });
});

test('delete a permission', function(assert) {
  server.create('permission');
  visit('/permissions');
  click('a:contains(Remove)');

  andThen(function() {
    assert.equal(currentPath(), 'permissions.index');
    assert.deepEqual(confirmCalledWith, ['Are you sure?']);
    assert.equal(find('#blankslate').length, 1);
  });
});
