import DS from 'ember-data';

export default DS.Model.extend({
  givenBy: DS.belongsTo('user', {async: true}),
  permission: DS.belongsTo('permission', {async: true}),
  project: DS.belongsTo('project', {async: true}),
  user: DS.belongsTo('user', {async: true})
});
