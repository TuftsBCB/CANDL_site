import Constants  from '../constants/Constants';
import {
  sendFilesToServer
} from '../requester';


export function uploadFile1(files) {
  return { type: Constants.FILE_DROP1, file: files[0] };
}

export function uploadFile2(files) {
  return { type: Constants.FILE_DROP2, file: files[0] };
}

export function uploadFile3(files) {
  return { type: Constants.FILE_DROP3, file: files[0] };
}

export function changeEmail(email) {
  return { type: Constants.CHANGE_EMAIL, email: email };
}

export function submitAll(graph1, graph2, LMs, email) {

  // -----------------------------------------------------------
  // HERE IS WHERE YOU MAKE SURE all fields are well formed.
  var origG1 = graph1.name;
  var origG2 = graph2.name;
  var allCorrect = origG1.endsWith('.ppi') && origG2.endsWith('.ppi');
  // allCorrect = allCorrect && ... ;

  if (!allCorrect) return { type: Constants.SUBMIT_FAILED,  };
  // -----------------------------------------------------------


  return dispatch => {
    dispatch({ type: Constants.SUBMIT });
    sendFilesToServer(graph1, graph2, LMs, email).then(
      dispatch({ type: Constants.SUBMIT_SUCCEEDED })
    ).catch(e =>
      dispatch({ type: Constants.SUBMIT_FAILED, error: e })
    )
  }
}
