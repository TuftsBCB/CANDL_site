import React, { Component, PropTypes } from 'react';
import { connect }      from 'react-redux';


export default class AddEmail extends Component {
  constructor() {
    super(arguments);
  }

  render() {

    const {onClick} = this.props;

    return (
        <div>
          <h4>Email to send results: </h4>
          <input type="text" placeholder="Email" ref='input' onChange={e => this.handleChange(e)} />
        </div>
    )
  }

  handleChange(e) {

    const node  = this.refs.input;
    const text = node.value.trim()
    this.props.onClick(text);
  }
}

AddEmail.propTypes = {
  onClick: PropTypes.func.isRequired,
}