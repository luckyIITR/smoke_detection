import api from '../../utils/api';
import {
    PREDICT_DONE,
    PREDICT_ERROR,
    PREDICT_STARTED
} from '../types';
import { setAlert } from './alert';

// Predict by image
const predictbyimage = ({ formData, url }) => async (dispatch) => {
    dispatch({
        type: PREDICT_STARTED,
    });

    // Append the image file
    // console.log(formData);

    try {
        const res = await api.post('/smoke_detection_img', formData);

        dispatch({
            type: PREDICT_DONE,
            payload: { ...res.data, url: url }
        });

    } catch (err) {
        // console.log(err);
        dispatch({
            type: PREDICT_ERROR,
            payload: { msg: err.response, status: err.response }
        });
    }
};


// Predict by image
const predictbyurl = (formData) => async (dispatch) => {
    dispatch({
        type: PREDICT_STARTED,
    });
    try {
        const res = await api.post('/smoke_detection_url', formData);

        dispatch({
            type: PREDICT_DONE,
            payload: { ...res.data, url: formData.url }
        });

    } catch (err) {
        // console.log(err);
        dispatch(
            setAlert(err.response.data.detail, 'danger')
        );

        dispatch({
            type: PREDICT_ERROR,
            payload: { msg: err.response.data.detail, status: err.response.status }
        });
    }
};


export { predictbyimage, predictbyurl };
