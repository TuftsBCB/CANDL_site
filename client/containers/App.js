import React, { Component, PropTypes } from 'react';
import { connect }      from 'react-redux';
import AddEmail from '../components/AddEmail';
import FilePanel from '../components/FilePanel';
import {
  uploadFile1,
  uploadFile2,
  uploadFile3,
  changeEmail,
  submitAll,
  // ADD FUNCTIONS HERE
}   from '../actions/actions';


class MyApp extends Component {
  render() {
    const {dispatch, graph1, graph2, LMs, g1Name, g2Name, lmName, email} = this.props;

    return (
      <div id="outside">
        <h1> Run CANDL on your own files</h1>
        <div>
          <FilePanel fileLabel="First Graph File" fileName={g1Name} dropFile={files => dispatch(uploadFile1(files))}/>
          <FilePanel fileLabel="Second Graph File" fileName={g2Name} dropFile={files => dispatch(uploadFile2(files))}/>
          <FilePanel fileLabel="Landmarks File" fileName={lmName} dropFile={files => dispatch(uploadFile3(files))}/>
        </div>
        <div>
          <AddEmail onClick={(e) => dispatch(changeEmail(e))} />
        </div>
        <div>
          <button onClick={() => dispatch(submitAll(graph1, graph2, LMs, email))}>Run CANDL!</button>
        </div>
      </div>
    );
  }
}

MyApp.propTypes = {
  dispatch: PropTypes.func.isRequired,
  graph1: PropTypes.object.isRequired,
  graph2: PropTypes.object.isRequired,
  LMs: PropTypes.object.isRequired,
  g1Name: PropTypes.string.isRequired,
  g2Name: PropTypes.string.isRequired,
  lmName: PropTypes.string.isRequired,
};


// for now, we want it all!
const select = state => state;

// Wrap the component to inject dispatch and state into it
export default connect(select)(MyApp);
