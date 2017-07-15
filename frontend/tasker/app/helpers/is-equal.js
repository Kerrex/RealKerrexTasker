import Ember from 'ember';

export function isEqual(param1, param2) {
  console.log(param1);
  return param1 == param2;
}

export default Ember.Helper.helper(isEqual);
