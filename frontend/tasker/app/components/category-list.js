import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  store: Ember.inject.service('store'),
  session: Ember.inject.service(),
  addNewCategoryDialog: null,

  hasEditPermission: Ember.computed('store', function () {
    let that = this;
    let token = this.get('session.data').authenticated.token;
    Ember.$.ajax({
      url: ENV.host + '/api-has-permission/',
      type: 'POST',
      headers: {
        'Authorization': 'Token ' + token
      },
      data: that.get('project.id'),
      contentType: 'application/json;charset=utf-8',
      dataType: 'json'
    }).then(function (response) {
      alert(response);
      that.set('hasEditPermission', response == 'True')
    }, function (xhr/*, status, error*/) {
      that.set('hasEditPermission', xhr.status === 200)
    });
  }),

  didInsertElement() {
    let store = this.get('store');
    let $this = this.$();
    $this.find('.cardList').sortable({
      connectWith: ".connectedCategory",
      placeholder: "ui-state-highlight",
      cancel: ".ui-state-disabled",
      dropOnEmpty: true,
      update: function (event, ui) {
        let cardId = ui.item.find('li').attr('data-card-id');

        store.find('card', cardId).then(function (card) {
          $this.find('.ember-list-element').each(function () {

            let categoryId = Ember.$(this).attr('data-category-id');
            Ember.$(this).find('.cardList .card').each(function (card_index) {

              if (Ember.$(this).attr('data-card-id') === cardId) {
                store.find('category', categoryId).then(function (category) {
                  if (card.get('category') !== category
                    || card.get('orderInCategory') !== card_index) {
                    card.set('category', category);
                    card.set('orderInCategory', card_index);
                    card.save();
                  }
                });
              }
            })
          });
        });
      }
    }).disableSelection();
  },

  didRender() {
    let that = this;
    let dialog = Ember.$("#addNewCategoryDialog").dialog({
      autoOpen: false,
      height: 100,
      width: 250,
      modal: true,
      buttons: {
        "Apply": function () {
          let newCategory = that.get('store').createRecord('category', {
            name: that.get('newCategoryName'),
            project: that.get('project')
          });
          newCategory.save();
          //location.reload();
          dialog.dialog('close');
        },
        Cancel: function () {
          dialog.dialog('close');
        }
      },
      close: function () {
      }
    });
    this.set('addNewCategoryDialog', dialog);

    let sumOfWidth = 100;
    Ember.$('.category-list-element').each(function() {
      sumOfWidth += Ember.$(this).outerWidth();
    });
    Ember.$('.category-list').css('width', sumOfWidth)
  },

  actions: {
    showAddNewCategoryDialog() {
      this.get('addNewCategoryDialog').dialog("open");
    },

    addNewCategory() {
      let newCategory = this.get('store').createRecord('category', {
        name: this.get('newCategoryName'),
        project: this.get('project')
      });
      newCategory.save();
      if (!Ember.testing) {
        location.reload();
      }
      this.get('addNewCategoryDialog').dialog('close');
    },
    reloadModel() {
      this.sendAction();
    }
  }


});
