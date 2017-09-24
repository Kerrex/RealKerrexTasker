import DS from 'ember-data';

export default DS.Model.extend({
  user: DS.belongsTo('user', {async: true}),
  card: DS.belongsTo('card', {async: true}),
  minutesBeforeStart: DS.attr('number')
});
