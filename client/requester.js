  import request from 'superagent';

export function sendFilesToServer(graph1, graph2, LMs, email) {
  var formData = new FormData();
  if (graph1 && graph1 instanceof File) {
    formData.append('graph1', graph1);
  }
  if (graph2 && graph2 instanceof File) {
    formData.append('graph2', graph2);
  }
  if (LMs && LMs instanceof File) {
    formData.append('LMs', LMs);
  }
  if (email && typeof email === 'string') {
    formData.append('email', email);
  }
  return _postHelper('/upload', formData);
}

function _postHelper(url, formData) {
  return new Promise((resolve, reject) => {
    request.post(url)
      .send(formData)
      .end((err, response) => {
        if (err) {
          reject(err);
        } else {
          resolve(res.body);
        }
    });
  })
}
