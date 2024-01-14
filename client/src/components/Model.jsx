import React, { useState } from 'react'
import PropTypes from 'prop-types';
import { predictbyimage, predictbyurl } from "../store/actions/predict";
import { connect } from 'react-redux';
import Spinner from "./Spinner";


const isObjectEmpty = (objectName) => {
    return Object.keys(objectName).length === 0
}

function Model({ modelRef, predict, predictbyimage, predictbyurl }) {

    const [image, setimage] = useState('')
    const [formData, setformData] = useState({
        url: '',
    })

    const fileHandle = e => {
        if (e.target.files.length !== 0) {
            setimage(e.target.files[0])
        }
    }

    const urlHandle = e => {
        setformData({ ...formData, [e.target.name]: e.target.value });
    }


    const predict_image = e => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', image, image.name);
        const url = URL.createObjectURL(image);
        predictbyimage({formData, url});
    }

    const predict_url = e => {
        e.preventDefault();
        // console.log(formData);

        predictbyurl(formData);
    }

    return (
        <div class="mx-auto container p-10" id="model" ref={modelRef}>
            {/* {#    <h2 class="text-4xl font-bold mb-4">ML Model</h2>#} */}
            <h1 class="text-4xl font-bold mb-4">Try It Now!</h1>
            <p class="text-10lg mb-10">Experience the power of image classification. Upload your images and see instant results!</p>

            <div class="flex flex-wrap">
                {/* <!-- First Column --> */}
                <div class="lg:w-1/2 p-2">
                    <div >
                        <h2 class="text-3xl font-bold dark:text-black mb-4">Predict via Uploading Image</h2>
                        <form onSubmit={predict_image}>
                            <div class="mb-4">
                                <label for="imageUpload" class="block text-gray-800 text-xl font-semibold mb-2">Choose an Image</label>
                                <input onChange={fileHandle} type="file" id="imageUpload" name="file" class="border rounded p-2 w-full" />
                            </div>
                            <button type="submit" class="bg-blue-500 text-white py-2 px-4 rounded-full inline-flex items-center">
                                <span class="mr-2">Predict</span>
                                <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6">
                                    <path d="M8 13L13 8L8 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="round"></path>
                                    <path d="M12 8L2 8" stroke="currentColor" stroke-width="1.5"></path>
                                </svg>
                            </button>
                        </form>
                    </div>

                    <div>
                        <h2 class="text-3xl font-bold dark:text-black mb-4">Predict via Image URL</h2>
                        <form onSubmit={predict_url}>
                            <div class="mb-4">
                                <label for="imageUrl" class="block text-gray-800 text-xl font-semibold mb-2">Image URL</label>
                                <input onChange={urlHandle} type="url" id="url" name="url" class="border rounded p-2 w-full" placeholder="https://example.com/image.jpg" required />
                            </div>
                            <button type="submit" class="bg-blue-500 text-white py-2 px-4 rounded-full inline-flex items-center">
                                <span class="mr-2">Predict</span>
                                <svg viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6">
                                    <path d="M8 13L13 8L8 3" stroke="currentColor" stroke-width="1.5" stroke-linecap="square" stroke-linejoin="round"></path>
                                    <path d="M12 8L2 8" stroke="currentColor" stroke-width="1.5"></path>
                                </svg>
                            </button>
                        </form>
                    </div>
                </div>

                {/* <!-- Second Column --> */}
                <div class="lg:w-1/2 p-2">
                    <h2 class="text-3xl font-bold dark:text-black mb-4">Result</h2>
                    <div id="imagePreview" class="border border-gray-300 rounded-md p-4 min-h-20">
                        {/* <!-- Image preview will be displayed here --> */}
                        {
                            !isObjectEmpty(predict.probability) && (<>
                                <img src={predict.probability.url} alt="Fixed Size Image" class="w-40 h-40 object-cover rounded-md shadow-lg mx-auto" />
                                <div className="max-w-sm mx-auto mt-4">
                                    <div>
                                        <div className="text-center">
                                            <h1 className="text-2xl font-bold mb-4">Smoke Probability :</h1>
                                            <h1 className="text-3xl text-red-500 font-bold mb-6">
                                                {predict.probability.SmokingProbability}
                                            </h1>
                                            <h1 className="text-2xl font-bold mb-4">Non Smoke Probability :</h1>
                                            <h1 className="text-3xl text-green-500 font-bold">
                                                {predict.probability.NonSmokingProbability}
                                            </h1>
                                        </div>
                                    </div>
                                </div>
                            </>
                            )
                        }
                        {
                            predict.loading &&
                            <Spinner />
                        }

                    </div>
                </div>
            </div>

        </div>
    )
}

Model.propTypes = {
    predict: PropTypes.object.isRequired
};

const mapStateToProps = (state) => ({
    predict: state.predict
});

export default connect(mapStateToProps, { predictbyimage, predictbyurl })(Model)