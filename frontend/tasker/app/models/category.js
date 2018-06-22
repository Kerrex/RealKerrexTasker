import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  orderInProject: DS.attr('number'),
  project: DS.belongsTo('project', {async: true}),
  cards: DS.hasMany('card', {inverse: 'category', async: true})
});
