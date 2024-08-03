import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SpeciesRiskMap from './components/SpeciesRiskMap';
import FeatureImportanceChart from './components/FeatureImportanceChart';
import SpeciesDetailView from './components/SpeciesDetailView';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SpeciesRiskMap />} />
        <Route path="/feature-importance" element={<FeatureImportanceChart />} />
        <Route path="/species/:id" element={<SpeciesDetailView />} />
      </Routes>
    </Router>
  );
}

export default App;
