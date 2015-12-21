import express from 'express';
import fs from "fs";
import multer from 'multer'
import PythonShell from 'python-shell';

const router = new express.Router();
const multerOptions = multer.diskStorage({
  destination: 'uploads/',
  // this function can be whatever you want - just doing an example here
  filename: (req, file, cb) => {
    cb(null, file.fieldname);
  }
});
const upload = multer({ storage: multerOptions });

// define as its own function so we can invoke manually
const graphUpload = upload.fields([{
  name: 'graph1', maxCount: 1
}, {
  name: 'graph2', maxCount: 1
}, {
  name: 'LMs', maxCount: 1
}]);
router.post('/upload', (req, res) => {
  // manually call function so we can manually do error handling
  graphUpload(req, res, e => {
    // if there's an error set the status and send it
    if (e) {
      res.status(500);
      res.json(e);
    // otherwise send a noop so that the client knows everything went a-ok
    } else {

      var email = req.body.email;
      var fdr = 'uploads/' + "sub" + Date.now() + '/';
      fs.mkdir(fdr);

      var newG1name = req.files.graph1[0].filename;
      var newG2name = req.files.graph2[0].filename;
      var newLMname = req.files.LMs[0].filename;

      setTimeout(function(){
        fs.rename('uploads/' +  req.files.graph1[0].filename, fdr + newG1name);
        fs.rename('uploads/' +  req.files.graph2[0].filename, fdr + newG2name);
        fs.rename('uploads/' +  req.files.LMs[0].filename, fdr + newLMname);
      }, 100);

      var options = {
        args: [newG1name, newG2name, newLMname, email, fdr]
      };

      PythonShell.run('run_CANDL_outer.py', options, function (err) {
        if (err){
          console.log('python error');
          res.status(500);
          res.json(e);
        } else {
          console.log('finished');
          res.json({});
        }
      });
    }
  });
});

export default router;
