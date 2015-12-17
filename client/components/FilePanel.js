import React, { Component, PropTypes } from 'react';
import { connect }      from 'react-redux';
import Dropzone from 'react-dropzone'

import {
  uploadFile,
  // ADD FUNCTIONS HERE
}   from '../actions/actions';

export default class FilePanel extends Component {
  constructor(props) {
    super(props);
    this.state = {hasFile: false};
  }

  render() {
    const {dropFile, fileLabel, fileName} = this.props;
    const tx = fileName || 'Drag and drop file, or click to upload';

    return (
      <div className="upload-panel">
        <h4>{fileLabel}</h4>
        <Dropzone id="lesstall" onDrop={this.props.dropFile} >
          <div id="drop" multiple="false" >{tx}</div>
        </Dropzone>
      </div>
    );
  }
}

FilePanel.propTypes = {
  dropFile: PropTypes.func.isRequired,
  fileLabel: PropTypes.string.isRequired,
  fileName: PropTypes.string.isRequired,
};
