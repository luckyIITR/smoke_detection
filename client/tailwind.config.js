import withMT from "@material-tailwind/react/utils/withMT";
export default withMT({
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./node_modules/flowbite/**/*.js",
    "./index.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [require('flowbite/plugin')],
});

