import React, { useState } from 'react'

function Model({ targetRef }) {
    const [image, setimage] = useState('')
    const [url, seturl] = useState('')

    const fileHandle = e => {
        if (e.target.files.length !== 0) {
            setimage(e.target.files[0])
        }
    }

    const urlHandle = e =>{
        seturl(e.target.value);
    }

    const predict_image = e =>{
        e.preventDefault();
        console.log(image);
    }

    const predict_url = e =>{
        e.preventDefault();
        console.log(url);
    }

    return (
        <div class="relative z-10 max-w-screen-lg mx-auto pt-10 h-screen" id="model" ref={targetRef}>
            {/* {#    <h2 class="text-4xl font-bold mb-4">ML Model</h2>#} */}
            <h1 class="text-4xl font-bold mb-4">Try It Now!</h1>
            <p class="text-10lg mb-10">Experience the power of image classification. Upload your images and see instant results!</p>

            <div class="grid grid-cols-2 gap-4 ">
                {/* <!-- First Column --> */}
                <div>
                    <div class="max-w-screen-lg mx-auto mb-8">
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

                    <div class="max-w-screen-lg mx-auto my-8 my-20">
                        <h2 class="text-3xl font-bold dark:text-black mb-4">Predict via Image URL</h2>
                        <form onSubmit={predict_url}>
                            <div class="mb-4">
                                <label for="imageUrl" class="block text-gray-800 text-xl font-semibold mb-2">Image URL</label>
                                <input onChange = {urlHandle}type="url" id="imageUrl" name="imageUrl" class="border rounded p-2 w-full" placeholder="https://example.com/image.jpg" required />
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
                <div>
                    <h2 class="text-3xl font-bold dark:text-black mb-4">Image Preview</h2>
                    <div id="imagePreview" class="border border-gray-300 rounded-md p-4">
                        {/* <!-- Image preview will be displayed here --> */}
                    </div>
                </div>
            </div>

        </div>
    )
}

export default Model