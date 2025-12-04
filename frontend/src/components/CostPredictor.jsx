import React from 'react';

const CostPredictor = ({ costData }) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold mb-2">Cost Predictor</h3>
      <div className="text-3xl font-bold text-green-600">
        KES {costData.current_bill_estimate}
      </div>
      <p className="text-sm text-gray-500">Estimated Bill</p>
      {costData.savings > 0 && (
        <div className="mt-2 text-sm text-green-500 bg-green-50 px-2 py-1 rounded inline-block">
          You're saving KES {costData.savings} with active discounts!
        </div>
      )}
    </div>
  );
};

export default CostPredictor;
