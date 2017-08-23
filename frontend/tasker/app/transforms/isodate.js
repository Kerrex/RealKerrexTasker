import DS from 'ember-data';
import moment from "moment";

export default DS.Transform.extend({
  deserialize(serialized) {
    console.log(serialized);
    return serialized;
  },

  serialize(deserialized) {
    return moment(deserialized).format();
  }
});
