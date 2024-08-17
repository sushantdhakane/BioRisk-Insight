const { override, addBabelPreset } = require('customize-cra');


export default override(
  addBabelPreset('@babel/preset-env'),
  addBabelPreset('@babel/preset-react')
);
