import Ember from 'ember';
import ENV from 'tasker/config/environment';

export default Ember.Component.extend({
  session: Ember.inject.service(),
  isServiceWorkerUnsupported: null,
  tagName: "span",
  applicationServerPublicKey: "BGT0GrbebqIG90p4Dz33vEk6PaiICRpLy4_Oryjyqd2jzLbnIAW5xKbPLkO4rUPqF53GqcFylAu_LvlcJCsBo-0",

  urlB64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/\-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  },

  updateServer(self, subscription) {
    Ember.$.ajax({
      url: ENV.host + '/api-register-service-worker/',
      type: 'POST',
      data: JSON.stringify({
        subscription_id: JSON.stringify(subscription),
        token: self.get('session.data').authenticated.token
      }),
      contentType: 'application/json;charset=utf-8',
      dataType: 'json'
    }).then((response) => {
      alert('sent!');
      if (response != "OK") {
        /* Do nothing here */
      }
    }, (xhr/*, status, error*/) => {
      let response = xhr.responseText;
      Ember.run(function () {
        reject(response);
      });
    });
  },

  didRender() {

    if ('serviceWorker' in navigator && 'PushManager' in window) {
      //console.log('Service Worker and Push is supported!');

      navigator.serviceWorker.register('/service-worker.js').then((registration) => {
        //console.log('Service worker is registered: ', registration);
        this.set('swRegistration', registration);
        this.send('subscribeSw');
      }).catch((/*error*/) => {
        this.set('isServiceWorkerUnsupported', true);
      });
    } else {
      this.set('isServiceWorkerUnsupported', true);
    }
  },

  actions: {
    subscribeSw() {
      const applicationServerKey = this.get('urlB64ToUint8Array')(this.get('applicationServerPublicKey'));
      this.get('swRegistration').pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: applicationServerKey
      }).then((subscription) => {
        //console.log("User is subscribed!");
        //console.log(JSON.stringify(subscription));
        this.get('updateServer')(this, subscription);
      }).catch((/* error */) => {
        /* Do nothing */
      });
      this.get('swRegistration').pushManager.getSubscription().then((subscription) => {
        this.set('isSubscribed', !(subscription === null));
      });
    }
  }
});
