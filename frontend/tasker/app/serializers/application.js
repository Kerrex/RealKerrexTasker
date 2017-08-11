import DS from 'ember-data';

export default DS.JSONAPISerializer.extend({
  serialize(snapshot, options) {
    let json = this._super(...arguments);
    var relationshipObject = json.data.relationships;
    //json.data.relationships.owner.data.type = json.data.relationships.owner.data.type.capitalize();
    for (let relationship in relationshipObject) {
      console.log(relationship);
      if (relationshipObject[relationship].data) {
        relationshipObject[relationship].data.type = relationshipObject[relationship].data.type.capitalize();
      }

      //relationshipObject[relationship] = relationshipObject[relationship].data.id;
    }
    console.log(json);
    return json;
  },
  keyForAttribute(key) {
    return key.underscore();
  },

  keyForRelationship(key) {
    return key.underscore();
  }
});
