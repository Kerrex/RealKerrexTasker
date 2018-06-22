module.exports = {
  globals: {
    server: true,
    Ember: true,
    Uint8Array: true,
    reject: true
  },
  root: true,
  parserOptions: {
    ecmaVersion: 2017,
    sourceType: 'module'
  },
  extends: 'eslint:recommended',
  env: {
    browser: true
  },
  rules: {
  }
};
