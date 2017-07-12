import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  description: DS.attr('string'),
  dateCreated: DS.attr('date'),
  lastModified: DS.attr('date'),
  defaultPermission: DS.belongsTo('permission', {async: true}),
  owner: DS.belongsTo('user', {async: true}),
});
