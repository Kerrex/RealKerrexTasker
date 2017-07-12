import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';

var application;
var originalConfirm;
var confirmCalledWith;

module('Acceptance: Project', {
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

test('visiting /projects without data', function(assert) {
  visit('/projects');

  andThen(function() {
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').text().trim(), 'No Projects found');
  });
});

test('visiting /projects with data', function(assert) {
  server.create('project');
  visit('/projects');

  andThen(function() {
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('create a new project', function(assert) {
  visit('/projects');
  click('a:contains(New Project)');

  andThen(function() {
    assert.equal(currentPath(), 'projects.new');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');
    fillIn('label:contains(Date created) input', new Date());
    fillIn('label:contains(Last modified) input', new Date());
    fillIn('label:contains(Owner) input', 'MyString');
    fillIn('label:contains(Default permission) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('update an existing project', function(assert) {
  server.create('project');
  visit('/projects');
  click('a:contains(Edit)');

  andThen(function() {
    assert.equal(currentPath(), 'projects.edit');

    fillIn('label:contains(Name) input', 'MyString');
    fillIn('label:contains(Description) input', 'MyString');
    fillIn('label:contains(Date created) input', new Date());
    fillIn('label:contains(Last modified) input', new Date());
    fillIn('label:contains(Owner) input', 'MyString');
    fillIn('label:contains(Default permission) input', 'MyString');

    click('input:submit');
  });

  andThen(function() {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('table tbody tr').length, 1);
  });
});

test('show an existing project', function(assert) {
  server.create('project');
  visit('/projects');
  click('a:contains(Show)');

  andThen(function() {
    assert.equal(currentPath(), 'projects.show');

    assert.equal(find('p strong:contains(Name:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Description:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Date created:)').next().text(), new Date());
    assert.equal(find('p strong:contains(Last modified:)').next().text(), new Date());
    assert.equal(find('p strong:contains(Owner:)').next().text(), 'MyString');
    assert.equal(find('p strong:contains(Default permission:)').next().text(), 'MyString');
  });
});

test('delete a project', function(assert) {
  server.create('project');
  visit('/projects');
  click('a:contains(Remove)');

  andThen(function() {
    assert.equal(currentPath(), 'projects.index');
    assert.deepEqual(confirmCalledWith, ['Are you sure?']);
    assert.equal(find('#blankslate').length, 1);
  });
});
