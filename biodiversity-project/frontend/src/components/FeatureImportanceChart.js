import React from 'react';
import Plot from 'react-plotly.js';

const FeatureImportanceChart = ({ data }) => {
  return (
    <Plot
      data={[
        {
          x: data.map(d => d.feature),
          y: data.map(d => d.importance),
          type: 'bar'
        }
      ]}
      layout={{ title: 'Feature Importance' }}
    />
  );
}

export default FeatureImportanceChart;
