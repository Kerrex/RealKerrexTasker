import Ember from 'ember';
import { module, test } from 'qunit';
import startApp from '../helpers/start-app';
import { currentSession, authenticateSession, invalidateSession } from 'tasker/tests/helpers/ember-simple-auth';

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

test('visiting / without data', function(assert) {
  authenticateSession(application);
  visit('/');

  andThen(function() {
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').text().trim(), 'No projects found. Please use button above to add your first one!');
  });
});

test('visiting /projects with data', function(assert) {
  authenticateSession(application);
  server.create('project', {user_id: 0});
  visit('/');

  andThen(function() {
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('.board-tile').length, 1);
  });
});

test('create a new project', function(assert) {
  authenticateSession(application);
  server.loadFixtures('permissions');
  visit('/');
  click('.new-project-button');

  andThen(function() {
    assert.equal(currentPath(), 'projects.new');
    let secondOption = find(".select-permission option:eq(1)");
    fillIn('input#name', 'NewProject');
    fillIn('input#description', 'MyProject');
    fillIn('.select-permission', secondOption.val());

    click('input:submit');
  });

  andThen(function() {
    visit('/');
  });
  andThen(function () {
    assert.equal(find('#blankslate').length, 0);
    assert.equal(find('.board-tile').length, 1);
  });
});

test('add new permission to existing project', function (assert) {
  authenticateSession(application);
  server.loadFixtures('users');
  server.create('project', {owner_id: 1});

  visit('/1/edit');

  andThen(function () {

    assert.equal(currentPath(), 'projects.edit');
    assert.equal(currentURL(), "/1/edit");
    click('.add-new-user-permission-button');
  });

  andThen(function () {
    fillIn('#add-permission-username', "email2@email.pl");
    click('#add-edit-permission-modal .btn');
  });

});

test('update an existing project', function(assert) {
  authenticateSession(application);
  server.loadFixtures('users');
  server.create('project', {owner_id: 0});
  visit('/1/edit');

  andThen(function() {
    assert.equal(currentPath(), 'projects.edit');
    assert.equal(currentURL(), "/1/edit");
    fillIn("input#name", "New name");
    fillIn("input#description", "New description");
    click('input.btn-primary');
  });
  andThen(function () {
    visit('/');
  });

  andThen(function() {
    let boardTile = find('.board-tile');
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').length, 0);
    assert.equal(boardTile.length, 1);
    assert.equal(boardTile.find('.project-name').text(), "New name");
    assert.equal(boardTile.find('.project-description').text(), "New description");
  });
});

test('enter existing project', function(assert) {
  authenticateSession(application);
  server.create('project');
  visit('/');
  click('.board-tile');

  andThen(function() {
    assert.equal(currentPath(), 'projects.show');
    assert.equal(currentURL(), '/1')
  });
});

test('delete a project', function(assert) {
  authenticateSession(application);
  server.create('project');
  visit('/1/edit');
  click('a.remove-project-button');

  andThen(function() {
    assert.equal(currentPath(), 'projects.delete');
    assert.equal(currentURL(), "/1/delete");

    click('a.btn-danger');
  });

  andThen(function () {
    assert.equal(currentPath(), 'projects.index');
    assert.equal(find('#blankslate').text().trim(), 'No projects found. Please use button above to add your first one!');
  });
});

test('add new category', function (assert) {
  authenticateSession(application);
  server.create('project');
  visit('/1');
  //click('.add-new-category');

  andThen(() => {
    assert.equal(find('.category-list-element').length, 1);
    server.create('category', {project_id: 1});
    click('.go-to-project-list-button');
    // Nie działa z powodu JQuery UI i sposobu wyświetlania dialogów
    //let dialog = find('#addNewCategoryDialog');
    //fillIn('.new-category-input', "New category");
    //click('#addNewCategoryDialog .ui-dialog-buttonset'.find('button:eq(0)'));
  });

  andThen(() => {
    assert.equal(currentPath(), 'projects.index');
    click('.board-tile');
  });

  andThen(() => {
    assert.equal(currentPath(), 'projects.show');
    assert.equal(find('.category-list-element').length, 2);
  });
});

test('go to project list button on project main page', function (assert) {
  authenticateSession(application);
  server.create('project');
  visit('/1');
  click('.go-to-project-list-button');

  andThen(() => {
    assert.equal(currentPath(), 'projects.index');
  });
});

test('add new card in existing category', function (assert) {
  authenticateSession(application);
  server.create('project');
  server.create('category', {project_id: 1});
  visit('/1');
  //click('.add-new-category');

  andThen(() => {
    assert.equal(find('.category-list-element').length, 2);
    assert.equal(find('.category-list .cardList li').length, 1);
    server.create('card', {category_id: 1});
    click('.go-to-project-list-button');
    // Nie działa z powodu JQuery UI i sposobu wyświetlania dialogów
    //click('.ui-slate-add-new');
    //fillIn('input[name="newCardName"]', "New card");
    //click('#addNewCategoryDialog .ui-dialog-buttonset button:eq(0)');
  });

  andThen(() => {
    click('.board-tile');
  });

  andThen(() => {
    assert.equal(currentPath(), 'projects.show');
    assert.equal(find('.category-list-element').length, 2);
    assert.equal(find('.category-list .cardList li').length, 2);
  });
});

test('calendar shows up', function (assert) {
  authenticateSession(application);
  server.create('project');
  visit('/1');

  andThen(() => {
    assert.equal(currentPath(), 'projects.show');
    assert.equal(find('#board-calendar-modal').css('display'), 'none');
    click('#show-calendar-button');
  });

  andThen(() => {
    assert.equal(find('#board-calendar-modal').css('display'), 'block');
  });
});


