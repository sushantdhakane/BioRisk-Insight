const { override, addBabelPreset } = require('customize-cra');


module.exports = override(
  addBabelPreset('@babel/preset-env'),
  addBabelPreset('@babel/preset-react')
);
