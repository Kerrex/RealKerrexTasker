import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({
  keyForAttribute(key) {
    return key.underscore();
  },

  keyForRelationship(key) {
    return key.underscore();
  }
});
