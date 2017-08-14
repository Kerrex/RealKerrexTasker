import DS from 'ember-data';
import ENV from 'tasker/config/environment';
import DataAdapterMixin from 'ember-simple-auth/mixins/data-adapter-mixin';

export default DS.JSONAPIAdapter.extend(DataAdapterMixin, {
  host: ENV.host,
  namespace: 'api',
  authorizer: 'authorizer:drf-token-authorizer',

  shouldReloadRecord: function (store, snapshot) {
    return true;
  },

  shouldReloadAll: function (store, snapshot) {
    return true;
  },

  shouldBackgroundReloadRecord: function (store, snapshot) {
    return true;
  },

  shouldBackgroundReloadAll: function (store, snapshot) {
    return true;
  }
});
