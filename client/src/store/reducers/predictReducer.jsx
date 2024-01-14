import { PREDICT_DONE, PREDICT_ERROR, PREDICT_STARTED } from "../types";

const initialState = {
    img: null,
    loading : false,
    probability : {},
    error: {}
};

function predictReducer(state = initialState, action) {
    const { type, payload } = action;

    switch (type) {
        case PREDICT_DONE:
            return {
                ...state,
                loading : false,
                probability: payload
            };
        case PREDICT_ERROR:
            return {
                ...state,
                loading : false,
                error: payload,
            };
        case PREDICT_STARTED:
            return {
                ...state,
                loading : true,
                img: null,
                probability : {},
            }
        default:
            return state;
    }
}

export default predictReducer;