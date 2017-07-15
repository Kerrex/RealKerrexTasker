import Ember from 'ember';
import SaveModelMixin from 'tasker/mixins/categories/save-model-mixin';

export default Ember.Route.extend(SaveModelMixin, {
  model: function() {
    return this.store.createRecord('category');
  }
});
