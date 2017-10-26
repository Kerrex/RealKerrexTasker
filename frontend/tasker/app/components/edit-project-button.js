import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  session: Ember.inject.service(),
  tagName: 'span',
  hasEditPermission: Ember.computed('store', function () {
    //alert('Im here!');
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
      //alert(response);
      that.set('hasEditPermission', response == 'True')
    }, function (xhr/*, status, error*/) {
      //alert(xhr.status);
      //console.log(xhr);
      that.set('hasEditPermission', xhr.status === 200)
    });
  }),
});
