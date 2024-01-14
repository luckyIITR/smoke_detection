import { combineReducers } from "redux";
import alertReducer from "./alertReducer";
import predictReducer from "./predictReducer";


export default combineReducers({
  "alert" : alertReducer,
  "predict" : predictReducer
});