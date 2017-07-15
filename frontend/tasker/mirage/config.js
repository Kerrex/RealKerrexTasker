import Response from "ember-cli-mirage/response";
export default function() {
this.get('/cards');
this.get('/cards/:id');
this.post('/cards');
this.del('/cards/:id');
this.patch('/cards/:id');
this.get('/categories');
this.get('/categories/:id');
this.post('/categories');
this.del('/categories/:id');
this.patch('/categories/:id');
this.get('/permissions');
this.get('/permissions/:id');
this.post('/permissions');
this.del('/permissions/:id');
this.patch('/permissions/:id');
this.get('/projects');
this.get('/projects/:id');
this.post('/projects');
this.del('/projects/:id');
this.patch('/projects/:id');

  // These comments are here to help you get started. Feel free to delete them.

  /*
    Config (with defaults).

    Note: these only affect routes defined *after* them!
  */

  this.urlPrefix = 'http://localhost:8000';    // make this `http://localhost:8080`, for example, if your API is on a different server
  // this.namespace = '';    // make this `/api`, for example, if your API is namespaced
  // this.timing = 400;      // delay for each request, automatically set to 0 during testing

  /*
    Shorthand cheatsheet:

    this.get('/posts');
    this.post('/posts');
    this.get('/posts/:id');
    this.put('/posts/:id'); // or this.patch
    this.del('/posts/:id');

    http://www.ember-cli-mirage.com/docs/v0.3.x/shorthands/
  */
  this.post('/api-auth-token/', (db, request) => {
    let attrs = JSON.parse(request.requestBody);
    if (attrs.username === 'goodusername' && attrs.password === 'goodpassword') {
      return '{"token": "e5d92c005934e4034b8335e03ee836fae4ceecfd"}';
    } else {
      return new Response(400,
                          {'Content-Type': 'application/json'},
                          {"status": "400", "source": {"pointer": "/data/attributes/non_field_errors"},
                            "detail": "Unable to log in with provided credentials."});
    }

  });
}
