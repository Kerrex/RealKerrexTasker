import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;
var originalConfirm;
var confirmCalledWith;

module('Acceptance: Category', {
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

test('visiting /categories without data', function(assert) {
  visit('/categories');

  andThen(function() {
    assert.equal(currentPath(), 'categories.index');
    assert.equal(find('#blankslate').text().trim(), 'No Categories found');
  });
});

test('visiting /categories with data', function(assert) {
  server.create('category');
  visit('/categories');

  andThen(function() {
    assert.equal(currentPath(), 'categories.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('create a new category', function(assert) {
  visit('/categories');
  click('a:contains(New Category)');

  andThen(function() {
    assert.equal(currentPath(), 'categories.new');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Order in project) input', 42);
    fillIn('label:contains(Project) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('update an existing category', function(assert) {
  server.create('category');
  visit('/categories');
  click('a:contains(Edit)');

  andThen(function() {
    assert.equal(currentPath(), 'categories.edit');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Order in project) input', 42);
    fillIn('label:contains(Project) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('show an existing category', function(assert) {
  server.create('category');
  visit('/categories');
  click('a:contains(Show)');

  andThen(function() {
    assert.equal(currentPath(), 'categories.show');

    assert.equal(find('p strong:contains(Name:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Order in project:)').next().text(), 42);
    assert.equal(find('p strong:contains(Project:)').next().text(), 'MyString');
  });
});

test('delete a category', function(assert) {
  server.create('category');
  visit('/categories');
  click('a:contains(Remove)');

  andThen(function() {
    assert.equal(currentPath(), 'categories.index');
    assert.deepEqual(confirmCalledWith, ['Are you sure?']);
    assert.equal(find('#blankslate').length, 1);
  });
});
