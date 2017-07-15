import { Factory } from 'ember-cli-mirage';

export default Factory.extend(
  {name: 'MyString', description: 'MyString', dateCreated: new Date(), lastModified: new Date(), createdBy: 'MyString', modifiedBy: 'MyString', category: 'MyString' }
);
