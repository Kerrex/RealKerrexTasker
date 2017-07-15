import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({
  serialize(snapshot, options) {
    let json = this._super(...arguments);
    var relationshipObject = json.data.relationships;
    //json.data.relationships.owner.data.type = json.data.relationships.owner.data.type.capitalize();
    for (let relationship in relationshipObject) {
      console.log(relationship);

      relationshipObject[relationship].data.type = relationshipObject[relationship].data.type.capitalize();
    }
    return json;
  },
  keyForAttribute(key) {
    return key.underscore();
  },

  keyForRelationship(key) {
    return key.underscore();
  }
});
