import DS from 'ember-data';

export default DS.Model.extend({
  name: DS.attr('string'),
  description: DS.attr('string'),
  dateCreated: DS.attr('date'),
  lastModified: DS.attr('date'),
  createdBy: DS.belongsTo('user'),
  modifiedBy: DS.belongsTo('user'),
  category: DS.belongsTo('category', {inverse: 'cards', async: true})
});
