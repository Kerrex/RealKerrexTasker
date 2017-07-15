import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;
var originalConfirm;
var confirmCalledWith;

module('Acceptance: Card', {
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

test('visiting /cards without data', function(assert) {
  visit('/cards');

  andThen(function() {
    assert.equal(currentPath(), 'cards.index');
    assert.equal(find('#blankslate').text().trim(), 'No Cards found');
  });
});

test('visiting /cards with data', function(assert) {
  server.create('card');
  visit('/cards');

  andThen(function() {
    assert.equal(currentPath(), 'cards.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('create a new card', function(assert) {
  visit('/cards');
  click('a:contains(New Card)');

  andThen(function() {
    assert.equal(currentPath(), 'cards.new');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');
    fillIn('label:contains(Datecreated) input', new Date());
    fillIn('label:contains(Lastmodified) input', new Date());
    fillIn('label:contains(Createdby) input', 'MyString');
    fillIn('label:contains(Modifiedby) input', 'MyString');
    fillIn('label:contains(Category) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('update an existing card', function(assert) {
  server.create('card');
  visit('/cards');
  click('a:contains(Edit)');

  andThen(function() {
    assert.equal(currentPath(), 'cards.edit');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');
    fillIn('label:contains(Datecreated) input', new Date());
    fillIn('label:contains(Lastmodified) input', new Date());
    fillIn('label:contains(Createdby) input', 'MyString');
    fillIn('label:contains(Modifiedby) input', 'MyString');
    fillIn('label:contains(Category) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('show an existing card', function(assert) {
  server.create('card');
  visit('/cards');
  click('a:contains(Show)');

  andThen(function() {
    assert.equal(currentPath(), 'cards.show');

    assert.equal(find('p strong:contains(Name:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Description:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Datecreated:)').next().text(), new Date());
    assert.equal(find('p strong:contains(Lastmodified:)').next().text(), new Date());
    assert.equal(find('p strong:contains(Createdby:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Modifiedby:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Category:)').next().text(), 'MyString');
  });
});

test('delete a card', function(assert) {
  server.create('card');
  visit('/cards');
  click('a:contains(Remove)');

  andThen(function() {
    assert.equal(currentPath(), 'cards.index');
    assert.deepEqual(confirmCalledWith, ['Are you sure?']);
    assert.equal(find('#blankslate').length, 1);
  });
});
