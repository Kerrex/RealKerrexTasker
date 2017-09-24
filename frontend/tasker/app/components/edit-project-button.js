import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  tagName: 'span',
  hasEditPermission: Ember.computed('store', function () {
    //alert('Im here!');
    let that = this;
    Ember.$.ajax({
      url: ENV.host + '/api-has-permission/',
      type: 'POST',
      data: that.get('project.id'),
      contentType: 'application/json;charset=utf-8',
      dataType: 'json'
    }).then(function (response) {
      //alert(response);
      that.set('hasEditPermission', response == 'True')
    }, function (xhr/*, status, error*/) {
      //alert(xhr.status);
      //console.log(xhr);
      that.set('hasEditPermission', xhr.status === 200)
    });
  }),
});
