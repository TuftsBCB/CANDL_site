import Constants from '../constants/Constants';
import assign from 'object-assign';

const initialState = {
  graph1: {},
  graph2: {},
  LMs: {},
  g1Name: "",
  g2Name: "",
  lmName: "",
  email: "",
  waiting: 0,
  success: 0,
  failure: 0,
};

export default function reduce(state = initialState, action) {
  switch (action.type) {
  case Constants.FILE_DROP1:
    return assign({}, state, {
      graph1: action.file,
      g1Name: action.file.name,
    });

  case Constants.FILE_DROP2:
    return assign({}, state, {
      graph2: action.file,
      g2Name: action.file.name,
    });

  case Constants.FILE_DROP3:
    return assign({}, state, {
      LMs: action.file,
      lmName: action.file.name,
    });

  case Constants.CHANGE_EMAIL:
    return assign({}, state, {
      email: action.email,
    });

  // not yet implemented
  case Constants.SUBMIT:
  case Constants.SUBMIT_SUCCEEDED:
  case Constants.SUBMIT_FAILED:
    return state;

  default:
    return state;
  }
}
